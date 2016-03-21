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
        new_filters = {
                'v':'gp',
                'b':'B',
                'rp':'R',
        }
        tgs = Target.objects.filter(aperture__in=['any','sml'])
        for t in tgs:
            filters = [x.strip() for x in t.filters.split(',')]
            if t.aperture == 'any':
                aperture = {'0m4':4.}
            elif t.aperture == 'sml':
                aperture = {'0m4':1.5}
            for ap_id, mult in aperture.items():
                for f in filters:
                    try:
                        filterid = new_filters[f]
                    except:
                        filterid = f
                    try:
                        exp_time = float(t.exposure)*mult
                    except:
                        exp_time = 30.
                    p = Params(filters=filterid, exposure=exp_time,aperture=ap_id , target=t)
                    p.save()
                    self.stdout.write('Added %s' % p)
