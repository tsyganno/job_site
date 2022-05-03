from django.forms import ModelForm
from django import forms
from job_site_app.models import Company, Vacancy, Application, Resume
from django.forms import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class ResumeForm(forms.ModelForm):

    class Meta:
        model = Resume

        fields = ('name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio')

    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'surname',
                'status',
                'salary',
                'specialty',
                'grade',
                'education',
                'experience',
                'portfolio',
            ),
            ButtonHolder(Submit('submit', 'Сохранить'))
        )


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application

        fields = ('written_username', 'written_phone', 'written_cover_letter')

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'written_username',
                'written_phone',
                'written_cover_letter',
            ),
            ButtonHolder(Submit('submit', 'Отправить отклик'))
        )


class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy

        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max')

    def __init__(self, *args, **kwargs):
        super(VacancyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'specialty',
                'skills',
                'description',
                'salary_min',
                'salary_max',
            ),
            ButtonHolder(Submit('submit', 'Сохранить'))
        )


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = ('name', 'location', 'logo', 'description', 'employee_count')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'location',
                'logo',
                'description',
                'employee_count',
            ),
            ButtonHolder(Submit('submit', 'Сохранить'))
        )
