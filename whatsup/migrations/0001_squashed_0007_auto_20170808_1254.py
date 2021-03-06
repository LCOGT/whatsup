# Generated by Django 2.1.7 on 2019-04-12 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('whatsup', '0001_initial'), ('whatsup', '0002_auto_20150715_1535'), ('whatsup', '0003_target_owner'), ('whatsup', '0004_auto_20150903_1045'), ('whatsup', '0005_auto_20150904_0923'), ('whatsup', '0006_auto_20160318_1419'), ('whatsup', '0007_auto_20170808_1254')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Constellation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('shortname', models.CharField(max_length=3)),
            ],
            options={
                'verbose_name': 'Constellation',
                'verbose_name_plural': 'Constellations',
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('ra', models.FloatField(db_index=True, default=0.0)),
                ('dec', models.FloatField(default=0.0)),
                ('avm_code', models.CharField(blank=True, max_length=50, null=True)),
                ('avm_desc', models.CharField(blank=True, max_length=50, null=True)),
                ('exposure', models.TextField(default=b'0', verbose_name=b'exposure time on 2-meters')),
                ('best', models.BooleanField(default=False, verbose_name=b"Editor's pick")),
                ('constellation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='whatsup.Constellation')),
                ('filters', models.TextField(default=b'rp,v,b', verbose_name=b'filters using approved LCOGT nomenclature, comma separated')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Target',
                'verbose_name_plural': 'Targets',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('shortname', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.AddField(
            model_name='target',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='whatsup.Project'),
        ),
        migrations.AddField(
            model_name='target',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='targets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='target',
            name='aperture',
            field=models.CharField(choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'0m4', b'0.4-meter'), (b'any', b'Any')], blank=True, null=True, max_length=5),
        ),
        migrations.CreateModel(
            name='Params',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filters', models.CharField(choices=[(b'B', b'Bessell-B'), (b'I', b'Bessell-I'), (b'R', b'Bessell-R'), (b'V', b'Bessell-V'), (b'H-Alpha', b'H Alpha'), (b'H-Beta', b'H Beta'), (b'OIII', b'OIII'), (b'Y', b'PanSTARRS-Y'), (b'zs', b'PanSTARRS-Z'), (b'gp', b'SDSS-g&prime;'), (b'ip', b'SDSS-i&prime;'), (b'rp', b'SDSS-r&prime;'), (b'up', b'SDSS-u&prime;'), (b'solar', b'Solar (V+R)')], max_length=15, verbose_name=b'Filter name')),
                ('exposure', models.FloatField(default=1)),
                ('aperture', models.CharField(choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'0m4', b'0.4-meter'), (b'any', b'Any'), (b'sml', b' 1m and 0.4m only')], blank=True, null=True, max_length=5)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='whatsup.Target')),
            ],
            options={
                'ordering': ['target', 'aperture'],
                'verbose_name': 'Observation Parameter',
            },
        ),
        migrations.AlterField(
            model_name='target',
            name='aperture',
            field=models.CharField(choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'04m', b'0.4-meter'), (b'any', b'Any'), (b'sml', b' 1m and 0.4m only')], blank=True, null=True, max_length=5, verbose_name=b'Appropriate aperture'),
        ),
        migrations.AlterField(
            model_name='target',
            name='aperture',
            field=models.CharField(choices=[(b'1m0', b'1-meter'), (b'2m0', b'2-meter'), (b'0m4', b'0.4-meter'), (b'any', b'Any'), (b'sml', b' 1m and 0.4m only')], blank=True, null=True, max_length=5, verbose_name=b'Appropriate aperture'),
        ),
        migrations.RemoveField(
            model_name='target',
            name='exposure',
        ),
        migrations.RemoveField(
            model_name='target',
            name='filters',
        ),
    ]
