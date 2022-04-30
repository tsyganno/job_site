from django.shortcuts import render, redirect
from django.db.models import Count
from django.views.generic import ListView, DetailView
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


def my_company(request):
    return render(request, 'job_site_app/company-edit.html')


def create(request):
    return render(request, 'job_site_app/company-edit.html')


class CompanyCreateView(CreateView):
    template_name = 'job_site_app/company-create.html'
    form_class = CompanyForm
    success_url = reverse_lazy('job:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CompanyCreateView, self).form_valid(form)


def let_sstart(request):
    return render(request, 'job_site_app/company-create.html')


def choice(request, pk: int):
    companies = Company.objects.all()
    for company in companies:
        if company.owner_id == pk:
            return redirect('job:my_company')
    return redirect('job:let_sstart')


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
