from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from ..forms import (AnswerForm, BaseAnswerFormSet, EditQuestionFormSet, 
    StatusFilter, SortFilter, SurveyForm, QuestionFormSet)
from ..models import Answer, Submission, Survey, Question


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

@login_required
def start_survey(request, slug):
    survey = get_object_or_404(Survey, slug=slug, creator=request.user)

    if not survey.is_active:
        survey.is_active = True
        survey.save()
        return HttpResponseRedirect(reverse(
            'details-survey', kwargs={ 'slug': survey.slug }))

    return HttpResponseRedirect(reverse(
        'preview-survey', kwargs={ 'slug': survey.slug }))

@login_required
def survey_list(request):
    statuses = StatusFilter(request.GET)
    sorting = SortFilter(request.GET)

    request_status = request.GET.get('status')
    request_sorting = request.GET.get('sort')
    request_search = request.GET.get('search')

    if request_status == 'all' or not request_status:
        surveys = Survey.objects.order_by('-created_at')
    elif request_status == 'running':
        surveys = Survey.objects.filter(is_active=True).order_by('-created_at')
    elif request_status == 'inactive':
        surveys = Survey.objects.filter(is_active=False).order_by('-created_at')

    if request_sorting == 'newest':
        surveys = surveys.order_by('-created_at')
    elif request_sorting == 'oldest':
        surveys = surveys.order_by('created_at')

    if request_search:
        surveys = surveys.filter(title__icontains=request_search)

    paginator = Paginator(surveys, 10)

    page_number = request.GET.get('page')
    survey_page = paginator.get_page(page_number)

    context = {
        'surveys': survey_page,
        'statuses': statuses,
        'sorting': sorting,
    }
    return render(request, 'surveys/pages/surveys-list.html', context)

def survey_submission(request, slug):
    survey = get_object_or_404(Survey, slug=slug, is_active=True)
    questions = survey.question_set.order_by('id')

    form_kwargs = { 'questions': questions }

    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)
    if request.method == 'POST':
        question_formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        if question_formset.is_valid():
            with transaction.atomic():
                submission = Submission.objects.create(survey=survey)
                for question in question_formset:
                    Answer.objects.create(
                        option_id=question.cleaned_data['option'], submission=submission)
            
            return HttpResponseRedirect(reverse('thanks-survey'))
    else:
        question_formset = AnswerFormSet(form_kwargs=form_kwargs)
        
    context = {
        'survey': survey,
        'questions': question_formset,
    }
    return render(request, 'surveys/pages/submission.html', context)
