from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_mission, name='submit_mission'),
    path('results/', views.get_mission_results, name='get_mission_results'),
    path('statistics/', views.get_mission_statistics, name='get_mission_statistics'),
]