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
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, related_name='polymorphic_argus_notifications.notificationpluginconfiguration_set')),
        ))
        db.send_create_signal('argus_notifications', ['NotificationPluginConfiguration'])

        # Adding model 'Notification'
        db.create_table('argus_notifications_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['argus_service_configurations.ServiceConfiguration'], related_name='notifications')),
            ('plugin', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('plugin_config', self.gf('django.db.models.fields.related.OneToOneField')(null=True, to=orm['argus_notifications.NotificationPluginConfiguration'], unique=True, related_name='notification')),
        ))
        db.send_create_signal('argus_notifications', ['Notification'])


    def backwards(self, orm):
        # Deleting model 'NotificationPluginConfiguration'
        db.delete_table('argus_notifications_notificationpluginconfiguration')

        # Deleting model 'Notification'
        db.delete_table('argus_notifications_notification')


    models = {
        'argus_notifications.notification': {
            'Meta': {'object_name': 'Notification'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.OneToOneField', [], {'null': 'True', 'to': "orm['argus_notifications.NotificationPluginConfiguration']", 'unique': 'True', 'related_name': "'notification'"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_service_configurations.ServiceConfiguration']", 'related_name': "'notifications'"})
        },
        'argus_notifications.notificationpluginconfiguration': {
            'Meta': {'object_name': 'NotificationPluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'related_name': "'polymorphic_argus_notifications.notificationpluginconfiguration_set'"})
        },
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'check_interval': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {}),
            'max_retries_soft': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True', 'unique': 'True'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_notifications']