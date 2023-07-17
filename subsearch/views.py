from celery import shared_task
from django.shortcuts import render
from datetime import datetime
from django.core.files.storage import default_storage
from django.conf import settings
import boto3
import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

def index(request):
    if request.method == "POST":
        file = request.FILES['video-file']
        unique_name = datetime.now().strftime("%Y%m%d%H%M%S") + '-' + file.name
        upload_dir = settings.BASE_DIR / 'media' / unique_name
        default_storage.save(upload_dir, file)
        srt_location = settings.BASE_DIR/ 'media' / unique_name + '.srt'
        video_id = str(uuid.uuid4())
        process_video.delay(upload_dir.as_uri(), srt_location.as_uri(), video_id)
        return redirect('search', pk=video_id)
        
    return render(request, "index.html", {})

@shared_task
def process_video(file, srt_location, video_id):
    s3_client = boto3.client('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    s3_client.upload_file(file, os.environ.get('AWS_BUCKET_NAME'), file.name)

    subprocess.run(['/cc/ccextractor/linux/ccextractor', file, '-o', srt_location])
    
    dynamo_client = boto3.client('dynamodb', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    table = dynamo_client.Table(os.environ.get('AWS_TABLE_NAME'))
    item = {
        'pk' : video_id,
        'video' : file,
        'subs' : srt_location
    }
    table.put_item(Item=item)


def search_subs(request, pk):
    pass

def srt_file_view(request, uuid):
    
    dynamo_client = boto3.client('dynamodb', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    table = dynamo_client.Table(os.environ.get('AWS_TABLE_NAME'))

    response = table.get_item(Key={'uuid': uuid})
    item = response.get('Item', None)

    if item is None:
        return HttpResponse('SRT file not found.', status=404)

    srt_content = item.get('content', None)

    if request.GET['phrase']:
        phrase = request.GET['phrase']
        timestamps = search_phrase_in_srt(srt_content, phrase)
        return render(request, 'srt_results.html', {'timestamps': timestamps, 'phrase': phrase})

    return render(request, 'srt_form.html', {'uuid': uuid})

def search_phrase_in_srt(srt_content, phrase):
    timestamps = []
    subtitle_entries = srt_content.strip().split('\n\n')

    for entry in subtitle_entries:
        lines = entry.split('\n')

        timestamps_line = lines[1]
        subtitle_text_lines = lines[2:]

        if phrase in ' '.join(subtitle_text_lines):
            timestamps.append(timestamps_line)

    return timestamps
