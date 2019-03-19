"""
WhatsUP: astronomical object suggestions for Las Cumbres Observatory
Copyright (C) 2014-2017 LCO

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

from django.urls import include, path, re_path
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    re_path(r'^', include('whatsup.urls')),
    re_path(r'^admin/', admin.site.urls),
]
