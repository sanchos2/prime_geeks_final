from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from recruitment.forms import VacancyForm
from recruitment.models import Candidate, VacancyRequest


def index(request):
    return render(request, 'index.html')


def vacancies(requests):
    all_vacancies = VacancyRequest.objects.all()
    vacancies_list = []
    for vacancy in all_vacancies:
        vacancies_list.append({
            'name': vacancy.title,
            'level': vacancy.level.name,
            'direction': 'Аналитика',
            'department': 'Финансовый департамент',
            'published_at': vacancy.published_at,
            'status': 1,
        })

    return render(requests, 'vacancies.html', context={'vacancies': vacancies_list})


def candidates(requests):
    all_candidates = Candidate.objects.all()
    candidates = []
    for candidate in all_candidates:
        candidates.append({
            'name': candidate.title,
            'raiting': 6,
            'social': 'OK',
            'response_date': '10-11-2020',
            'recommended_vacancy': get_object_or_404(VacancyRequest, pk=1),
            'contacts': 'elisey.fedorov@gmail.com',
        })
    return render(requests, 'candidates.html', context={'candidates': candidates})


def new_vacancy(requests):
    return render(requests, 'new_vacancy.html')


def view_vacancy(requests):  # TODO pk
    return render(requests, 'vacancy_view.html')


def video(requests):
    return render(requests, 'video.html')


def chats(requests):
    return render(requests, 'chats.html')


def new_vacancy(request):

    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacancies')
    else:
        form = VacancyForm()
    return render(request, 'new_vacancy.html', {'form': form})
