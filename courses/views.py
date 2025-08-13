# courses/views.py
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from .models import Course, Chapter, Video, Instructor, Enrollment, CourseLike
from .serializers import CourseSerializer, MyCourseSerializer, MyLikedCourseSerializer
from .filters import CourseFilter
from django.db import transaction
from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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
    
class EnrollCourseView(APIView):
    """수강신청: 이미 있으면 ACTIVE로 전환(멱등)"""
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, course_id:int):
        course = get_object_or_404(Course, pk=course_id, is_active=True)

        # 이미 Enrollment가 있으면 상태만 ACTIVE로 갱신, 없으면 생성
        enr, created = Enrollment.objects.update_or_create(
            user=request.user,
            course=course,
            defaults={
                'status': Enrollment.Status.ACTIVE,
                'expired_at': None,  # 재활성화 시 만료 초기화
            }
        )

        return Response(
            {
                'enrollment_id': enr.id,           # Enrollment의 PK (자동 생성)
                'course_id': course.course_id,
                'is_enrolled': True,
                'status': enr.status,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    
class CourseLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request, course_id:int):
        """좋아요 (멱등). 이미 있으면 그대로 200."""
        course = get_object_or_404(Course, pk=course_id, is_active=True)
        like, created = CourseLike.objects.get_or_create(user=request.user, course=course)
        return Response(
            {'course_id': course.course_id, 'is_liked': True},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    @transaction.atomic
    def delete(self, request, course_id:int):
        """좋아요 취소 (행 삭제)"""
        course = get_object_or_404(Course, pk=course_id)
        CourseLike.objects.filter(user=request.user, course=course).delete()
        return Response({'course_id': course.course_id, 'is_liked': False}, status=status.HTTP_200_OK)
    
class MyLikedCoursesView(generics.ListAPIView):
    """GET /api/users/mypage/likes  -> 내가 좋아요한 코스 리스트"""
    serializer_class = MyLikedCourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (CourseLike.objects
                .filter(user=self.request.user)
                .select_related('course')
                .order_by('-created_at'))