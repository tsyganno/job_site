from django.urls import path
from .views import index, vacancies, specialization, company, vacancy


urlpatterns = [
    path('', index, name='index'),
    path('vacancies/', vacancies, name='vacancies'),
    path('vacancies/cat/frontend/', specialization, name='specialization'),
    path('companies/<int:id_company>/', company, name='company'),
    path('vacancies/<int:id_vacancy>/', vacancy, name='vacancy'),
]