# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceConfiguration'
        db.create_table('argus_service_configurations_serviceconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_template', self.gf('django.db.models.fields.BooleanField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, blank=True)),
            ('check_interval', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('retry_interval_soft', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('retry_interval_hard', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('max_retries_soft', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('argus_service_configurations', ['ServiceConfiguration'])


    def backwards(self, orm):
        # Deleting model 'ServiceConfiguration'
        db.delete_table('argus_service_configurations_serviceconfiguration')


    models = {
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'check_interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {}),
            'max_retries_soft': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'blank': 'True'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['argus_service_configurations']