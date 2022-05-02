from django.shortcuts import render, redirect, reverse
from django.db.models import Count
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


from job_site_app.models import Vacancy, Company, Specialty
from job_site_app.forms import CompanyForm


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')





class EditCompanyCreateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'job_site_app/company-edit.html'
    success_message = 'Информация о компании обновлена!'
    model = Company
    form_class = CompanyForm

    def get_object(self, queryset=None):
        return self.model.objects.get(owner=self.request.user)

    def get_success_url(self):
        pk_user = self.request.user.pk
        company = Company.objects.get(owner_id=pk_user)
        return reverse("job:my_company", kwargs={"name_company": company.name})


class CompanyCreateView(CreateView, LoginRequiredMixin):
    login_url = 'login'
    template_name = 'job_site_app/company-create.html'
    form_class = CompanyForm
    model = Company

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CompanyCreateView, self).form_valid(form)

    def get_success_url(self):
        pk_user = self.request.user.pk
        company = Company.objects.get(owner_id=pk_user)
        return reverse("job:my_company", kwargs={"name_company": company.name})


class LetsstartIndexView(TemplateView, LoginRequiredMixin):
    login_url = 'login'
    template_name = 'job_site_app/company-create.html'


def choice(request, pk: int):
    companies = Company.objects.all()
    for company in companies:
        if company.owner_id == pk:
            name_company = str(''.join(company.name))
            return redirect('job:my_company', name_company=(name_company))
    return redirect('job:letsstart')


class IndexView(TemplateView):
    template_name = 'job_site_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.annotate(count_company=Count('company'))
        context['specialty'] = Specialty.objects.annotate(count_specialty=Count('specialty'))
        return context


class VacancyListView(ListView):
    template_name = 'job_site_app/vacancies.html'
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super(VacancyListView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        return context


class SpecialtyListView(ListView):
    model = Vacancy
    template_name = 'job_site_app/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(SpecialtyListView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(specialty__code=self.kwargs['spec'])
        context['special'] = Specialty.objects.get(code=self.kwargs['spec'])
        return context


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'job_site_app/company.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(company=self.kwargs['pk'])
        return context


class VacancyDetailView(DetailView):
    model = Vacancy
    template_name = 'job_site_app/vacancy.html'
