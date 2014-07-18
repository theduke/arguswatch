# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Notification.always_on_hard_recovery'
        db.delete_column('argus_notifications_notification', 'always_on_hard_recovery')

        # Deleting field 'Notification.on_soft_warning'
        db.delete_column('argus_notifications_notification', 'on_soft_warning')

        # Deleting field 'Notification.on_soft_recovery'
        db.delete_column('argus_notifications_notification', 'on_soft_recovery')

        # Deleting field 'Notification.on_hard_critical'
        db.delete_column('argus_notifications_notification', 'on_hard_critical')

        # Deleting field 'Notification.on_soft_critical'
        db.delete_column('argus_notifications_notification', 'on_soft_critical')

        # Deleting field 'Notification.on_ok'
        db.delete_column('argus_notifications_notification', 'on_ok')

        # Deleting field 'Notification.on_hard_warning'
        db.delete_column('argus_notifications_notification', 'on_hard_warning')

        # Deleting field 'Notification.on_hard_recovery'
        db.delete_column('argus_notifications_notification', 'on_hard_recovery')

        # Adding field 'Notification.on_remains_up'
        db.add_column('argus_notifications_notification', 'on_remains_up',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_critical_soft'
        db.add_column('argus_notifications_notification', 'on_critical_soft',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_warning_soft'
        db.add_column('argus_notifications_notification', 'on_warning_soft',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_recovery_soft'
        db.add_column('argus_notifications_notification', 'on_recovery_soft',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_critical_hard'
        db.add_column('argus_notifications_notification', 'on_critical_hard',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.on_warning_hard'
        db.add_column('argus_notifications_notification', 'on_warning_hard',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.on_recovery_hard'
        db.add_column('argus_notifications_notification', 'on_recovery_hard',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.always_on_recovery_hard'
        db.add_column('argus_notifications_notification', 'always_on_recovery_hard',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Notification.always_on_hard_recovery'
        db.add_column('argus_notifications_notification', 'always_on_hard_recovery',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
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

        # Adding field 'Notification.on_soft_critical'
        db.add_column('argus_notifications_notification', 'on_soft_critical',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_ok'
        db.add_column('argus_notifications_notification', 'on_ok',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_hard_warning'
        db.add_column('argus_notifications_notification', 'on_hard_warning',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.on_hard_recovery'
        db.add_column('argus_notifications_notification', 'on_hard_recovery',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Deleting field 'Notification.on_remains_up'
        db.delete_column('argus_notifications_notification', 'on_remains_up')

        # Deleting field 'Notification.on_critical_soft'
        db.delete_column('argus_notifications_notification', 'on_critical_soft')

        # Deleting field 'Notification.on_warning_soft'
        db.delete_column('argus_notifications_notification', 'on_warning_soft')

        # Deleting field 'Notification.on_recovery_soft'
        db.delete_column('argus_notifications_notification', 'on_recovery_soft')

        # Deleting field 'Notification.on_critical_hard'
        db.delete_column('argus_notifications_notification', 'on_critical_hard')

        # Deleting field 'Notification.on_warning_hard'
        db.delete_column('argus_notifications_notification', 'on_warning_hard')

        # Deleting field 'Notification.on_recovery_hard'
        db.delete_column('argus_notifications_notification', 'on_recovery_hard')

        # Deleting field 'Notification.always_on_recovery_hard'
        db.delete_column('argus_notifications_notification', 'always_on_recovery_hard')


    models = {
        'argus_notifications.emailpluginconfig': {
            'Meta': {'_ormbases': ['argus_notifications.NotificationPluginConfiguration'], 'object_name': 'EmailPluginConfig'},
            'emails': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notificationpluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['argus_notifications.NotificationPluginConfiguration']", 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'argus_notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'always_on_recovery_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '300'}),
            'interval_hard_warning': ('django.db.models.fields.PositiveIntegerField', [], {'default': '3600'}),
            'interval_ok': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'blank': 'True', 'max_length': '50'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {'default': '120'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_notifications']