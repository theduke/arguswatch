# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'NotificationPluginConfiguration'
        db.create_table('argus_notifications_notificationpluginconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['contenttypes.ContentType'], related_name='polymorphic_argus_notifications.notificationpluginconfiguration_set')),
        ))
        db.send_create_signal('argus_notifications', ['NotificationPluginConfiguration'])

        # Adding model 'EmailPluginConfig'
        db.create_table('argus_notifications_emailpluginconfig', (
            ('notificationpluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['argus_notifications.NotificationPluginConfiguration'], unique=True, primary_key=True)),
            ('emails', self.gf('django.db.models.fields.TextField')()),
            ('subject', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('argus_notifications', ['EmailPluginConfig'])

        # Adding model 'Notification'
        db.create_table('argus_notifications_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['argus_service_configurations.ServiceConfiguration'], related_name='notifications')),
            ('plugin', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('plugin_config', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['argus_notifications.NotificationPluginConfiguration'], related_name='notification')),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('on_remains_up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('on_critical_soft', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('on_warning_soft', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('on_recovery_soft', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('on_critical_hard', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('on_warning_hard', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('on_recovery_hard', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('interval', self.gf('django.db.models.fields.PositiveIntegerField')(default=1800)),
            ('interval_remains_up', self.gf('django.db.models.fields.PositiveIntegerField')(default=86400)),
            ('interval_warning_hard', self.gf('django.db.models.fields.PositiveIntegerField')(default=3600)),
            ('interval_critical_hard', self.gf('django.db.models.fields.PositiveIntegerField')(default=600)),
            ('interval_recovery_hard', self.gf('django.db.models.fields.PositiveIntegerField')(default=600)),
        ))
        db.send_create_signal('argus_notifications', ['Notification'])

        # Adding model 'ServiceNotifications'
        db.create_table('argus_notifications_servicenotifications', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['argus_notifications.Notification'], related_name='service_notifications')),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['argus_services.Service'], related_name='notifications')),
            ('last_sent', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('argus_notifications', ['ServiceNotifications'])

        # Adding unique constraint on 'ServiceNotifications', fields ['notification', 'service']
        db.create_unique('argus_notifications_servicenotifications', ['notification_id', 'service_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ServiceNotifications', fields ['notification', 'service']
        db.delete_unique('argus_notifications_servicenotifications', ['notification_id', 'service_id'])

        # Deleting model 'NotificationPluginConfiguration'
        db.delete_table('argus_notifications_notificationpluginconfiguration')

        # Deleting model 'EmailPluginConfig'
        db.delete_table('argus_notifications_emailpluginconfig')

        # Deleting model 'Notification'
        db.delete_table('argus_notifications_notification')

        # Deleting model 'ServiceNotifications'
        db.delete_table('argus_notifications_servicenotifications')


    models = {
        'argus_notifications.emailpluginconfig': {
            'Meta': {'_ormbases': ['argus_notifications.NotificationPluginConfiguration'], 'object_name': 'EmailPluginConfig'},
            'emails': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notificationpluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_notifications.NotificationPluginConfiguration']", 'unique': 'True', 'primary_key': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'on_critical_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_critical_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_recovery_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_recovery_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_remains_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'on_warning_hard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_warning_soft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['argus_notifications.NotificationPluginConfiguration']", 'related_name': "'notification'"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_service_configurations.ServiceConfiguration']", 'related_name': "'notifications'"})
        },
        'argus_notifications.notificationpluginconfiguration': {
            'Meta': {'object_name': 'NotificationPluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['contenttypes.ContentType']", 'related_name': "'polymorphic_argus_notifications.notificationpluginconfiguration_set'"})
        },
        'argus_notifications.servicenotifications': {
            'Meta': {'object_name': 'ServiceNotifications', 'unique_together': "(('notification', 'service'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent': ('django.db.models.fields.DateTimeField', [], {}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_notifications.Notification']", 'related_name': "'service_notifications'"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_services.Service']", 'related_name': "'notifications'"})
        },
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'api_can_trigger_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_retries_soft': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'unique': 'True', 'max_length': '50'}),
            'passive_check_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passive_check_api_key': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100'}),
            'passive_check_ips': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {'default': '120'})
        },
        'argus_services.service': {
            'Meta': {'object_name': 'Service'},
            'celery_task_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '100', 'default': "''"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'blank': 'True', 'to': "orm['argus_services.ServiceGroup']", 'symmetrical': 'False', 'related_name': "'services'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_issued': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_ok': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_retries': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['argus_services.Service']", 'related_name': "'children'"}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']", 'related_name': "'service'"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_service_configurations.ServiceConfiguration']", 'related_name': "'services'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'state_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'})
        },
        'argus_services.servicegroup': {
            'Meta': {'object_name': 'ServiceGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'blank': 'True', 'to': "orm['argus_services.ServiceGroup']", 'related_name': "'children'"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'argus_services.servicepluginconfiguration': {
            'Meta': {'object_name': 'ServicePluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['contenttypes.ContentType']", 'related_name': "'polymorphic_argus_services.servicepluginconfiguration_set'"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']", 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']", 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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