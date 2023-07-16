# subsearch-django
A Django app to search a video's subtitle phrases to get the timestamp

## Technologies Used
- Django
- Celery
- Amazon SQS
- DynamoDB
- S3 Storage
- Docker

## How to use?
Step 1:

Clone the repository locally in your system
```
git clone  https://github.com/vivekthedev/subsearch-django.git
```

Step 2:

Create a `.env` file in the project directory and populate the values of the following fields:

```
AWS_ACCESS_KEY=""
AWS_SECRET_KEY=""
DJANGO_SECRET_KEY=""
AWS_BUCKET_NAME=""
AWS_TABLE_NAME=""
```

Step 3:

(NOTE: For this step please make sure that you have docker installed and Docker Daemon is running in your system.)
Crate docker image from the Dockerfile using the following command.
```
docker build .
```

Step 4:
Run the two container- web and celery to run your application
```
docker-compose up -d
```

Step 5:
Goto http://127.0.0.1:8000/

