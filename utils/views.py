from django.shortcuts import render
from utils.models import Vacancy
from djqscsv import render_to_csv_response


def csv_view(request):
    qs = Vacancy.objects.all().values(
        'title',
        'published_at',
        'source_id',
        'employer_type',
        'employer_name',
        'location_city',
        'location_country',
        'salary_currency',
        'salary_value',
        'salary_left_value',
        'salary_right_value',
        'job_format',
        'candidate_level',
        'specialization',
        'branch',
        'source',
        'description'
    )
    return render_to_csv_response(qs)
