from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('whatsup.views',
    url(r'^$', 'home', name='home'),
    url(r'search/(?P<format>[^/]+)/$', 'search'),
    url(r'search/$', 'search'),
    url(r'^admin/', include(admin.site.urls)),
)
