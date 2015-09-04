"""
WhatsUP: astronomical object suggestions for Las Cumbres Observatory Global Telescope Network
Copyright (C) 2014-2015 LCOGT

ingest_guidedtours.py  - Ingest of existing XML files containing Guided Tours

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from django.conf import settings
from django.core.management.base import BaseCommand

from whatsup.models import Target, Params

class Command(BaseCommand):
    help = 'Update all targets to use new Params model instances'

    def handle(self, *args, **options):
        tgs = Target.objects.all()
        for t in tgs:
            filters = [x.strip() for x in t.filters.split(',')]
            if t.aperture == 'any' or t.aperture == 'sml':
                aperture = '1m0'
            else:
                aperture = t.aperture
            for f in filters:
                if f =='v':
                    f = 'V'
                elif f == 'b':
                    f='B'
                p = Params(filters=f, exposure=t.exposure,aperture=aperture, target=t)
                p.save()
                self.stdout.write('Added %s' % p)
