from django.urls import path, include
from django.http import HttpResponse

from .views import survey


survey_patterns = [
    path('create/', survey.create_survey, name='create-survey'),
    path('preview/<slug:slug>/', survey.preview_survey, name='preview-survey'),
    path('edit/<slug:slug>/', survey.edit_survey, name='edit-survey'),
]

urlpatterns = [
    path('survey/', include(survey_patterns)),
]
