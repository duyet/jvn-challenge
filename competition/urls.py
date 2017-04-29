from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^dataset/$', views.dataset, name='dataset'),
    url(r'^preview/(?P<id>[0-9]+)/$', views.preview, name='preview'),
    url(r'^preview_submit/(?P<id>[0-9]+)/$', views.preview_submit, name='preview_submit'),
    url(r'^submit/(?P<id>[0-9]+)$', views.submit, name='submit'),
    url(r'^dataset/download/(?P<id>[0-9]+)$', views.download, name='download'),
]