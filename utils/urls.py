from django.urls import path


from . import views

urlpatterns = [
    path('', views.csv_view, name='csv_view'),
]