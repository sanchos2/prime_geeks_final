from django.urls import path

from utils import views

urlpatterns = [
    path('vacancies/', views.csv_view_vacancies, name='csv_view_vacancies'),
    path('resume/', views.csv_view_resume, name='csv_view_resume'),
]
