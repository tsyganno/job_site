from django.shortcuts import render


def index(request):
    return render(request, 'job_site_app/index.html')


def vacancies(request):
    return render(request, 'job_site_app/vacancies.html')


def specialization(request):
    return render(request, 'job_site_app/spec.html')


def company(request, id_company: int):
    return render(request, 'job_site_app/company.html')


def vacancy(request, id_vacancy: int):
    return render(request, 'job_site_app/vacancy.html')
