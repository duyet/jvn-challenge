from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^dataset/$', views.dataset, name='dataset'),
    url(r'^submit/(?P<id>[0-9]+)$', views.submit, name='submit'),
    url(r'^dataset/download/(?P<id>[0-9]+)$', views.download, name='download'),
]