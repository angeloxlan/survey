from django.urls import path, include
from django.http import HttpResponse

from .views import create_survey, preview_survey


survey_patterns = [
    path('create/', create_survey, name='create-survey'),
    path('preview/<slug:slug>/', preview_survey, name='preview-survey'),
]

urlpatterns = [
    path('survey/', include(survey_patterns)),
]
