from django.shortcuts import render
from django.views.generic import TemplateView


class CreatePageView(TemplateView):
    template_name = 'surveys/pages/create.html'
