from django.urls import path
from .views import IndexView, SpecialtyDetailView, CompanyDetailView, VacancyDetailView, VacancyListView


app_name = 'job'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('vacancies/', VacancyListView.as_view(), name='vacancies'),
    path('vacancies/cat/frontend/<int:pk>/', SpecialtyDetailView.as_view(), name='specialization'),
    path('companies/<int:pk>/', CompanyDetailView.as_view(), name='company'),
    path('vacancies/<int:pk>/', VacancyDetailView.as_view(), name='vacancy'),
]
