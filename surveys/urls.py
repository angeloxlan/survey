from django.urls import path
from django.http import HttpResponse

from .views import create_survey


urlpatterns = [
    path('create/', create_survey, name='create-survey'),
]
