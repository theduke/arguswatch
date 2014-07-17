# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailPluginConfig'
        db.create_table('argus_notifications_emailpluginconfig', (
            ('notificationpluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, primary_key=True, to=orm['argus_notifications.NotificationPluginConfiguration'])),
            ('emails', self.gf('django.db.models.fields.TextField')()),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('argus_notifications', ['EmailPluginConfig'])


    def backwards(self, orm):
        # Deleting model 'EmailPluginConfig'
        db.delete_table('argus_notifications_emailpluginconfig')


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
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification'", 'null': 'True', 'to': "orm['argus_notifications.NotificationPluginConfiguration']"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notifications'", 'to': "orm['argus_service_configurations.ServiceConfiguration']"})
        },
        'argus_notifications.notificationpluginconfiguration': {
            'Meta': {'object_name': 'NotificationPluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_argus_notifications.notificationpluginconfiguration_set'", 'null': 'True', 'to': "orm['contenttypes.ContentType']"})
        },
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'check_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_retries_soft': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {'default': '120'})
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