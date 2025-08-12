# courses/models.py
#import uuid
from django.db import models

class Course(models.Model):
    class Type(models.TextChoices):
        BOOST = 'boost', '부스트'
        VOD = 'vod', '일반'

    class Level(models.TextChoices):
        A = "초급"
        B = "중급"
        C = "실무"

    class Category(models.TextChoices):
        FE = "fe", "프론트엔드"
        BE = "be", "백엔드"
        DA = "data", "데이터분석"
        AI = "ai", "인공지능"
        UIUX = "UI/UX", "디자인"
        ETC = "etc", "기타"


    course_id = models.AutoField(primary_key=True)
    #uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)  # 영구 식별자
    order_index = models.PositiveIntegerField(default=0, db_index=True)  # 코스 리스트 표시 순서

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=Type.choices)
    level = models.CharField(max_length=50)
    price = models.IntegerField()
    price_type = models.CharField(max_length=10, choices=[("free", "무료"), ("paid", "유료"), ("gov", "국비")], default="paid")
    description = models.TextField()
    course_time = models.DateTimeField()
    course_duedate = models.DateTimeField()
    discord_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # 활성화 여부

    class Meta:
        ordering = ["order_index", "course_id"]  # 기본 정렬

    def __str__(self):
        return self.title


class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    order_index = models.PositiveIntegerField(default=0, db_index=True)
    class Meta:
        ordering = ["order_index", "chapter_id"]
        constraints = [
            models.UniqueConstraint(fields=["course", "order_index"],
                                    name="uniq_chapter_order_per_course")
        ]  # 같은 코스 내에서 order_index 중복 방지
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.course.title}] {self.title}"

class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.CharField(max_length=500)
    duration = models.IntegerField()
    order_index = models.PositiveIntegerField(default=0, db_index=True)
    class Meta:
        ordering = ["order_index", "video_id"]
        constraints = [
            models.UniqueConstraint(fields=["chapter", "order_index"],
                                    name="uniq_video_order_per_chapter")
        ]  # 같은 챕터 내에서 order_index 중복 방지

    def __str__(self):
        return f"[{self.chapter.title}] {self.title}"

class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)  # PK
    name = models.CharField(max_length=255)  # 강사명
    code = models.IntegerField(unique=True)  # 강사 코드
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='instructors')
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    affiliation = models.CharField(max_length=255, blank=True, null=True)  # 소속
    profile_image = models.ImageField(upload_to='instructor_profiles/', blank=True) # 강사 프로필 이미지
    
    def __str__(self):
        return self.name