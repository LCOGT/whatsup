# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Target.ra'
        db.add_column('whatsup_target', 'ra',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'Target.dec'
        db.add_column('whatsup_target', 'dec',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Target.ra'
        db.delete_column('whatsup_target', 'ra')

        # Deleting field 'Target.dec'
        db.delete_column('whatsup_target', 'dec')


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
            'dec': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exposure': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'ra': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        }
    }

    complete_apps = ['whatsup']