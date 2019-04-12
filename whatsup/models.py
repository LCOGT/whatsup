"""
WhatsUP: astronomical object suggestions for Las Cumbres Observatory Global Telescope Network
Copyright (C) 2014-2015 LCOGT

models.py - Database schemas

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

APERTURES = (
    ('1m0', '1-meter'), ('2m0', '2-meter'), ('0m4', '0.4-meter'), ('any', 'Any'), ('sml', ' 1m and 0.4m only'))

FILTERS = (('B', 'Bessell-B'),
           ('I', 'Bessell-I'),
           ('R', 'Bessell-R'),
           ('V', 'Bessell-V'),
           ('H-Alpha', 'H Alpha'),
           ('H-Beta', 'H Beta'),
           ('OIII', 'OIII'),
           ('Y', 'PanSTARRS-Y'),
           ('zs', 'PanSTARRS-Z'),
           ('gp', 'SDSS-g&prime;'),
           ('ip', 'SDSS-i&prime;'),
           ('rp', 'SDSS-r&prime;'),
           ('up', 'SDSS-u&prime;'),
           ('solar', 'Solar (V+R)')
           )

CATEGORIES = (
                ('3.6.4', 'Star cluster'),
                ('3.6.4.1', 'Open Cluster'),
                ('3.6.4.2', 'Globular Cluster'),
                ('4', 'Nebula'),
                ('4.1.2', 'Star-forming Nebula'),
                ('4.1.3', 'Planetary Nebula'),
                ('4.1.4', 'Supernova Remnant'),
                ('5','Galaxy'),
                ('5.1.1', 'Spiral Galaxy'),
                ('5.1.2', 'Barred Spiral Galaxy'),
                ('5.1.4', 'Elliptical Galaxy'),
                ('5.1.6', 'Irregular Galaxies'),
                ('5.5', 'Galaxy Groups'),
                )

class Constellation(models.Model):
    name = models.CharField(max_length=20)
    shortname = models.CharField(max_length=3)

    class Meta:
        verbose_name = _('Constellation')
        verbose_name_plural = _('Constellations')

    def __unicode__(self):
        return u"%s" % self.name

class Target(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    ra = models.FloatField(db_index=True, default=0.0)
    dec = models.FloatField(default=0.0)
    avm_code = models.CharField(max_length=50, null=True, blank=True)
    avm_desc = models.CharField(max_length=50, null=True, blank=True)
    constellation = models.ForeignKey(Constellation, null=True, blank=True, on_delete=models.CASCADE)
    best = models.BooleanField("Editor's pick", default=False)

    class Meta:
        verbose_name = _('Target')
        verbose_name_plural = _('Targets')
        ordering = ['name', ]

    def __unicode__(self):
        return u"%s" % self.name


class Params(models.Model):
    target = models.ForeignKey(Target, related_name='parameters', on_delete=models.CASCADE)
    filters = models.CharField('Filter name', choices=FILTERS, max_length=15)
    exposure = models.FloatField(default=1)
    aperture = models.CharField(max_length=3, choices=APERTURES, default='1m0')

    class Meta:
        verbose_name = _('Observation Parameter')
        ordering = ['target', 'aperture']

    def __unicode__(self):
        return u"%s for %s" % (self.filters, self.target)
