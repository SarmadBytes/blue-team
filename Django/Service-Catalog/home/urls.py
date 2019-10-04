from django.conf.urls import url
from home.views import index
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', index.as_view(), name='index'),
    
]
