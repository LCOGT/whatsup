"""
WhatsUP: astronomical object suggestions for Las Cumbres Observatory Global Telescope Network
Copyright (C) 2014-2015 LCOGT

admin.py

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from django.contrib import admin
from whatsup.models import Target, Project


class TargetAdmin(admin.ModelAdmin):
    list_display = ['name', 'ra', 'dec', 'description', 'avm_desc']
    list_filter = ['avm_desc']


admin.site.register(Target, TargetAdmin)
admin.site.register(Project)
