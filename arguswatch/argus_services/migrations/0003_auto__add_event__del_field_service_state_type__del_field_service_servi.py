# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('argus_services_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('old_state_provisional', self.gf('django.db.models.fields.BooleanField')()),
            ('new_state', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('new_state_provisional', self.gf('django.db.models.fields.BooleanField')()),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('message', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('argus_services', ['Event'])

        # Deleting field 'Service.state_type'
        db.delete_column('argus_services_service', 'state_type')

        # Deleting field 'Service.service_config'
        db.delete_column('argus_services_service', 'service_config_id')

        # Adding field 'Service.config'
        db.add_column('argus_services_service', 'config',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', default=1, to=orm['argus_service_configurations.ServiceConfiguration']),
                      keep_default=False)

        # Adding field 'Service.state_provisional'
        db.add_column('argus_services_service', 'state_provisional',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Service.state_message'
        db.add_column('argus_services_service', 'state_message',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'Service.state'
        db.alter_column('argus_services_service', 'state', self.gf('django.db.models.fields.CharField')(max_length=20))

    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('argus_services_event')

        # Adding field 'Service.state_type'
        db.add_column('argus_services_service', 'state_type',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Service.service_config'
        raise RuntimeError("Cannot reverse this migration. 'Service.service_config' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Service.service_config'
        db.add_column('argus_services_service', 'service_config',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', to=orm['argus_service_configurations.ServiceConfiguration']),
                      keep_default=False)

        # Deleting field 'Service.config'
        db.delete_column('argus_services_service', 'config_id')

        # Deleting field 'Service.state_provisional'
        db.delete_column('argus_services_service', 'state_provisional')

        # Deleting field 'Service.state_message'
        db.delete_column('argus_services_service', 'state_message')


        # Changing field 'Service.state'
        db.alter_column('argus_services_service', 'state', self.gf('django.db.models.fields.PositiveSmallIntegerField')())

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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'passive_check_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passive_check_api_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'passive_check_ips': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'argus_services.contact': {
            'Meta': {'object_name': 'Contact'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_services.ContactGroup']", 'null': 'True', 'related_name': "'contacts'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'argus_services.contactgroup': {
            'Meta': {'object_name': 'ContactGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'argus_services.event': {
            'Meta': {'object_name': 'Event'},
            'event': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'new_state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'new_state_provisional': ('django.db.models.fields.BooleanField', [], {}),
            'old_state': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'old_state_provisional': ('django.db.models.fields.BooleanField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'argus_services.httppluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'HttpPluginConfig'},
            'response_code': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'response_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'argus_services.imappluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'IMAPPluginConfig'},
            'auth_method': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'check_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '143'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'argus_services.nooppluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'NoOpPluginConfig'},
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"})
        },
        'argus_services.pingpluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'PingPluginConfig'},
            'cmd': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'argus_services.poppluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'POPPluginConfig'},
            'auth_method': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'check_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '110'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'timeout': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'argus_services.portpluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'PortPluginConfig'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '80'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'argus_services.service': {
            'Meta': {'object_name': 'Service'},
            'celery_task_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'config': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': "orm['argus_service_configurations.ServiceConfiguration']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['argus_services.ServiceGroup']", 'null': 'True', 'related_name': "'services'", 'symmetrical': 'False', 'blank': 'True'}),
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'}),
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
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['argus_services.ServiceGroup']", 'null': 'True', 'related_name': "'children'", 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'argus_services.servicepluginconfiguration': {
            'Meta': {'object_name': 'ServicePluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'polymorphic_argus_services.servicepluginconfiguration_set'", 'to': "orm['contenttypes.ContentType']"})
        },
        'argus_services.smtppluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'SMTPPluginConfig'},
            'auth_method': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'check_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '25'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'timeout': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'argus_services.sqlquerypluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'SQLQueryPluginConfig'},
            'database': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'database_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3306'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'query_eval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query_replace_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query_replace_timedelta': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'validation': ('django.db.models.fields.TextField', [], {}),
            'validation_mode': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'argus_services.sshcmdpluginconfig': {
            'Meta': {'_ormbases': ['argus_services.SSHPluginConfig'], 'object_name': 'SSHCmdPluginConfig'},
            'command': ('django.db.models.fields.TextField', [], {}),
            'sshpluginconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.SSHPluginConfig']"})
        },
        'argus_services.sshpluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'SSHPluginConfig'},
            'auth_method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '22'}),
            'private_key': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'primary_key': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']"}),
            'timeout': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'related_name': "'user_set'", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'unique_together': "(('app_label', 'model'),)", 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_services']