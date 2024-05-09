from rest_framework import serializers

from reservations.models import Reservation
from .models import Exam


class ExamSerializer(serializers.ModelSerializer):
    is_reserved = serializers.SerializerMethodField()
    is_confirmed = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = '__all__'

    def get_is_reserved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Reservation.objects.filter(user=request.user, exam=obj).exists()
        return False

    def get_is_confirmed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Reservation.objects.filter(user=request.user, exam=obj, is_confirmed=True).exists()
        return False
