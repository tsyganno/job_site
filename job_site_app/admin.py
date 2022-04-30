from django.contrib import admin
from job_site_app.models import Vacancy, Company, Specialty, Application


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'skills', 'description', 'salary_min', 'salary_max', 'published_at')
    list_display_links = ('title', 'description')
    search_fields = ('title', 'description',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'logo', 'description', 'employee_count', 'owner')
    list_display_links = ('name', 'description', 'logo')
    search_fields = ('name', 'description',)


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'picture')
    list_display_links = ('code', 'title')
    search_fields = ('code', 'title',)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('written_username', 'written_phone', 'written_cover_letter')
    list_display_links = ('written_username', 'written_phone')
    search_fields = ('written_username', 'written_phone',)


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Application, ApplicationAdmin)
