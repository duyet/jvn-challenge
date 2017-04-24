from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^help/$', views.help, name='help'),
    url(r'^resources/$', views.resources, name='resources'),
]