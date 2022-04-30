from django.forms import ModelForm
from django import forms
from job_site_app.models import Company
from django.forms import TextInput


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company

        fields = ('name', 'location', 'logo', 'description', 'employee_count')

