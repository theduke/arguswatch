# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ServiceConfiguration.max_retries_soft'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'max_retries_soft')

        # Deleting field 'ServiceConfiguration.check_interval'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'check_interval')

        # Deleting field 'ServiceConfiguration.retry_interval_soft'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'retry_interval_soft')

        # Deleting field 'ServiceConfiguration.retry_interval_hard'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'retry_interval_hard')

        # Adding field 'ServiceConfiguration.check_interval_ok'
        db.add_column('argus_service_configurations_serviceconfiguration', 'check_interval_ok',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=900),
                      keep_default=False)

        # Adding field 'ServiceConfiguration.check_interval_provisional'
        db.add_column('argus_service_configurations_serviceconfiguration', 'check_interval_provisional',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=300),
                      keep_default=False)

        # Adding field 'ServiceConfiguration.check_interval_warning'
        db.add_column('argus_service_configurations_serviceconfiguration', 'check_interval_warning',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)

        # Adding field 'ServiceConfiguration.check_interval_down'
        db.add_column('argus_service_configurations_serviceconfiguration', 'check_interval_down',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)

        # Adding field 'ServiceConfiguration.check_interval_unknown'
        db.add_column('argus_service_configurations_serviceconfiguration', 'check_interval_unknown',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)

        # Adding field 'ServiceConfiguration.max_retries'
        db.add_column('argus_service_configurations_serviceconfiguration', 'max_retries',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ServiceConfiguration.max_retries_soft'
        db.add_column('argus_service_configurations_serviceconfiguration', 'max_retries_soft',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3),
                      keep_default=False)

        # Adding field 'ServiceConfiguration.check_interval'
        db.add_column('argus_service_configurations_serviceconfiguration', 'check_interval',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)

        # Adding field 'ServiceConfiguration.retry_interval_soft'
        db.add_column('argus_service_configurations_serviceconfiguration', 'retry_interval_soft',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=120),
                      keep_default=False)

        # Adding field 'ServiceConfiguration.retry_interval_hard'
        db.add_column('argus_service_configurations_serviceconfiguration', 'retry_interval_hard',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)

        # Deleting field 'ServiceConfiguration.check_interval_ok'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'check_interval_ok')

        # Deleting field 'ServiceConfiguration.check_interval_provisional'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'check_interval_provisional')

        # Deleting field 'ServiceConfiguration.check_interval_warning'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'check_interval_warning')

        # Deleting field 'ServiceConfiguration.check_interval_down'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'check_interval_down')

        # Deleting field 'ServiceConfiguration.check_interval_unknown'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'check_interval_unknown')

        # Deleting field 'ServiceConfiguration.max_retries'
        db.delete_column('argus_service_configurations_serviceconfiguration', 'max_retries')


    models = {
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'api_can_trigger_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_interval_down': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'check_interval_ok': ('django.db.models.fields.PositiveIntegerField', [], {'default': '900'}),
            'check_interval_provisional': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            'check_interval_unknown': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'check_interval_warning': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_retries': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'blank': 'True'}),
            'passive_check_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passive_check_api_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'passive_check_ips': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['argus_service_configurations']