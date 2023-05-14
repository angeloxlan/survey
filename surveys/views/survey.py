from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from ..forms import SurveyForm, QuestionFormSet, EditQuestionFormSet
from ..models import Submission, Survey, Question


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

@login_required
def edit_survey(request, slug):
    survey = get_object_or_404(Survey, slug=slug, creator=request.user)

    if survey.is_active:
        return HttpResponseRedirect(reverse(
            'details-survey', kwargs={ 'slug': survey.slug }))

    if request.method == 'POST':
        survey_form = SurveyForm(request.POST or None, instance=survey)
        question_formset = EditQuestionFormSet(
            request.POST or None, instance=survey,
            queryset=Question.objects.filter(survey=survey).order_by('id'))

        if all([survey_form.is_valid(), question_formset.is_valid()]):
            survey_form.save()
            question_formset.save()
            return HttpResponseRedirect(reverse(
                'preview-survey', kwargs={ 'slug': survey.slug }))
    else:
        survey_form = SurveyForm(instance=survey)
        question_formset = EditQuestionFormSet(
            instance=survey,
            queryset=Question.objects.filter(survey=survey).order_by('id'))

    context = {
        'survey': survey,
        'formSurvey': survey_form,
        'formQuestion': question_formset,
    }

    return render(request, 'surveys/pages/edit.html', context)

@login_required
def details_survey(request, slug):
    survey = get_object_or_404(Survey, slug=slug, creator=request.user)

    if not survey.is_active:
        return HttpResponseRedirect(reverse(
            'preview-survey', kwargs={ 'slug': survey.slug }))

    total_submissions = Submission.objects.filter(survey=survey).count()
    host = request.get_host()
    # public_path = reverse('public-survey', kwargs={ 'slug': survey.slug })
    public_url = f'{request.scheme}://{host}'
    context = {
        'public_url': public_url,
        'survey': survey,
        'total_submissions': total_submissions,
    }
    return render(request, 'surveys/pages/detail.html', context)
