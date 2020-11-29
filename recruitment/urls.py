from django.urls import path

from recruitment import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vacancies/', views.vacancies, name='vacancies'),
    path('candidates/', views.candidates, name='candidates'),
    path('new_vacancy/', views.new_vacancy, name='new_vacancy'),
    path('vacancy/', views.view_vacancy, name='view_vacancy'),
    path('video/', views.video, name='video'),
    path('chats/', views.chats, name='chats'),
]
