from django.urls import path
from job_site_app.views import IndexView, SpecialtyListView, CompanyDetailView, VacancyListView, \
    choice, LetsstartIndexView, CompanyCreateView, EditCompanyCreateView, UserVacancyIndexView, getting_information, \
    StartVacancyIndexView, VacancyCreateView, EditVacancyCreateView, CheckView, ApplicationCreateView


app_name = 'job'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('send/', CheckView.as_view(), name='send'),
    path('vacancies/', VacancyListView.as_view(), name='vacancies'),
    path('vacancies/cat/<str:spec>/', SpecialtyListView.as_view(), name='specialization'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company'),
    path('vacancies/<int:pk>/', ApplicationCreateView.as_view(), name='vacancy'),
    path('mycompany/choice/<int:pk>/', choice, name='choice'),
    path('mycompany/letsstart/', LetsstartIndexView.as_view(), name='letsstart'),
    path('mycompany/create/', CompanyCreateView.as_view(), name='add_company'),
    path('mycompany/vacancies/create/', StartVacancyIndexView.as_view(), name='start_vacancy'),
    path('mycompany/vacancies/', UserVacancyIndexView.as_view(), name='user_vacancies'),
    path('mycompany/getting_information_about_vacancies/<int:pk>/', getting_information, name='getting_information'),
    path('mycompany/<str:name_company>/', EditCompanyCreateView.as_view(), name='my_company'),
    path('mycompany/vacancies/create/vacancy', VacancyCreateView.as_view(), name='add_vacancy'),
    path('mycompany/vacancies/<int:pk>/', EditVacancyCreateView.as_view(), name='edit_vacancy'),

]
