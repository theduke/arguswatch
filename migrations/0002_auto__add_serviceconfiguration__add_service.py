# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceConfiguration'
        db.create_table('arguswatch_serviceconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['contenttypes.ContentType'], related_name='polymorphic_arguswatch.serviceconfiguration_set')),
        ))
        db.send_create_signal('arguswatch', ['ServiceConfiguration'])

        # Adding model 'Service'
        db.create_table('arguswatch_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, to=orm['arguswatch.Service'], null=True)),
            ('plugin', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['arguswatch.ServiceConfiguration'])),
        ))
        db.send_create_signal('arguswatch', ['Service'])


    def backwards(self, orm):
        # Deleting model 'ServiceConfiguration'
        db.delete_table('arguswatch_serviceconfiguration')

        # Deleting model 'Service'
        db.delete_table('arguswatch_service')


    models = {
        'arguswatch.service': {
            'Meta': {'object_name': 'Service'},
            'config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['arguswatch.ServiceConfiguration']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['arguswatch.Service']", 'null': 'True'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'arguswatch.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['contenttypes.ContentType']", 'related_name': "'polymorphic_arguswatch.serviceconfiguration_set'"})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['arguswatch']