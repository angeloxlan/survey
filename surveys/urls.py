from django.urls import path
from django.http import HttpResponse

from .views import create_survey, preview_survey


urlpatterns = [
    path('survey/create/', create_survey, name='create-survey'),
    path('survey/preview/<slug:slug>/', preview_survey, name='preview-survey'),
]
