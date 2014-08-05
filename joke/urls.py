from django.conf.urls import patterns, url

from joke import views

urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<joke_id>\d+)/$', views.detail, name='detail'),
)