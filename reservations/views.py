from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from exams.models import Exam
from project.pagination import CustomPagination
from project.permissions import IsAdminOrReadOnlyForIsConfirmed
from rest_framework import viewsets, permissions, status
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework import filters


class UserFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        return queryset.filter(user=user)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnlyForIsConfirmed]
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]
    filter_backends = [UserFilterBackend]

    def get_queryset(self):
        queryset = self.queryset.filter(exam_id=self.kwargs.get('exam_pk'))
        return queryset

    def perform_create(self, serializer):
        exam_id = self.kwargs.get('exam_pk')
        exam = get_object_or_404(Exam, pk=exam_id)

        existing_reservation = Reservation.objects.filter(user=self.request.user, exam=exam)
        if existing_reservation.exists():
            raise ValidationError("이미 해당 시험에 예약 되어 있습니다.")

        serializer.save(user=self.request.user, exam=exam)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.user != request.user:
            raise PermissionDenied("다른 사용자의 예약은 수정할 수 없습니다.")

        if instance.is_confirmed:
            return Response({"error": "수정할 수 없습니다. 예약이 이미 확인되었습니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        exam = instance.exam

        if exam.is_exam_open:
            with transaction.atomic():
                serializer.validated_data['is_confirmed'] = True
                self.perform_update(serializer)
                exam.reservation_count += 1
                exam.save()
            return Response(serializer.data)
        else:
            raise ValidationError("예약이 불가능한 시험입니다.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not self.request.user.is_staff and instance.user != self.request.user:
            raise PermissionDenied("다른 사용자의 예약은 삭제할 수 없습니다.")

        if instance.is_confirmed:
            return Response({"error": "삭제할 수 없습니다. 예약이 이미 확인되었습니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReservationByUserReadOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
