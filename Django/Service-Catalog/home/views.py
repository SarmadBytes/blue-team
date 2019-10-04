from django.views.generic import TemplateView
from django.shortcuts import render


class index(TemplateView):
    template_name = 'index/home.html'