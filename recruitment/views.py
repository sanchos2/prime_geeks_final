from django.shortcuts import render, redirect, get_object_or_404

from recruitment.forms import VacancyForm
from recruitment.models import Candidate, VacancyRequest


def index(request):
    """Рендеринг главной страницы."""
    return render(request, 'index.html')


def vacancies(requests):
    """Рендеринг списка вакансий."""
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
    """Рендеринг списка кандидатов."""
    all_candidates = Candidate.objects.all().order_by('ratings')[:10]
    candidates_list = []
    for candidate in all_candidates:
        candidates_list.append({
            'name': candidate.title,
            'rating': candidate,
            'social': candidate,
            'response_date': '10-11-2020',
            'recommended_vacancy': get_object_or_404(VacancyRequest, pk=1),
            'contacts': 'elisey.fedorov@gmail.com',
        })
    return render(requests, 'candidates.html', context={'candidates': candidates_list})


def view_vacancy(requests):
    """Рендеринг описания вакансии."""
    return render(requests, 'vacancy_view.html')


def video(requests):
    """Рендеринг видео."""
    return render(requests, 'video.html')


def chats(requests):
    """Рендеринг чата."""
    return render(requests, 'chats.html')


def new_vacancy(request):
    """Обработка формы новой вакансии."""
    if request.method == 'POST':
        form = VacancyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vacancies')
    else:
        form = VacancyForm()
    return render(request, 'new_vacancy.html', {'form': form})
