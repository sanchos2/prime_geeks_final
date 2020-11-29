from django.contrib import admin

from recruitment.models import Candidate, Language
from recruitment.models import Level, HardRequirements, SoftRequirements, Specialization, VacancyRequest


class CandidateAdmin(admin.ModelAdmin):
    """Кастомизация админки."""

    list_display = ['title', 'salary']
    search_fields = ['source_id']
    list_per_page = 40


admin.site.register(Level)
admin.site.register(SoftRequirements)
admin.site.register(HardRequirements)
admin.site.register(Specialization)
admin.site.register(VacancyRequest)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Language)
