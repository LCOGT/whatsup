# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('whatsup_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('shortname', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('whatsup', ['Project'])

        # Adding field 'Target.filters'
        db.add_column('whatsup_target', 'filters',
                      self.gf('django.db.models.fields.TextField')(default='r,v,b'),
                      keep_default=False)

        # Adding field 'Target.aperture'
        db.add_column('whatsup_target', 'aperture',
                      self.gf('django.db.models.fields.CharField')(default='any', max_length=3),
                      keep_default=False)

        # Adding field 'Target.project'
        db.add_column('whatsup_target', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['whatsup.Project'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Target.exposure'
        db.alter_column('whatsup_target', 'exposure', self.gf('django.db.models.fields.TextField')())
        # Adding index on 'Target', fields ['ra']
        db.create_index('whatsup_target', ['ra'])


    def backwards(self, orm):
        # Removing index on 'Target', fields ['ra']
        db.delete_index('whatsup_target', ['ra'])

        # Deleting model 'Project'
        db.delete_table('whatsup_project')

        # Deleting field 'Target.filters'
        db.delete_column('whatsup_target', 'filters')

        # Deleting field 'Target.aperture'
        db.delete_column('whatsup_target', 'aperture')

        # Deleting field 'Target.project'
        db.delete_column('whatsup_target', 'project_id')


        # Changing field 'Target.exposure'
        db.alter_column('whatsup_target', 'exposure', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'whatsup.constellation': {
            'Meta': {'object_name': 'Constellation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'whatsup.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'shortname': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'whatsup.target': {
            'Meta': {'ordering': "['name']", 'object_name': 'Target'},
            'aperture': ('django.db.models.fields.CharField', [], {'default': "'any'", 'max_length': '3'}),
            'avm_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'avm_desc': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'best': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'constellation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whatsup.Constellation']", 'null': 'True', 'blank': 'True'}),
            'dec': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exposure': ('django.db.models.fields.TextField', [], {'default': "'0'"}),
            'filters': ('django.db.models.fields.TextField', [], {'default': "'r,v,b'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['whatsup.Project']", 'null': 'True', 'blank': 'True'}),
            'ra': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'})
        }
    }

    complete_apps = ['whatsup']