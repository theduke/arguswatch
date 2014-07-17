# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Notification.name'
        db.add_column('argus_notifications_notification', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=100, default=''),
                      keep_default=False)

        # Adding field 'Notification.description'
        db.add_column('argus_notifications_notification', 'description',
                      self.gf('django.db.models.fields.TextField')(blank=True, default=''),
                      keep_default=False)

        # Adding field 'Notification.on_ok'
        db.add_column('argus_notifications_notification', 'on_ok',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_soft_critical'
        db.add_column('argus_notifications_notification', 'on_soft_critical',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_soft_warning'
        db.add_column('argus_notifications_notification', 'on_soft_warning',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_soft_recovery'
        db.add_column('argus_notifications_notification', 'on_soft_recovery',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_hard_critical'
        db.add_column('argus_notifications_notification', 'on_hard_critical',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.on_hard_warning'
        db.add_column('argus_notifications_notification', 'on_hard_warning',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.on_hard_recovery'
        db.add_column('argus_notifications_notification', 'on_hard_recovery',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.always_on_hard_recovery'
        db.add_column('argus_notifications_notification', 'always_on_hard_recovery',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.interval'
        db.add_column('argus_notifications_notification', 'interval',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=300),
                      keep_default=False)

        # Adding field 'Notification.interval_ok'
        db.add_column('argus_notifications_notification', 'interval_ok',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Notification.interval_hard_warning'
        db.add_column('argus_notifications_notification', 'interval_hard_warning',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=3600),
                      keep_default=False)

        # Adding field 'Notification.last_sent'
        db.add_column('argus_notifications_notification', 'last_sent',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Notification.name'
        db.delete_column('argus_notifications_notification', 'name')

        # Deleting field 'Notification.description'
        db.delete_column('argus_notifications_notification', 'description')

        # Deleting field 'Notification.on_ok'
        db.delete_column('argus_notifications_notification', 'on_ok')

        # Deleting field 'Notification.on_soft_critical'
        db.delete_column('argus_notifications_notification', 'on_soft_critical')

        # Deleting field 'Notification.on_soft_warning'
        db.delete_column('argus_notifications_notification', 'on_soft_warning')

        # Deleting field 'Notification.on_soft_recovery'
        db.delete_column('argus_notifications_notification', 'on_soft_recovery')

        # Deleting field 'Notification.on_hard_critical'
        db.delete_column('argus_notifications_notification', 'on_hard_critical')

        # Deleting field 'Notification.on_hard_warning'
        db.delete_column('argus_notifications_notification', 'on_hard_warning')

        # Deleting field 'Notification.on_hard_recovery'
        db.delete_column('argus_notifications_notification', 'on_hard_recovery')

        # Deleting field 'Notification.always_on_hard_recovery'
        db.delete_column('argus_notifications_notification', 'always_on_hard_recovery')

        # Deleting field 'Notification.interval'
        db.delete_column('argus_notifications_notification', 'interval')

        # Deleting field 'Notification.interval_ok'
        db.delete_column('argus_notifications_notification', 'interval_ok')

        # Deleting field 'Notification.interval_hard_warning'
        db.delete_column('argus_notifications_notification', 'interval_hard_warning')

        # Deleting field 'Notification.last_sent'
        db.delete_column('argus_notifications_notification', 'last_sent')


    models = {
        'argus_notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'always_on_hard_recovery': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            'interval_hard_warning': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600'}),
            'interval_ok': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'last_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'on_hard_critical': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_hard_recovery': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_hard_warning': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_soft_critical': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_soft_recovery': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_soft_warning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'to': "orm['argus_notifications.NotificationPluginConfiguration']", 'unique': 'True', 'related_name': "'notification'"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_service_configurations.ServiceConfiguration']", 'related_name': "'notifications'"})
        },
        'argus_notifications.notificationpluginconfiguration': {
            'Meta': {'object_name': 'NotificationPluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['contenttypes.ContentType']", 'related_name': "'polymorphic_argus_notifications.notificationpluginconfiguration_set'"})
        },
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'check_interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {}),
            'max_retries_soft': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'max_length': '50'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_notifications']