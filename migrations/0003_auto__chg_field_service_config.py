# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Service.config'
        db.alter_column('arguswatch_service', 'config_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['arguswatch.ServiceConfiguration']))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Service.config'
        raise RuntimeError("Cannot reverse this migration. 'Service.config' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Service.config'
        db.alter_column('arguswatch_service', 'config_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['arguswatch.ServiceConfiguration']))

    models = {
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
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['arguswatch']