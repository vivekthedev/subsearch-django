from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("search/<pk:uuid>", views.search_subs, name="search"),
]