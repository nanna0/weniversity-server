# courses/urls.py

from django.urls import path, include
from .views import CourseViewSet, EnrollCourseView, CourseLikeView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
    path('enroll/<int:course_id>/', EnrollCourseView.as_view(), name='enroll-course'),
    path('<int:course_id>/like/', CourseLikeView.as_view()),
]

