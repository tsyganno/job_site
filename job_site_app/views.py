from django.shortcuts import render, redirect, reverse
from django.db.models import Count
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.db.models import Q

from job_site_app.models import Vacancy, Company, Specialty, Application, Resume
from job_site_app.forms import CompanyForm, VacancyForm, ApplicationForm, ResumeForm


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')


class SearchView(LoginRequiredMixin, ListView, View):
    login_url = 'accounts:login'
    template_name = 'job_site_app/search.html'

    def get(self, request):
        query = self.request.GET.get('q')
        object_list = Vacancy.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        context = {'object_list': object_list, 'query': query}
        return render(request, self.template_name, context)


def availability(request, pk: int):
    user_resume = Resume.objects.filter(owner_id=pk)
    if len(user_resume) > 0:
        return redirect('job:my_resume')
    return redirect('job:letsstart_resume')


class EditResumeCreateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/resume-edit.html'
    success_message = 'Информация обновлена!'
    model = Resume
    form_class = ResumeForm

    def get_object(self, queryset=None):
        return self.model.objects.get(owner=self.request.user)

    def get_success_url(self):
        return reverse("job:my_resume")


class ResumeCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/resume-create.html'
    form_class = ResumeForm
    model = Resume

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(ResumeCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("job:my_resume")


class LetsstartResumeIndexView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/resume-create.html'


class CheckView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/send.html'


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/vacancy.html'
    form_class = ApplicationForm
    model = Application

    def get_context_data(self, **kwargs):
        context = super(ApplicationCreateView, self).get_context_data(**kwargs)
        context['vacancy'] = Vacancy.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.vacancy = Vacancy.objects.get(id=self.kwargs['pk'])
        return super(ApplicationCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("job:send")


class EditVacancyCreateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/vacancy-edit.html'
    success_message = 'Информация о вакансии обновлена!'
    model = Vacancy
    form_class = VacancyForm

    def get_context_data(self, **kwargs):
        context = super(EditVacancyCreateView, self).get_context_data(**kwargs)
        context['user_company'] = str(Vacancy.objects.get(id=self.kwargs['pk']).title)
        context['applications'] = Application.objects.filter(vacancy=self.kwargs['pk'])
        return context

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['pk'])

    def get_success_url(self):
        vacancy = Vacancy.objects.get(id=self.kwargs['pk'])
        return reverse("job:edit_vacancy", kwargs={"pk": vacancy.pk})


class VacancyCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/vacancy-create.html'
    form_class = VacancyForm
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super(VacancyCreateView, self).get_context_data(**kwargs)
        pk_user = self.request.user.pk
        context['user_company'] = str(Company.objects.filter(owner_id=pk_user).first().name)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.company = Company.objects.filter(owner_id=self.request.user.pk).first()
        return super(VacancyCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("job:user_vacancies")


class UserVacancyIndexView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/vacancy-list.html'

    def get_context_data(self, **kwargs):
        context = super(UserVacancyIndexView, self).get_context_data(**kwargs)
        pk_user = self.request.user.pk
        context['user_company'] = str(Company.objects.filter(owner_id=pk_user).first().name)
        context['user_vacancies'] = \
            Vacancy.objects.filter(company__owner_id=pk_user).annotate(count_application=Count('applications'))
        return context


def getting_information(request, pk: int):
    user_vacancies = Vacancy.objects.filter(company__owner_id=pk)
    if len(user_vacancies) > 0:
        return redirect('job:user_vacancies')
    return redirect('job:start_vacancy')


class StartVacancyIndexView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/vacancy-create.html'

    def get_context_data(self, **kwargs):
        context = super(StartVacancyIndexView, self).get_context_data(**kwargs)
        pk_user = self.request.user.pk
        context['user_company'] = str(Company.objects.filter(owner_id=pk_user).first().name)
        return context


class EditCompanyCreateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'accounts:login'
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


class CompanyCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:login'
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


class LetsstartIndexView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:login'
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


class VacancyListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    template_name = 'job_site_app/vacancies.html'
    model = Vacancy

    def get_context_data(self, **kwargs):
        context = super(VacancyListView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.all()
        return context


class SpecialtyListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = Vacancy
    template_name = 'job_site_app/vacancies.html'

    def get_context_data(self, **kwargs):
        context = super(SpecialtyListView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(specialty__code=self.kwargs['spec'])
        context['special'] = Specialty.objects.get(code=self.kwargs['spec'])
        return context


class CompanyDetailView(LoginRequiredMixin, DetailView):
    login_url = 'accounts:login'
    model = Company
    template_name = 'job_site_app/company.html'

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)
        context['vacancies'] = Vacancy.objects.filter(company=self.kwargs['pk'])
        return context
