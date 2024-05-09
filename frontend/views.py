from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class IndexPage(TemplateView):
    template_name = 'index.html'


class SignUpPage(TemplateView):
    template_name = 'signup.html'


class ExamPage(TemplateView):
    template_name = 'exam.html'


class ExamDetailPage(TemplateView):
    template_name = 'exam-detail.html'


class AdminPage(TemplateView):
    template_name = 'admin.html'


class ExamCreatePage(TemplateView):
    template_name = 'exam-create.html'
