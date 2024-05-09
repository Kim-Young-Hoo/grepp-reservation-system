import datetime

from django.core.management.base import BaseCommand
from django.db import connection

from exams.models import Exam
from reservations.models import Reservation
from users.models import User


class Command(BaseCommand):
    help = 'Execute post migration operations'

    def handle(self, *args, **kwargs):

        try:
        # dummy users
            for i in range(1, 10):
                User.objects.create_user(email="dummy{}@test.com".format(i), password="1234")
            print("dummy user created complete")

            # staff users
            User.objects.create_superuser(email="admin@test.com", password="1234")
            print("admin user created complete")

            # dummy exams
            current_datetime = datetime.datetime.now()
            current_hour_datetime = current_datetime.replace(minute=0, second=0, microsecond=0)
            for i in range(30):
                Exam.objects.create(
                    title="시험 {}번".format(i),
                    description="이 시험은 이러이러이러합니다",
                    start_time=current_hour_datetime + datetime.timedelta(days=i)
                )
            print("dummy exam created complete")

            # dummy reservations
            for user in User.objects.filter(is_staff=False)[:3]:
                for exam in Exam.objects.all():
                    Reservation.objects.create(user=user, exam=exam)
            print("dummy reservations created complete")
        except Exception as e:
            print(e)
