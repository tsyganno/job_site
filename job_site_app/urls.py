from django.urls import path
from job_site_app.views import IndexView, SpecialtyListView, CompanyDetailView, VacancyDetailView, VacancyListView, \
    choice, let_sstart, my_company, create, CompanyCreateView


app_name = 'job'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('vacancies/', VacancyListView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:spec>/', SpecialtyListView.as_view(), name='specialization'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company'),
    path('vacancies/<int:pk>/', VacancyDetailView.as_view(), name='vacancy'),
    path('vacancies/<int:pk>/', VacancyDetailView.as_view(), name='vacancy'),
    path('mycompany/choice/<int:pk>/', choice, name='choice'),
    path('mycompany/letsstart/', let_sstart, name='let_sstart'),
    path('mycompany/create/', CompanyCreateView.as_view(), name='add_company'),
    path('mycompany/', my_company, name='my_company'),
]
