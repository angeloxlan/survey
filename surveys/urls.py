from django.urls import path, include
from django.http import HttpResponse

from .views import survey


survey_patterns = [
    path('create/', survey.create_survey, name='create-survey'),
    path('preview/<slug:slug>/', survey.preview_survey, name='preview-survey'),
    path('edit/<slug:slug>/', survey.edit_survey, name='edit-survey'),
    path('detail/<slug:slug>/', survey.details_survey, name='details-survey'),
    path('start/<slug:slug>/', survey.start_survey, name='start-survey'),
]

urlpatterns = [
    path('survey/', include(survey_patterns)),
    path('surveys/', survey.survey_list, name='list-surveys'),
    path('thanks/<str:survey_title>', survey.ThankSubmission.as_view(), name='thanks-survey'),
    path('<slug:slug>/', survey.survey_submission, name='submission-survey'),
]
