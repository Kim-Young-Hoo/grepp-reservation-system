import datetime
from django.db import models
from django.utils import timezone


class Exam(models.Model):
    """
    시험 신청 슬롯 엔티티
    """
    title = models.CharField(max_length=255, db_index=True, help_text="시험 제목")
    description = models.CharField(max_length=255, help_text="시험 설명")
    duration = models.IntegerField(default=2, help_text="시험 진행 시간(hour)")
    start_time = models.DateTimeField(db_index=True, help_text="시험 시작 시간")
    reservation_count = models.IntegerField(default=0, help_text="예약 카운트")
    capacity = models.IntegerField(default=50000, help_text="최대 수용 인원(명)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.start_time}"

    @property
    def is_exam_open(self):
        return self.reservation_count < self.capacity and self.start_time > timezone.now() + datetime.timedelta(hours=3)