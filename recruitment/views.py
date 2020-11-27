from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def vacancies(requests):
    return render(requests, 'vacancies.html')


def candidates(requests):
    return render(requests, 'candidates.html')


def new_vacancy(requests):
    return render(requests, 'new_vacancy.html')


def view_vacancy(requests):  # TODO pk
    return render(requests, 'vacancy_view.html')


def video(requests):
    return render(requests, 'video.html')


def chats(requests):
    return render(requests, 'chats.html')
