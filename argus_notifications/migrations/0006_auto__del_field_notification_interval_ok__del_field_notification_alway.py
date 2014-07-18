# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Notification.interval_ok'
        db.delete_column('argus_notifications_notification', 'interval_ok')

        # Deleting field 'Notification.always_on_recovery_hard'
        db.delete_column('argus_notifications_notification', 'always_on_recovery_hard')

        # Deleting field 'Notification.interval_hard_warning'
        db.delete_column('argus_notifications_notification', 'interval_hard_warning')

        # Adding field 'Notification.interval_remains_up'
        db.add_column('argus_notifications_notification', 'interval_remains_up',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=86400),
                      keep_default=False)

        # Adding field 'Notification.interval_warning_hard'
        db.add_column('argus_notifications_notification', 'interval_warning_hard',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=3600),
                      keep_default=False)

        # Adding field 'Notification.interval_critical_hard'
        db.add_column('argus_notifications_notification', 'interval_critical_hard',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)

        # Adding field 'Notification.interval_recovery_hard'
        db.add_column('argus_notifications_notification', 'interval_recovery_hard',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Notification.interval_ok'
        db.add_column('argus_notifications_notification', 'interval_ok',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Notification.always_on_recovery_hard'
        db.add_column('argus_notifications_notification', 'always_on_recovery_hard',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.interval_hard_warning'
        db.add_column('argus_notifications_notification', 'interval_hard_warning',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=3600),
                      keep_default=False)

        # Deleting field 'Notification.interval_remains_up'
        db.delete_column('argus_notifications_notification', 'interval_remains_up')

        # Deleting field 'Notification.interval_warning_hard'
        db.delete_column('argus_notifications_notification', 'interval_warning_hard')

        # Deleting field 'Notification.interval_critical_hard'
        db.delete_column('argus_notifications_notification', 'interval_critical_hard')

        # Deleting field 'Notification.interval_recovery_hard'
        db.delete_column('argus_notifications_notification', 'interval_recovery_hard')


    models = {
        'argus_notifications.emailpluginconfig': {
            'Meta': {'_ormbases': ['argus_notifications.NotificationPluginConfiguration'], 'object_name': 'EmailPluginConfig'},
            'emails': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notificationpluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_notifications.NotificationPluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'argus_notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1800'}),
            'interval_critical_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'interval_recovery_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'interval_remains_up': ('django.db.models.fields.PositiveIntegerField', [], {'default': '86400'}),
            'interval_warning_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600'}),
            'last_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'on_critical_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_critical_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_recovery_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_recovery_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_remains_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_warning_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_warning_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_notifications.NotificationPluginConfiguration']", 'null': 'True', 'related_name': "'notification'"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_service_configurations.ServiceConfiguration']", 'related_name': "'notifications'"})
        },
        'argus_notifications.notificationpluginconfiguration': {
            'Meta': {'object_name': 'NotificationPluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'related_name': "'polymorphic_argus_notifications.notificationpluginconfiguration_set'"})
        },
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'check_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_retries_soft': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'max_length': '50'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {'default': '120'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_notifications']