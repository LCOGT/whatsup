# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whatsup', '0004_auto_20150903_1045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='params',
            options={'ordering': ['target', 'aperture'], 'verbose_name': 'Observation Parameter'},
        ),
        migrations.AlterField(
            model_name='params',
            name='aperture',
            field=models.CharField(default=b'1m0', max_length=3, choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter')]),
        ),
        migrations.AlterField(
            model_name='params',
            name='target',
            field=models.ForeignKey(related_name='parameters', to='whatsup.Target', on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='target',
            name='aperture',
            field=models.CharField(default=b'any', max_length=3, verbose_name=b'Appropriate aperture', choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'04m', b'0.4-meter'), (b'any', b'Any'), (b'sml', b' 1m and 0.4m only')]),
        ),
    ]
