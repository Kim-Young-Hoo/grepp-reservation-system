from django.urls import path, include
from rest_framework_nested import routers
from exams.urls import router as exams_router
from reservations.views import ReservationViewSet, ReservationByUserReadOnlyView

reservation_router = routers.NestedSimpleRouter(exams_router, r'exams', lookup='exam')
reservation_router.register(r'reservations', ReservationViewSet, basename='exam-reservations')


urlpatterns = [
    path('', include(reservation_router.urls)),
    path('users/<int:id>/reservations', ReservationByUserReadOnlyView.as_view({'get': 'list'}))
]
