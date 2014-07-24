# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Constellation'
        db.create_table('whatsup_constellation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal('whatsup', ['Constellation'])

        # Adding model 'Target'
        db.create_table('whatsup_target', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('avm_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('avm_desc', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('constellation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['whatsup.Constellation'], null=True, blank=True)),
            ('exposure', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('best', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('whatsup', ['Target'])


    def backwards(self, orm):
        # Deleting model 'Constellation'
        db.delete_table('whatsup_constellation')

        # Deleting model 'Target'
        db.delete_table('whatsup_target')


    models = {
        'whatsup.constellation': {
            'Meta': {'object_name': 'Constellation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'whatsup.target': {
            'Meta': {'object_name': 'Target'},
            'avm_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'avm_desc': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'best': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whatsup.Constellation']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exposure': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['whatsup']