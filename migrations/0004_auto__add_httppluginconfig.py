# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HttpPluginConfig'
        db.create_table('arguswatch_httppluginconfig', (
            ('serviceconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['arguswatch.ServiceConfiguration'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('timeout', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('response_code', self.gf('django.db.models.fields.IntegerField')(default=200)),
            ('response_text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('arguswatch', ['HttpPluginConfig'])


    def backwards(self, orm):
        # Deleting model 'HttpPluginConfig'
        db.delete_table('arguswatch_httppluginconfig')


    models = {
        'arguswatch.httppluginconfig': {
            'Meta': {'_ormbases': ['arguswatch.ServiceConfiguration'], 'object_name': 'HttpPluginConfig'},
            'response_code': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'response_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'serviceconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['arguswatch.ServiceConfiguration']"}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'arguswatch.service': {
            'Meta': {'object_name': 'Service'},
            'config': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['arguswatch.ServiceConfiguration']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['arguswatch.Service']", 'blank': 'True'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'arguswatch.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'polymorphic_arguswatch.serviceconfiguration_set'", 'to': "orm['contenttypes.ContentType']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['arguswatch']