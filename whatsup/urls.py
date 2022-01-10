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

from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.api_root, name='apiroot'),
    path('all/', views.TargetFullListView.as_view(), name="api_full_list"),
    path('target/',views.TargetDetailView.as_view(), name="api_target"),
    path('search/', views.TargetListView.as_view(), name="api_search"),
    path('range/', views.TargetListRangeView.as_view(), name="api_range"),
]
