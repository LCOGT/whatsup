# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsup', '0005_auto_20150904_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='target',
            name='aperture',
            field=models.CharField(default=b'any', max_length=3, verbose_name=b'Appropriate aperture', choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'0m4', b'0.4-meter'), (b'any', b'Any'), (b'sml', b' 1m and 0.4m only')]),
        ),
    ]
