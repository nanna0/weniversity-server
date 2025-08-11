# courses/views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Course
from .serializers import CourseSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Count
from .filters import CourseFilter

class CourseViewSet(viewsets.ModelViewSet):
    
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    # 필터링, 검색, 정렬 백엔드 설정
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['title', 'description', 'instructor']  # 검색 가능한 필드
    ordering_fields = ['price', 'duration', 'created_at', 'title']  # 정렬 가능한 필드
    ordering = ['order_index', '-created_at']  # 기본 정렬 (최신순)

    def get_queryset(self):
        """
        QuerySet 커스터마이징
        - 요청에 따른 동적 필터링 적용
        """
        print("🔍 get_queryset 호출됨")
        queryset = Course.objects.select_related().prefetch_related()
        
        # 활성화된 강의만 조회하는 파라미터
        active_only = self.request.query_params.get('active_only', 'false')
        if active_only.lower() == 'true':
            queryset = queryset.filter(is_active=True)
            print(f"✅ 활성화된 강의만 필터링: {queryset.count()}개")
        
        # 카테고리별 필터링
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__iexact=category)
            print(f"📂 카테고리 필터링 ({category}): {queryset.count()}개")

        # 타입별 필터링
        type = self.request.query_params.get('type')
        if type:
            queryset = queryset.filter(type__iexact=type)
            print(f"타입별 필터링 ({type}): {queryset.count()}개")

        # 레벨별 필터링
        level = self.request.query_params.get('level')
        if level:
            queryset = queryset.filter(level__iexact=level)
            print(f"레벨별 필터링 ({level}): {queryset.count()}개")
        
        # 가격별 필터링
        price = self.request.query_params.get('price')
        if price:
            queryset = queryset.filter(price__iexact=price)
            print(f"가격별 필터링 ({level}): {queryset.count()}개")

        # # 가격 범위 필터링
        # min_price = self.request.query_params.get('min_price')
        # max_price = self.request.query_params.get('max_price')
        
        # if min_price:
        #     queryset = queryset.filter(price__gte=min_price)
        #     print(f"💰 최소 가격 필터링 ({min_price}원 이상): {queryset.count()}개")
            
        # if max_price:
        #     queryset = queryset.filter(price__lte=max_price)
        #     print(f"💰 최대 가격 필터링 ({max_price}원 이하): {queryset.count()}개")
        
        # print(f"📊 최종 QuerySet: {queryset.count()}개 강의")
        # return queryset
    
    def list(self, request, *args, **kwargs):
        """
        강의 목록 조회 메서드 오버라이드
        - 요청 로깅 및 커스텀 응답 처리
        """
        print(f"📋 LIST 요청 받음")
        print(f"🔗 요청 URL: {request.build_absolute_uri()}")
        print(f"📝 쿼리 파라미터: {dict(request.query_params)}")
        
        # 부모 클래스의 list 메서드 호출
        response = super().list(request, *args, **kwargs)
        
        # 응답에 메타데이터 추가
        if isinstance(response.data, dict) and 'results' in response.data:
            response.data['meta'] = {
                'total_count': response.data.get('count', 0),
                'filters_applied': dict(request.query_params),
                'message': '강의 목록을 성공적으로 조회했습니다.'
            }
        
        print(f"✅ LIST 응답 완료: {len(response.data.get('results', []))}개 항목")
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """특정 강의 상세 조회"""
        print(f"🔍 RETRIEVE 요청: ID {kwargs.get('pk')}")
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """새 강의 생성"""
        print(f"➕ CREATE 요청: {request.data}")
        return super().create(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """
        인기 강의 조회 (커스텀 액션)
        URL: GET /api/courses/popular/
        """
        print("🔥 인기 강의 조회 요청")
        
        # 인기 강의 로직 (예: 가격이 낮고 활성화된 강의)
        popular_courses = self.get_queryset().filter(
            is_active=True,
            price__lte=100000
        ).order_by('price', '-created_at')[:10]
        
        serializer = self.get_serializer(popular_courses, many=True)
        
        return Response({
            'message': '인기 강의 목록입니다.',
            'count': popular_courses.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def categories(self, request):
        """
        카테고리 목록 조회
        URL: GET /api/courses/categories/
        """
        print("📂 카테고리 목록 조회 요청")
        
        categories = Course.objects.values('category').annotate(
            count=Count('id')
        ).order_by('category')
        
        return Response({
            'message': '카테고리 목록입니다.',
            'categories': list(categories)
        })
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """
        강의 활성화/비활성화 토글
        URL: POST /api/courses/{id}/toggle_active/
        """
        print(f"🔄 강의 {pk} 활성화 상태 토글 요청")
        
        course = self.get_object()
        course.is_active = not course.is_active
        course.save()
        
        serializer = self.get_serializer(course)
        
        return Response({
            'message': f'강의가 {"활성화" if course.is_active else "비활성화"}되었습니다.',
            'course': serializer.data
        })