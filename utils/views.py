from djqscsv import render_to_csv_response

from recruitment.models import Candidate
from utils.models import Vacancy


def csv_view_vacancies(request):
    """Функция выгрузки данных модели в csv."""
    exported_data = Vacancy.objects.all().values(
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
        'description',
    )
    return render_to_csv_response(exported_data)


def csv_view_resume(request):
    """Функция выгрузки данных модели в csv."""
    exported_data = Candidate.objects.all().values(
        'gender',
        'age',
        'city',
        'ready_to_move',
        'title',
        'salary',
        'branch',
        'spec',
        'type_of_work',
        'work_schedule',
        'total_work_exp',
        'last_employee',
        'last_job_title',
        'last_job_time',
        'skills',
        'about_candidate',
        'education',
        'source',
        'source_id',
        'last_job_responsibilities',
    )
    return render_to_csv_response(exported_data)
