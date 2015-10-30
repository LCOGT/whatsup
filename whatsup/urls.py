"""
WhatsUP: astronomical object suggestions for Las Cumbres Observatory Global Telescope Network
Copyright (C) 2014-2015 LCOGT

urls.py

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.conf.urls import include, url

from . import views


urlpatterns = [
    url(r'^$', views.api_root, name='apiroot'),
    url(r'search/v2/$', views.AdvTargetListView.as_view(), name="api_v2_search"),
    url(r'search/$', views.TargetListView.as_view(), name="api_search"),
    url(r'messier/$', views.TargetListView.as_view(), name="messier_search"),
    url(r'^target/(?P<pk>[0-9]+)/$', views.TargetDetail.as_view(), name='api_target_detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
