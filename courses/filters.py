# courses/filters.py
import django_filters
from django.db.models import Q, Value
from django.db.models.functions import Lower, Replace
from .models import Course, Enrollment

def _to_list(value):
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        items = value
    else:
        items = str(value).split(",")
    return [v.strip() for v in items if str(v).strip()]

class IContainsAnyFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """부분 일치(icontains), 쉼표/반복 파라미터 OR"""
    def filter(self, qs, value):
        terms = _to_list(value)
        if not terms:
            return qs
        q = Q()
        for t in terms:
            q |= Q(**{f"{self.field_name}__icontains": t})
        return qs.filter(q)

class NormalizedIExactAnyFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    """
    공백 제거 + 소문자 정규화 후 정확 일치, 쉼표/반복 파라미터 OR
    예: '데이터 분석' == '데이터분석'
    """
    def filter(self, qs, value):
        vals = _to_list(value)
        if not vals:
            return qs
        alias = f"norm_{self.field_name}"  # '__' 금지
        qs = qs.annotate(**{
            alias: Replace(Lower(self.field_name), Value(" "), Value(""))
        })
        cond = Q()
        for v in vals:
            cond |= Q(**{alias: v.lower().replace(" ", "")})
        return qs.filter(cond)

class CourseFilter(django_filters.FilterSet):
    # title: 부분 일치 다중(OR)
    title = IContainsAnyFilter(field_name="title")

    # category/type/level: 공백무시 정확 일치 다중(OR)
    category = NormalizedIExactAnyFilter(field_name="category")
    type     = NormalizedIExactAnyFilter(field_name="type")
    level    = NormalizedIExactAnyFilter(field_name="level")

    # price_type: free(=0), paid(>0), gov(<0) 다중(OR)
    price_type = django_filters.CharFilter(method="filter_price_type")

    def filter_price_type(self, qs, name, value):
        kinds = _to_list(value)
        if not kinds:
            return qs
        cond = Q()
        for k in kinds:
            k = k.lower()
            if k == "free":
                cond |= Q(price=0)
            elif k == "paid":
                cond |= Q(price__gt=0)
            elif k == "gov":
                cond |= Q(price__lt=0)
        return qs.filter(cond)

    class Meta:
        model = Course
        fields = []  # 커스텀 정의만 사용

class MyCourseFilter(django_filters.FilterSet):

    # category/type/level: 공백무시 정확 일치 다중(OR)
    status = NormalizedIExactAnyFilter(field_name="status")
    type = NormalizedIExactAnyFilter(field_name="course__type")

    class Meta:
        model = Enrollment
        fields = ["user", "course", "status", "type", "progress"]