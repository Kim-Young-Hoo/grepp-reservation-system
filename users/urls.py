from django.urls import path, include

from users.views import LoginView, UserDetailView, LogoutView, UserRegisterView

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('user', UserDetailView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
]
