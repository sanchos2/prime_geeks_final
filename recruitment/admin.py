from django.contrib import admin

from recruitment.models import Candidate, Language
from recruitment.models import Level, HardRequirements, Rating, SoftRequirements, Specialization, VacancyRequest


class RatingInline(admin.TabularInline):
    model = Rating


class CandidateAdmin(admin.ModelAdmin):
    """Кастомизация админки."""

    list_display = ['title', 'get_skill', 'get_social', 'salary']
    search_fields = ['source_id', 'title']
    inlines = [RatingInline]
    list_per_page = 40

    def get_skill(self, obj):
        """Вывод поля skill модели Rating"""
        return obj.ratings.skill

    get_skill.short_description = 'Skill'

    def get_social(self, obj):
        """Вывод поля social модели Rating"""
        return obj.ratings.social

    get_skill.short_description = 'Social'


admin.site.register(Level)
admin.site.register(Rating)
admin.site.register(SoftRequirements)
admin.site.register(HardRequirements)
admin.site.register(Specialization)
admin.site.register(VacancyRequest)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Language)
