from django.db import models
from django.utils.translation import ugettext as _

APERTURES = (('1m0','1-meter'), ('2m0','2-meter'), ('04m','0.4-meter'), ('any', 'Any') )

class Constellation(models.Model):
    name = models.CharField(max_length=20)
    shortname = models.CharField(max_length=3)
    class Meta:
        verbose_name = _('Constellation')
        verbose_name_plural = _('Constellations')

    def __unicode__(self):
        return u"%s" % self.name
    

class Project(models.Model):
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length=10)
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

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
    exposure = models.TextField('default exposure time in RVB',default='0')
    filters = models.TextField('filters using approved LCOGT nomenclature, comma separated',default='r,v,b')
    best = models.BooleanField("Editor's pick", default=False)
    aperture = models.CharField(max_length=3, choices=APERTURES, default='any')
    project = models.ForeignKey(Project,null=True,blank=True)

    class Meta:
        verbose_name = _('Target')
        verbose_name_plural = _('Targets')
        ordering = ['name',]

    def __unicode__(self):
        return u"%s" % self.name
