from django.conf.urls import patterns, url

from imgs import views

urlpatterns = patterns('',
    # ex: /imgs/fetchbg
    url(r'^fetchbg$', views.fetchbg, name='fetchbg'),
)