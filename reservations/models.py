from django.db import models

from exams.models import Exam
from users.models import User


class Reservation(models.Model):
    """
    예약 엔티티 - 시험 슬롯과 사용자 간의 연결 테이블
    """
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='reservations', help_text="예약한 사용자")
    exam = models.ForeignKey(Exam, db_index=True, on_delete=models.CASCADE, related_name='reservations', help_text="예약된 시험 슬롯")
    is_confirmed = models.BooleanField(default=False, help_text="예약 확정 여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
