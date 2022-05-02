from django.forms import ModelForm
from django import forms
from job_site_app.models import Company
from django.forms import TextInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


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
