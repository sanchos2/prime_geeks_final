from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('candidates/', views.candidates, name='candidates'),
    path('new_vacancy/', views.new_vacancy, name='new_vacancy'),
    path('vacancy/', views.view_vacancy, name='view_vacancy'),  # TODO pk
    path('video/', views.video, name='video'),
    path('chats/', views.chats, name='chats'),
    path('vacancy/new/', views.vacancy_new, name='vacancy_new'),
]
