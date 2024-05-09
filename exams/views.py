from django.db import models
from django.db.models import Q, ExpressionWrapper, BooleanField
from django.utils import timezone
from rest_framework import viewsets
from django_filters import rest_framework as django_filters
from rest_framework.filters import OrderingFilter

from project.pagination import CustomPagination
from project.permissions import IsAdminOrReadOnly
from .models import Exam
from .serializers import ExamSerializer


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [django_filters.DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['-created_at']
    ordering = ['-created_at']
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = self.queryset.filter(start_time__gt=timezone.now() + timezone.timedelta(hours=3))
            queryset = queryset.annotate(
                full_capacity=ExpressionWrapper(Q(capacity__gt=models.F('reservation_count')), output_field=BooleanField())
            )
            queryset = queryset.filter(full_capacity=True)
        return queryset
