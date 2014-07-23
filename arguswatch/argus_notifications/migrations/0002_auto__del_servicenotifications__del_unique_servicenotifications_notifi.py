# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ServiceNotifications', fields ['notification', 'service']
        db.delete_unique('argus_notifications_servicenotifications', ['notification_id', 'service_id'])

        # Deleting model 'ServiceNotifications'
        db.delete_table('argus_notifications_servicenotifications')

        # Adding model 'NotificationHistory'
        db.create_table('argus_notifications_notificationhistory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(related_name='histories', to=orm['argus_notifications.Notification'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['argus_services.Service'])),
            ('last_sent', self.gf('django.db.models.fields.DateTimeField')()),
            ('last_state_change_provisional', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_state_stays_provisional', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_state_change', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_state_stays', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_change_ok', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('argus_notifications', ['NotificationHistory'])

        # Adding unique constraint on 'NotificationHistory', fields ['notification', 'service']
        db.create_unique('argus_notifications_notificationhistory', ['notification_id', 'service_id'])

        # Deleting field 'Notification.interval_recovery_hard'
        db.delete_column('argus_notifications_notification', 'interval_recovery_hard')

        # Deleting field 'Notification.on_warning_hard'
        db.delete_column('argus_notifications_notification', 'on_warning_hard')

        # Deleting field 'Notification.interval'
        db.delete_column('argus_notifications_notification', 'interval')

        # Deleting field 'Notification.on_critical_hard'
        db.delete_column('argus_notifications_notification', 'on_critical_hard')

        # Deleting field 'Notification.on_recovery_hard'
        db.delete_column('argus_notifications_notification', 'on_recovery_hard')

        # Deleting field 'Notification.on_warning_soft'
        db.delete_column('argus_notifications_notification', 'on_warning_soft')

        # Deleting field 'Notification.interval_critical_hard'
        db.delete_column('argus_notifications_notification', 'interval_critical_hard')

        # Deleting field 'Notification.service_config'
        db.delete_column('argus_notifications_notification', 'service_config_id')

        # Deleting field 'Notification.interval_remains_up'
        db.delete_column('argus_notifications_notification', 'interval_remains_up')

        # Deleting field 'Notification.on_critical_soft'
        db.delete_column('argus_notifications_notification', 'on_critical_soft')

        # Deleting field 'Notification.on_remains_up'
        db.delete_column('argus_notifications_notification', 'on_remains_up')

        # Deleting field 'Notification.interval_warning_hard'
        db.delete_column('argus_notifications_notification', 'interval_warning_hard')

        # Deleting field 'Notification.on_recovery_soft'
        db.delete_column('argus_notifications_notification', 'on_recovery_soft')

        # Adding field 'Notification.config'
        db.add_column('argus_notifications_notification', 'config',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', default=1, to=orm['argus_service_configurations.ServiceConfiguration']),
                      keep_default=False)

        # Adding field 'Notification.interval_state_change_provisional'
        db.add_column('argus_notifications_notification', 'interval_state_change_provisional',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=-1),
                      keep_default=False)

        # Adding field 'Notification.interval_state_stays_provisional'
        db.add_column('argus_notifications_notification', 'interval_state_stays_provisional',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=-1),
                      keep_default=False)

        # Adding field 'Notification.interval_state_change'
        db.add_column('argus_notifications_notification', 'interval_state_change',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=60),
                      keep_default=False)

        # Adding field 'Notification.interval_state_stays'
        db.add_column('argus_notifications_notification', 'interval_state_stays',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=21600),
                      keep_default=False)

        # Adding field 'Notification.interval_change_ok'
        db.add_column('argus_notifications_notification', 'interval_change_ok',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Notification.interval_hard'
        db.add_column('argus_notifications_notification', 'interval_hard',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=5),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'NotificationHistory', fields ['notification', 'service']
        db.delete_unique('argus_notifications_notificationhistory', ['notification_id', 'service_id'])

        # Adding model 'ServiceNotifications'
        db.create_table('argus_notifications_servicenotifications', (
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['argus_services.Service'])),
            ('notification', self.gf('django.db.models.fields.related.ForeignKey')(related_name='service_notifications', to=orm['argus_notifications.Notification'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_sent', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('argus_notifications', ['ServiceNotifications'])

        # Adding unique constraint on 'ServiceNotifications', fields ['notification', 'service']
        db.create_unique('argus_notifications_servicenotifications', ['notification_id', 'service_id'])

        # Deleting model 'NotificationHistory'
        db.delete_table('argus_notifications_notificationhistory')

        # Adding field 'Notification.interval_recovery_hard'
        db.add_column('argus_notifications_notification', 'interval_recovery_hard',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)

        # Adding field 'Notification.on_warning_hard'
        db.add_column('argus_notifications_notification', 'on_warning_hard',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.interval'
        db.add_column('argus_notifications_notification', 'interval',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1800),
                      keep_default=False)

        # Adding field 'Notification.on_critical_hard'
        db.add_column('argus_notifications_notification', 'on_critical_hard',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.on_recovery_hard'
        db.add_column('argus_notifications_notification', 'on_recovery_hard',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Notification.on_warning_soft'
        db.add_column('argus_notifications_notification', 'on_warning_soft',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.interval_critical_hard'
        db.add_column('argus_notifications_notification', 'interval_critical_hard',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=600),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Notification.service_config'
        raise RuntimeError("Cannot reverse this migration. 'Notification.service_config' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Notification.service_config'
        db.add_column('argus_notifications_notification', 'service_config',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='notifications', to=orm['argus_service_configurations.ServiceConfiguration']),
                      keep_default=False)

        # Adding field 'Notification.interval_remains_up'
        db.add_column('argus_notifications_notification', 'interval_remains_up',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=86400),
                      keep_default=False)

        # Adding field 'Notification.on_critical_soft'
        db.add_column('argus_notifications_notification', 'on_critical_soft',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.on_remains_up'
        db.add_column('argus_notifications_notification', 'on_remains_up',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Notification.interval_warning_hard'
        db.add_column('argus_notifications_notification', 'interval_warning_hard',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=3600),
                      keep_default=False)

        # Adding field 'Notification.on_recovery_soft'
        db.add_column('argus_notifications_notification', 'on_recovery_soft',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Notification.config'
        db.delete_column('argus_notifications_notification', 'config_id')

        # Deleting field 'Notification.interval_state_change_provisional'
        db.delete_column('argus_notifications_notification', 'interval_state_change_provisional')

        # Deleting field 'Notification.interval_state_stays_provisional'
        db.delete_column('argus_notifications_notification', 'interval_state_stays_provisional')

        # Deleting field 'Notification.interval_state_change'
        db.delete_column('argus_notifications_notification', 'interval_state_change')

        # Deleting field 'Notification.interval_state_stays'
        db.delete_column('argus_notifications_notification', 'interval_state_stays')

        # Deleting field 'Notification.interval_change_ok'
        db.delete_column('argus_notifications_notification', 'interval_change_ok')

        # Deleting field 'Notification.interval_hard'
        db.delete_column('argus_notifications_notification', 'interval_hard')


    models = {
        'argus_notifications.emailpluginconfig': {
            'Meta': {'object_name': 'EmailPluginConfig', '_ormbases': ['argus_notifications.NotificationPluginConfiguration']},
            'emails': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'notificationpluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_notifications.NotificationPluginConfiguration']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'argus_notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['argus_service_configurations.ServiceConfiguration']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval_change_ok': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'interval_hard': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'interval_state_change': ('django.db.models.fields.SmallIntegerField', [], {'default': '60'}),
            'interval_state_change_provisional': ('django.db.models.fields.SmallIntegerField', [], {'default': '-1'}),
            'interval_state_stays': ('django.db.models.fields.SmallIntegerField', [], {'default': '21600'}),
            'interval_state_stays_provisional': ('django.db.models.fields.SmallIntegerField', [], {'default': '-1'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification'", 'null': 'True', 'to': "orm['argus_notifications.NotificationPluginConfiguration']"})
        },
        'argus_notifications.notificationhistory': {
            'Meta': {'object_name': 'NotificationHistory', 'unique_together': "(('notification', 'service'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_change_ok': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_sent': ('django.db.models.fields.DateTimeField', [], {}),
            'last_state_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_change_provisional': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_stays': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_stays_provisional': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'notification': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'histories'", 'to': "orm['argus_notifications.Notification']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['argus_services.Service']"})
        },
        'argus_notifications.notificationpluginconfiguration': {
            'Meta': {'object_name': 'NotificationPluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_argus_notifications.notificationpluginconfiguration_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"})
        },
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'passive_check_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passive_check_api_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'passive_check_ips': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'argus_services.service': {
            'Meta': {'object_name': 'Service'},
            'celery_task_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': "orm['argus_service_configurations.ServiceConfiguration']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'services'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['argus_services.ServiceGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_issued': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_ok': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_retries': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['argus_services.Service']"}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service'", 'null': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'unknown'"}),
            'state_message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state_provisional': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'argus_services.servicegroup': {
            'Meta': {'object_name': 'ServiceGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'related_name': "'children'", 'blank': 'True', 'to': "orm['argus_services.ServiceGroup']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'argus_services.servicepluginconfiguration': {
            'Meta': {'object_name': 'ServicePluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_argus_services.servicepluginconfiguration_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['auth.Permission']"})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'unique_together': "(('content_type', 'codename'),)", 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_notifications']