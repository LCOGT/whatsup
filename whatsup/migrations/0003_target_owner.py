# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whatsup', '0002_auto_20150715_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='owner',
            field=models.ForeignKey(related_name='targets', default=1, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='target',
            name='aperture',
            field=models.CharField(default=b'any', max_length=3, choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'04m', b'0.4-meter'), (b'any', b'Any')]),
        ),
    ]
        
