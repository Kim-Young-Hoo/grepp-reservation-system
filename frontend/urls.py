from django.urls import path
from django.views.generic import TemplateView

from frontend import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('signup/', views.SignUpPage.as_view(), name='signup'),
    path('exam/', views.ExamPage.as_view(), name='exam'),
    path('exam-detail/', views.ExamDetailPage.as_view(), name='exam-detail'),
    path('exam-create/', views.ExamCreatePage.as_view(), name='exam-create'),
]
