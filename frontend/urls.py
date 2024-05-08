from django.urls import path
from django.views.generic import TemplateView

from frontend import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('signup/', views.SignUpPage.as_view(), name='signup'),
]
