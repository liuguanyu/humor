from django.conf.urls import patterns, url

from joke import views

urlpatterns = patterns('',
    # ex: /jokes/
    url(r'^$', views.index, name='index'),

    # ex: /jokes/5/
    url(r'^(?P<joke_id>\d+)/$', views.detail, name='detail'),
    url(r'^list/(?P<page_no>\d*)$', views.get_joke_list, name='get_joke_list'),
    url(r'^getrandom$', views.get_random , name='get_random'),
    url(r'^fetchjoke/(?P<user_id>\d+)/$', views.fetch_joke, name='fetch_joke'),
)