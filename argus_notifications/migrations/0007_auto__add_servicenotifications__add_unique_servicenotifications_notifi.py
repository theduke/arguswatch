# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ServiceNotifications'
        db.create_table('argus_notifications_servicenotifications', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(related_name='service_notifications', to=orm['argus_notifications.Notification'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='service_notifications', to=orm['argus_services.Service'])),
            ('last_sent', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('argus_notifications', ['ServiceNotifications'])

        # Adding unique constraint on 'ServiceNotifications', fields ['notification', 'service']
        db.create_unique('argus_notifications_servicenotifications', ['notification_id', 'service_id'])

        # Deleting field 'Notification.last_sent'
        db.delete_column('argus_notifications_notification', 'last_sent')


    def backwards(self, orm):
        # Removing unique constraint on 'ServiceNotifications', fields ['notification', 'service']
        db.delete_unique('argus_notifications_servicenotifications', ['notification_id', 'service_id'])

        # Deleting model 'ServiceNotifications'
        db.delete_table('argus_notifications_servicenotifications')

        # Adding field 'Notification.last_sent'
        db.add_column('argus_notifications_notification', 'last_sent',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


    models = {
        'argus_notifications.emailpluginconfig': {
            'Meta': {'object_name': 'EmailPluginConfig', '_ormbases': ['argus_notifications.NotificationPluginConfiguration']},
            'emails': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notificationpluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['argus_notifications.NotificationPluginConfiguration']", 'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'on_critical_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_critical_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_recovery_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_recovery_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_remains_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_warning_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_warning_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'notification'", 'to': "orm['argus_notifications.NotificationPluginConfiguration']"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['argus_service_configurations.ServiceConfiguration']"})
        },
        'argus_notifications.notificationpluginconfiguration': {
            'Meta': {'object_name': 'NotificationPluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'polymorphic_argus_notifications.notificationpluginconfiguration_set'", 'to': "orm['contenttypes.ContentType']"})
        },
        'argus_notifications.servicenotifications': {
            'Meta': {'object_name': 'ServiceNotifications', 'unique_together': "(('notification', 'service'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent': ('django.db.models.fields.DateTimeField', [], {}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service_notifications'", 'to': "orm['argus_notifications.Notification']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service_notifications'", 'to': "orm['argus_services.Service']"})
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
        'argus_services.service': {
            'Meta': {'object_name': 'Service'},
            'celery_task_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_issued': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_ok': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_retries': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_services.Service']", 'null': 'True', 'related_name': "'children'", 'blank': 'True'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'service'", 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': "orm['argus_service_configurations.ServiceConfiguration']"}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'state_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'argus_services.servicepluginconfiguration': {
            'Meta': {'object_name': 'ServicePluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'polymorphic_argus_services.servicepluginconfiguration_set'", 'to': "orm['contenttypes.ContentType']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_notifications']