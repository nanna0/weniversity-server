# courses/views.py
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Course, Chapter, Video, Instructor, Enrollment
from .serializers import CourseSerializer, MyCourseSerializer
from .filters import CourseFilter
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

class CourseViewSet(ReadOnlyModelViewSet):
    serializer_class = CourseSerializer
    filterset_class = CourseFilter

    def get_queryset(self):
        return (
            Course.objects.filter(is_active=True)
            .prefetch_related(
                Prefetch("chapters", queryset=Chapter.objects.order_by("order_index", "chapter_id")),
                Prefetch("videos", queryset=Video.objects.order_by("order_index", "video_id")),
                Prefetch("instructors", queryset=Instructor.objects.order_by("name")),
            )
            .order_by("order_index", "course_id")
        )
    
class MyCourseListView(generics.ListAPIView):
    serializer_class = MyCourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']               # ?status=active
    search_fields = ['course__title']           # ?search=파이썬
    ordering_fields = ['enrolled_at', 'course__title']  # ?ordering=-enrolled_at
    ordering = ['-enrolled_at']                 # 기본 최신 등록순

    def get_queryset(self):
        return (Enrollment.objects
                .filter(user=self.request.user)
                .select_related('course')       # N+1 방지
                )
    
class MyCourseListView(generics.ListAPIView):
    serializer_class = MyCourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']               # ?status=active
    search_fields = ['course__title']           # ?search=파이썬
    ordering_fields = ['enrolled_at', 'course__title']  # ?ordering=-enrolled_at
    ordering = ['-enrolled_at']                 # 기본 최신 등록순

    def get_queryset(self):
        return (Enrollment.objects
                .filter(user=self.request.user)
                .select_related('course')       # N+1 방지
                )