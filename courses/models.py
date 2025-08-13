# courses/models.py
#import uuid
from django.db import models, transaction, IntegrityError
from django.core.validators import MinValueValidator, MaxValueValidator
import secrets
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

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
    code = models.PositiveIntegerField(
        unique=True, db_index=True,
        validators=[MinValueValidator(10000), MaxValueValidator(99999)],
        null=True, blank=True,
    )
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
    course_image = models.ImageField(upload_to='course/', blank=True) # 코스 이미지
    
    # User와 M2M (중간모델 Enrollment를 통해 연결)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Enrollment',
        related_name='courses',          # user.courses 로 접근
    )

    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='CourseLike',
        related_name='liked_courses',
        blank=True,
    )
    def __str__(self):
        return self.title
    
    @staticmethod
    def _gen_code_5digits() -> int:   # 인스턴스 메서드
        return secrets.randbelow(90000) + 10000

    def save(self, *args, **kwargs):
        if self.code is None:
            last_err = None
            for _ in range(30):  # 유니크 충돌 시 재시도
                self.code = self._gen_code_5digits()   # ← self 로 호출
                try:
                    with transaction.atomic():
                        return super().save(*args, **kwargs)
                except IntegrityError as e:
                    self.code = None
                    last_err = e
                    continue
            raise last_err or IntegrityError("5자리 코드 자동 발급 실패")
        return super().save(*args, **kwargs)
    
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
def validate_file_size(f):
    limit = getattr(settings, "MAX_UPLOAD_SIZE", 200 * 1024 * 1024)  # 기본 200MB
    if f.size > limit:
        raise ValidationError(f"파일이 너무 큽니다. 최대 {limit/1024/1024:.0f}MB")
    
class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='video/', blank=True, null=True, 
                                  validators=[
                                    FileExtensionValidator(['mp4','mov','mkv','webm','avi']),
                                    validate_file_size,
                                ], 
                                  )
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
    english_name = models.CharField(max_length=255, blank=True, null=True)  # 영어 이름   
    code = models.IntegerField(unique=True)  # 강사 코드
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='instructors')
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    affiliation = models.CharField(max_length=255, blank=True, null=True)  # 소속
    profile_image = models.ImageField(upload_to='instructor_profiles/', blank=True) # 강사 프로필 이미지
    
    def __str__(self):
        return self.name

# 수강 신청 모델   
class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        DROPPED = 'dropped', 'Dropped'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='course_enrollments',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    enrolled_at = models.DateTimeField(auto_now_add=True) # 등록일시
    expired_at = models.DateTimeField(null=True, blank=True)  # 만료일시
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 0~100 같은 퍼센트

    class Meta:
        unique_together = ('user', 'course')  # 같은 유저-코스 중복 방지
        indexes = [models.Index(fields=['user', 'course'])]

    def __str__(self):
        return f'{self.user} ↔ {self.course} ({self.status})'
    
# 강의 좋아요
class CourseLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_likes'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')  # 같은 유저가 같은 강의를 중복 좋아요 방지
        indexes = [models.Index(fields=['user', 'course'])]