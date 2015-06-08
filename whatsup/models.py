'''
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
'''
from django.db import models
from django.utils.translation import ugettext as _

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
    description = models.TextField(null=True,blank=True)
    ra = models.FloatField(db_index=True, default=0.0)
    dec = models.FloatField(default=0.0)
    avm_code = models.CharField(max_length=50,null=True,blank=True)
    avm_desc = models.CharField(max_length=50,null=True,blank=True)
    constellation = models.ForeignKey(Constellation,null=True,blank=True)
    exposure = models.IntegerField('default exposure time in RVB',default=0)
    #filters = models.ManyToManyField(Filters,null=True,blank=True)
    best = models.BooleanField("Editor's pick", default=False)

    class Meta:
        verbose_name = _('Target')
        verbose_name_plural = _('Targets')
        ordering = ['name',]

    def __unicode__(self):
        return u"%s" % self.name
