from django.conf.urls import url
from SaaSRequests.views import HomeView
from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    url(r'Success', TemplateView.as_view(template_name='Success'), name='home'),
    url(r'^$', HomeView.as_view(), name='home'),
    
]
