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
            ('is_template', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50, unique=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('check_interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=600)),
            ('retry_interval_soft', self.gf('django.db.models.fields.PositiveIntegerField')(default=120)),
            ('retry_interval_hard', self.gf('django.db.models.fields.PositiveIntegerField')(default=600)),
            ('max_retries_soft', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3)),
            ('passive_check_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('passive_check_ips', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('passive_check_api_key', self.gf('django.db.models.fields.CharField')(blank=True, max_length=100)),
            ('api_can_trigger_events', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('argus_service_configurations', ['ServiceConfiguration'])


    def backwards(self, orm):
        # Deleting model 'ServiceConfiguration'
        db.delete_table('argus_service_configurations_serviceconfiguration')


    models = {
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'api_can_trigger_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_retries_soft': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50', 'unique': 'True'}),
            'passive_check_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passive_check_api_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'passive_check_ips': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {'default': '120'})
        }
    }

    complete_apps = ['argus_service_configurations']