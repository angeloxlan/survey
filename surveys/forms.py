from django.forms import ModelForm, Textarea, inlineformset_factory, ValidationError
from django.forms.models import BaseInlineFormSet
from django.forms.utils import ErrorDict
from .models.option import Option
from .models.question import Question
from .models.survey import Survey


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description']
        labels = {
            'title': 'Survey title',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = 'Survey'
        self.fields['description'].widget.attrs['rows'] = 3
        self.fields['description'].widget.attrs['placeholder'] = 'Description'


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        labels = {
            'text': 'Question',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Question'
        self.fields['text'].widget.attrs['required'] = True

    def is_valid(self):
        super().is_valid()
        self._errors = ErrorDict()
        for name, field in self.fields.items():
            if name != 'text':
                continue
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(
                    self.data, self.files, self.add_prefix(name))
            try:
                value = field.clean(value)
                self.cleaned_data[name] = value
            except ValidationError as e:
                self._errors[name] = self.error_class([e])

        return self.is_bound and not self.errors


class OptionForm(ModelForm):
    class Meta:
        model = Option
        fields = ['text']
        labels = {
            'text': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['placeholder'] = 'Option'
        self.fields['text'].widget.attrs['required'] = True

    def is_valid(self):
        super().is_valid()
        self._errors = ErrorDict()
        for name, field in self.fields.items():
            if name != 'text':
                continue
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(
                    self.data, self.files, self.add_prefix(name))
            try:
                value = field.clean(value)
                self.cleaned_data[name] = value
            except ValidationError as e:
                self._errors[name] = self.error_class([e])

        return self.is_bound and not self.errors


class BaseQuestionFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseQuestionFormSet, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.options = OptionFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='%s-%s' % (
                form.prefix,
                OptionFormSet.get_default_prefix()),
        )

    def is_valid(self):
        form_valid = True
        if self.is_bound:
            for form in self.forms:
                form_valid &= form.is_valid()
                form.clean()
                if hasattr(form, 'options'):
                    form_valid &= form.options.is_valid()

        return form_valid

    def save(self, commit=True):
        result = super().save(commit=commit)
        for form in self.forms:
            if hasattr(form, 'options'):
                if not self._should_delete_form(form):
                    form.options.save(commit=commit)

        return result

    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__q_prefix__'),
            empty_permitted=True,
            use_required_attribute=False,
            **self.get_form_kwargs(None)
        )
        self.add_fields(form, None)
        return form


class BaseOptionFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseOptionFormSet, self).__init__(*args, **kwargs)

    def is_valid(self):
        form_valid = True
        if self.is_bound:
            for form in self.forms:
                form_valid &= form.is_valid()
                form.clean()

        return form_valid

    @property
    def empty_form(self):
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__o_prefix__'),
            empty_permitted=True,
            use_required_attribute=False,
            **self.get_form_kwargs(None)
        )
        self.add_fields(form, None)
        return form


QuestionFormSet = inlineformset_factory(
    Survey,
    Question,
    form=QuestionForm,
    formset=BaseQuestionFormSet,
    extra=1,
    can_delete=False,
)

OptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=OptionForm,
    formset=BaseOptionFormSet,
    can_delete=False,
    extra=1,
)


class EditBaseQuestionFormSet(BaseQuestionFormSet):
    def __init__(self, *args, **kwargs):
        super(EditBaseQuestionFormSet, self).__init__(*args, **kwargs)

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.options = EditOptionFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='%s-%s' % (
                form.prefix,
                EditOptionFormSet.get_default_prefix()),
        )


EditQuestionFormSet = inlineformset_factory(
    Survey,
    Question,
    form=QuestionForm,
    formset=EditBaseQuestionFormSet,
    extra=0,
    can_delete=True,
)

EditOptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=OptionForm,
    formset=BaseOptionFormSet,
    can_delete=True,
    extra=0,
)