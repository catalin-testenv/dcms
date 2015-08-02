

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.display, name='display'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.edit, name='edit'),
]
