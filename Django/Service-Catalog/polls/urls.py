from django.conf.urls import url
from polls.views import HomeView
from django.urls import path

from . import views

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    
]
