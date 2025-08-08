# courses/urls.py

from django.urls import path
from .views import CourseListView

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    #path('<int:pk>/', CourseListView.as_view(), name='course-detail'),    

]
#    list: GET /api/courses/ - 강의 목록 조회
#     create: POST /api/courses/ - 강의 생성
#     retrieve: GET /api/courses/{id}/ - 특정 강의 조회
#     update: PUT /api/courses/{id}/ - 강의 전체 수정
#     partial_update: PATCH /api/courses/{id}/ - 강의 부분 수정
#     destroy: DELETE /api/courses/{id}/ - 강의 삭제