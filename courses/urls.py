# courses/urls.py

from django.urls import path, include
from .views import CourseViewSet, MyCourseListView, EnrollCourseView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
    path('enroll/<int:course_id>', EnrollCourseView.as_view(), name='enroll-course'),
]

