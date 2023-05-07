from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import SurveyForm, QuestionFormSet
from .models import Survey


@login_required
def create_survey(request):
    survey = Survey()
    if request.method == 'POST':
        survey.creator = request.user
        survey_form = SurveyForm(request.POST, instance=survey)
        question_formset = QuestionFormSet(
            request.POST, instance=survey)

        if all([survey_form.is_valid(), question_formset.is_valid()]):
            survey_form.save()
            question_formset.save()
            return render(request, 'surveys/pages/preview.html')
    else:
        survey_form = SurveyForm(instance=survey)
        question_formset = QuestionFormSet(instance=survey)

    context = {
        'formSurvey': survey_form,
        'formQuestion': question_formset,
    }

    return render(request, 'surveys/pages/create.html', context)
