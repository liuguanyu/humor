from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', include('joke.urls', namespace="joke")),
    # url(r'^blog/', include('blog.urls')),

    url(r'^detail/', include('joke.urls', namespace="joke")),

    url(r'^joke/', include('joke.urls', namespace="joke")),
    url(r'^imgs/', include('imgs.urls', namespace="imgs")),
    
    url(r'^admin/', include(admin.site.urls)),
)
