from django import forms

from recruitment.models import VacancyRequest


class VacancyForm(forms.ModelForm):

    class Meta:
        model = VacancyRequest
        fields = (
            'title',
            'teaser',
            'description',
            'level',
            'salary_min',
            'salary_max',
            'hard_requirements',
            'working_conditions'
        )
