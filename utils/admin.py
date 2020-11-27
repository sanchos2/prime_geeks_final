from django.contrib import admin

from utils.models import Vacancy


class VacancyAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'salary_value',
        'salary_left_value',
        'salary_right_value',
        'job_format',
        'candidate_level',
        'employer_type',
        'employer_name',
        'location_city',
        'location_country',
    ]
    list_per_page = 40
    search_fields = ['source_id']


admin.site.register(Vacancy, VacancyAdmin)
