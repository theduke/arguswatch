# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SSHPluginConfig'
        db.create_table('argus_services_sshpluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['argus_services.ServicePluginConfiguration'], primary_key=True, unique=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=22)),
            ('auth_method', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('username', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('private_key', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('timeout', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=30)),
        ))
        db.send_create_signal('argus_services', ['SSHPluginConfig'])

        # Adding model 'SSHCmdPluginConfig'
        db.create_table('argus_services_sshcmdpluginconfig', (
            ('sshpluginconfig_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['argus_services.SSHPluginConfig'], primary_key=True, unique=True)),
            ('command', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('argus_services', ['SSHCmdPluginConfig'])

        # Adding model 'POPPluginConfig'
        db.create_table('argus_services_poppluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['argus_services.ServicePluginConfiguration'], primary_key=True, unique=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=110)),
            ('check_authentication', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auth_method', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('username', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('timeout', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=30)),
        ))
        db.send_create_signal('argus_services', ['POPPluginConfig'])

        # Adding model 'IMAPPluginConfig'
        db.create_table('argus_services_imappluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['argus_services.ServicePluginConfiguration'], primary_key=True, unique=True)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=143)),
            ('check_authentication', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auth_method', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('username', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
        ))
        db.send_create_signal('argus_services', ['IMAPPluginConfig'])

        # Adding model 'SMTPPluginConfig'
        db.create_table('argus_services_smtppluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['argus_services.ServicePluginConfiguration'], primary_key=True, unique=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=110)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('check_authentication', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auth_method', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('username', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('password', self.gf('django.db.models.fields.CharField')(blank=True, max_length=255)),
            ('timeout', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=30)),
        ))
        db.send_create_signal('argus_services', ['SMTPPluginConfig'])


    def backwards(self, orm):
        # Deleting model 'SSHPluginConfig'
        db.delete_table('argus_services_sshpluginconfig')

        # Deleting model 'SSHCmdPluginConfig'
        db.delete_table('argus_services_sshcmdpluginconfig')

        # Deleting model 'POPPluginConfig'
        db.delete_table('argus_services_poppluginconfig')

        # Deleting model 'IMAPPluginConfig'
        db.delete_table('argus_services_imappluginconfig')

        # Deleting model 'SMTPPluginConfig'
        db.delete_table('argus_services_smtppluginconfig')


    models = {
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
        'argus_services.contact': {
            'Meta': {'object_name': 'Contact'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_services.ContactGroup']", 'null': 'True', 'blank': 'True', 'related_name': "'contacts'"}),
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
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'HttpPluginConfig'},
            'response_code': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'response_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'argus_services.imappluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'IMAPPluginConfig'},
            'auth_method': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'check_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '143'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'argus_services.nooppluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'NoOpPluginConfig'},
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'})
        },
        'argus_services.pingpluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'PingPluginConfig'},
            'cmd': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'blank': 'True', 'max_length': '15'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'argus_services.poppluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'POPPluginConfig'},
            'auth_method': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'check_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '110'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'timeout': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'argus_services.portpluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'PortPluginConfig'},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '80'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'argus_services.service': {
            'Meta': {'object_name': 'Service'},
            'celery_task_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '100'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['argus_services.ServiceGroup']", 'null': 'True', 'blank': 'True', 'related_name': "'services'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_issued': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_ok': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_retries': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_services.Service']", 'null': 'True', 'blank': 'True', 'related_name': "'children'"}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'null': 'True', 'related_name': "'service'"}),
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
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['argus_services.ServiceGroup']", 'null': 'True', 'blank': 'True', 'related_name': "'children'"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'argus_services.servicepluginconfiguration': {
            'Meta': {'object_name': 'ServicePluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'related_name': "'polymorphic_argus_services.servicepluginconfiguration_set'"})
        },
        'argus_services.smtppluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'SMTPPluginConfig'},
            'auth_method': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'check_authentication': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '110'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'timeout': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'argus_services.sqlquerypluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'SQLQueryPluginConfig'},
            'database': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'database_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3306'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'query_eval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query_replace_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query_replace_timedelta': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'validation': ('django.db.models.fields.TextField', [], {}),
            'validation_mode': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'argus_services.sshcmdpluginconfig': {
            'Meta': {'_ormbases': ['argus_services.SSHPluginConfig'], 'object_name': 'SSHCmdPluginConfig'},
            'command': ('django.db.models.fields.TextField', [], {}),
            'sshpluginconfig_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.SSHPluginConfig']", 'primary_key': 'True', 'unique': 'True'})
        },
        'argus_services.sshpluginconfig': {
            'Meta': {'_ormbases': ['argus_services.ServicePluginConfiguration'], 'object_name': 'SSHPluginConfig'},
            'auth_method': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '22'}),
            'private_key': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True', 'unique': 'True'}),
            'timeout': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '30'}),
            'username': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '255'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'related_name': "'user_set'", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['argus_services']