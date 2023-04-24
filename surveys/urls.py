from django.urls import path
from django.http import HttpResponse

from .views import CreatePageView


urlpatterns = [
    path('create/', CreatePageView.as_view(), name='create-form'),
]
