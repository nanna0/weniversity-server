# import django_filters 
# from .models import Course

# class CourseFilter(django_filters.FilterSet):
#     """강의 필터 클래스"""

# # 텍스트 검색 (부분 일치)
#     title = django_filters.CharFilter(
#         lookup_expr='icontains', 
#         help_text="강의 제목으로 검색"
#     )
#     instructor = django_filters.CharFilter(
#         lookup_expr='icontains',
#         help_text="강사명으로 검색"
#     )

# # 숫자 범위 필터
#     price_min = django_filters.NumberFilter(
#         field_name='price', 
#         lookup_expr='gte',
#         help_text="최소 가격"
#     )
#     price_max = django_filters.NumberFilter(
#         field_name='price', 
#         lookup_expr='lte',
#         help_text="최대 가격"
#     )

# # 날짜 범위 필터
#     created_after = django_filters.DateTimeFilter(
#         field_name='created_at', 
#         lookup_expr='gte',
#         help_text="생성일 이후"
#     )

#     class Meta:
#         model = Course
#         fields = {
#             'category': ['exact', 'in'],  # 정확히 일치 또는 목록에서 선택
#             'level': ['exact', 'in'],
#             'is_active': ['exact'],
#         }
