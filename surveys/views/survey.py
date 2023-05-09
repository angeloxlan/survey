from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from ..forms import SurveyForm, QuestionFormSet
from ..models import Survey


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
            return HttpResponseRedirect(reverse(
                'preview-survey', kwargs={ 'slug': survey.slug }))
    else:
        survey_form = SurveyForm(instance=survey)
        question_formset = QuestionFormSet(instance=survey)

    context = {
        'formSurvey': survey_form,
        'formQuestion': question_formset,
    }

    return render(request, 'surveys/pages/create.html', context)

@login_required
def preview_survey(request, slug):
    survey = get_object_or_404(Survey, slug=slug, creator=request.user)

    if survey.is_active:
        return HttpResponseRedirect(reverse(
            'details-survey', kwargs={ 'slug': survey.slug }))

    context = {
        'survey': survey,
    }
    return render(request, 'surveys/pages/preview.html', context)
