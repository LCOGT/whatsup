# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whatsup', '0003_target_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Params',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filters', models.CharField(max_length=15, verbose_name=b'Filter name', choices=[(b'B', b'Bessell-B'), (b'I', b'Bessell-I'), (b'R', b'Bessell-R'), (b'V', b'Bessell-V'), (b'H-Alpha', b'H Alpha'), (b'H-Beta', b'H Beta'), (b'OIII', b'OIII'), (b'Y', b'PanSTARRS-Y'), (b'zs', b'PanSTARRS-Z'), (b'gp', b'SDSS-g&prime;'), (b'ip', b'SDSS-i&prime;'), (b'rp', b'SDSS-r&prime;'), (b'up', b'SDSS-u&prime;'), (b'solar', b'Solar (V+R)')])),
                ('exposure', models.FloatField(default=1)),
                ('aperture', models.CharField(default=b'any', max_length=3, choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter')])),
                ('target', models.ForeignKey(to='whatsup.Target', on_delete=models.CASCADE)),
            ],
        ),
    ]
