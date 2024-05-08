from django.urls import path, include

from users.views import LoginView, LogoutView, UserRegisterView

urlpatterns = [
    path('register', UserRegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
]
