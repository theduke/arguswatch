# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ServiceGroup.description'
        db.add_column('argus_services_servicegroup', 'description',
                      self.gf('django.db.models.fields.TextField')(blank=True, default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ServiceGroup.description'
        db.delete_column('argus_services_servicegroup', 'description')


    models = {
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
        'argus_services.contact': {
            'Meta': {'object_name': 'Contact'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['argus_services.ContactGroup']", 'related_name': "'contacts'", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'argus_services.contactgroup': {
            'Meta': {'object_name': 'ContactGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'argus_services.httppluginconfig': {
            'Meta': {'object_name': 'HttpPluginConfig', '_ormbases': ['argus_services.ServicePluginConfiguration']},
            'response_code': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'response_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'unique': 'True', 'primary_key': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'argus_services.service': {
            'Meta': {'object_name': 'Service'},
            'celery_task_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['argus_services.ServiceGroup']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_issued': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_ok': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_retries': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['argus_services.Service']", 'related_name': "'children'", 'null': 'True'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'service'", 'to': "orm['argus_services.ServicePluginConfiguration']", 'null': 'True'}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': "orm['argus_service_configurations.ServiceConfiguration']"}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'state_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'argus_services.servicegroup': {
            'Meta': {'object_name': 'ServiceGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'to': "orm['argus_services.ServiceGroup']", 'related_name': "'children'", 'null': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'argus_services.servicepluginconfiguration': {
            'Meta': {'object_name': 'ServicePluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'polymorphic_argus_services.servicepluginconfiguration_set'", 'to': "orm['contenttypes.ContentType']", 'null': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.Permission']"})
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
            'Meta': {'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_services']