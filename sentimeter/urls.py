from django.conf.urls import url
from . import views
from .views import userinput

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^analyse/(?P<choice>[1-4])/?$', views.analyse, name='analyse'),
]