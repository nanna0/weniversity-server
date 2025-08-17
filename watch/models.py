from django.db import models
import random

class FrontTest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} <{self.email}>"
    
class UserLastWatched(models.Model):
    userId = models.CharField(max_length=100)
    chapterId = models.IntegerField(null=True, blank=True)  # 추가
    videoId = models.IntegerField(null=True, blank=True)
    courseId = models.IntegerField()
    
    # 마지막 시청한 챕터/비디오 정보
    lastChapterId = models.IntegerField()
    lastVideoId = models.IntegerField()

    # 순서 정보 (이어서 보기용 정렬)
    lastChapterOrder = models.IntegerField(default=0)
    lastVideoOrder = models.IntegerField(default=0)
    lastChapterIndex = models.IntegerField(default=1)
    lastVideoIndex = models.IntegerField(default=1)
    lastCurrentTime = models.FloatField(default=0.0)

    # 시청 시각
    lastWatchedAt = models.DateTimeField(auto_now=True)

    class Meta:
        # 사용자당 코스별로 하나의 마지막 시청 위치만
        unique_together = ('userId', 'courseId')

    def __str__(self):
        return f"{self.userId} - Last watched Course {self.courseId}"
    

class WatchProgress(models.Model):
    userId = models.CharField(max_length=100)
    courseId = models.IntegerField(db_index=True)
    chapterId = models.IntegerField(db_index=True)
    videoId = models.IntegerField(db_index=True)

    # 시청 진행률
    currentTime = models.FloatField(default=0)
    totalDuration = models.FloatField(default=0)
    watchedPercentage = models.FloatField(default=0)
    isCompleted = models.BooleanField(default=False)

    # 시청 통계 
    totalWatchTime = models.FloatField(default=0)
    sessionCount = models.IntegerField(default=0)
    watchSpeed = models.FloatField(default=1.0)

    # 시간 정보
    firstWatchedAt = models.DateTimeField(auto_now_add=True)
    lastWatchedAt = models.DateTimeField(auto_now=True)
    completedAt = models.DateTimeField(null=True, blank=True)

    lastChapterIndex = models.IntegerField(default=0)  # 새로 추가
    lastVideoIndex = models.IntegerField(default=0)    # 새로 추가

    # 순서 정보 (정렬용)
    chapterOrder = models.IntegerField(default=0)   # 챕터 순서
    videoOrder = models.IntegerField(default=0)     # 비디오 순서

    chapterIndex = models.IntegerField(default=1)  # 사용자에게 보여줄 챕터 번호 (1부터)
    videoIndex = models.IntegerField(default=1)    # 사용자에게 보여줄 비디오 번호
        
    class Meta:
        unique_together = ['userId', 'courseId', 'chapterId', 'videoId']
        indexes = [
            models.Index(fields=['userId', 'courseId']),
            models.Index(fields=['userId', 'courseId', 'chapterOrder']),
            models.Index(fields=['userId', 'courseId', 'chapterOrder', 'videoOrder']),
        ]
    
    def __str__(self):
        return f"{self.userId}_{self.courseId}_{self.chapterId}_{self.videoId}"