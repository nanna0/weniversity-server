# courses/urls.py

from django.urls import path, include
from .views import CourseViewSet, MyCourseListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
]

