from django.contrib import admin

from recruitment.models import Candidate, Language

class CandidateAdmin(admin.ModelAdmin):
    list_display = ['title', 'salary']
    list_per_page = 40

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Language)
