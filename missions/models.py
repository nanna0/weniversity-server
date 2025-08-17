from django.db import models

class Mission(models.Model):
    email = models.EmailField()  # 사용자 식별을 위한 이메일
    problem_id = models.IntegerField()  # 문제 ID
    title = models.CharField(max_length=200)  # 문제 제목
    user_code = models.TextField(blank=True, null=True)  # 제출한 코드
    is_correct = models.BooleanField(default=False)  # 정답 여부
    message = models.TextField(blank=True, null=True)  # 평가 메시지
    submitted_at = models.DateTimeField(auto_now_add=True)  # 제출 시간

    class Meta:
        # unique_together = ('email', 'problem_id')  # 한 사용자당 문제당 하나의 제출만 허용
        ordering = ['-submitted_at']  # 최신순 정렬

    def __str__(self):
        return f"{self.email} - {self.title}"