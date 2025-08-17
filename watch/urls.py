from django.urls import path
from . import views


urlpatterns = [
    #프로젝트
    path('watch-progress/save/', views.watch_progress_upsert),
    
    # 코스별 진행률 조회
    path('watch-progress/<str:user_id>/<int:video_id>/', views.watch_progress_by_course),
    path('watch-progress-all/<str:user_id>/<int:video_id>/', views.watch_progress_by_course_all),
    path('watch-progress-detail/<str:user_id>/<int:video_id>/<int:chapter_id>/', views.watch_progress_detail),
    path('create-watch-progress/', views.create_watch_progress),
    path('create-next-video/', views.create_next_video),
    # path('watch-progress-upsert/', views.watch_progress_upsert),
]