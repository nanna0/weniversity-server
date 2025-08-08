# courses/models.py

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
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=10, choices=Type.choices)
    level = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    course_time = models.DateTimeField()
    course_duedate = models.DateTimeField()
    discord_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    order = models.CharField(max_length=10)
    course = models.ForeignKey(Course, related_name='chapters', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video_url = models.CharField(max_length=500)
    duration = models.IntegerField()
    order = models.IntegerField()


class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)  # PK
    name = models.CharField(max_length=255)  # 강사명
    code = models.IntegerField(unique=True)  # 강사 코드
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='instructors')
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    affiliation = models.CharField(max_length=255, blank=True, null=True)  # 소속