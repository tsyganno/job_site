from django.db.models import Count
from django.views.generic import ListView, DetailView
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views.generic.base import TemplateView

from job_site_app.models import Vacancy, Company, Specialty


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


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
