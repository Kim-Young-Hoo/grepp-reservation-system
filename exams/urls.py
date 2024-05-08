from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamSlotViewSet

router = DefaultRouter()
router.register(r'exams', ExamSlotViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
