# courses/views.py
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Course, Chapter, Video, Instructor
from .serializers import CourseSerializer
from .filters import CourseFilter

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
