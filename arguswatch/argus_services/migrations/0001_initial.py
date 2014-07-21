# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContactGroup'
        db.create_table('argus_services_contactgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('argus_services', ['ContactGroup'])

        # Adding model 'Contact'
        db.create_table('argus_services_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['argus_services.ContactGroup'], blank=True, related_name='contacts')),
        ))
        db.send_create_signal('argus_services', ['Contact'])

        # Adding model 'ServicePluginConfiguration'
        db.create_table('argus_services_servicepluginconfiguration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['contenttypes.ContentType'], related_name='polymorphic_argus_services.servicepluginconfiguration_set')),
        ))
        db.send_create_signal('argus_services', ['ServicePluginConfiguration'])

        # Adding model 'HttpPluginConfig'
        db.create_table('argus_services_httppluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['argus_services.ServicePluginConfiguration'], primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('timeout', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('response_code', self.gf('django.db.models.fields.IntegerField')(default=200)),
            ('response_text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('argus_services', ['HttpPluginConfig'])

        # Adding model 'PingPluginConfig'
        db.create_table('argus_services_pingpluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['argus_services.ServicePluginConfiguration'], primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(null=True, max_length=15, blank=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('timeout', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('cmd', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('argus_services', ['PingPluginConfig'])

        # Adding model 'PortPluginConfig'
        db.create_table('argus_services_portpluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['argus_services.ServicePluginConfiguration'], primary_key=True)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=80)),
            ('timeout', self.gf('django.db.models.fields.IntegerField')(default=10)),
        ))
        db.send_create_signal('argus_services', ['PortPluginConfig'])

        # Adding model 'NoOpPluginConfig'
        db.create_table('argus_services_nooppluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['argus_services.ServicePluginConfiguration'], primary_key=True)),
        ))
        db.send_create_signal('argus_services', ['NoOpPluginConfig'])

        # Adding model 'SQLQueryPluginConfig'
        db.create_table('argus_services_sqlquerypluginconfig', (
            ('servicepluginconfiguration_ptr', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['argus_services.ServicePluginConfiguration'], primary_key=True)),
            ('database_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('port', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=3306)),
            ('database', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('query', self.gf('django.db.models.fields.TextField')()),
            ('query_replace_time', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('query_replace_timedelta', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('query_eval', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('validation_mode', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('validation', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('argus_services', ['SQLQueryPluginConfig'])

        # Adding model 'ServiceGroup'
        db.create_table('argus_services_servicegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['argus_services.ServiceGroup'], blank=True, related_name='children')),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('argus_services', ['ServiceGroup'])

        # Adding model 'Service'
        db.create_table('argus_services_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['argus_services.Service'], blank=True, related_name='children')),
            ('plugin', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('plugin_config', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['argus_services.ServicePluginConfiguration'], related_name='service')),
            ('service_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['argus_service_configurations.ServiceConfiguration'], related_name='services')),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('state_type', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('state', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('last_issued', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('celery_task_id', self.gf('django.db.models.fields.CharField')(max_length=100, default='', blank=True)),
            ('last_checked', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_ok', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('last_state_change', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('num_retries', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('argus_services', ['Service'])

        # Adding M2M table for field groups on 'Service'
        m2m_table_name = db.shorten_name('argus_services_service_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('service', models.ForeignKey(orm['argus_services.service'], null=False)),
            ('servicegroup', models.ForeignKey(orm['argus_services.servicegroup'], null=False))
        ))
        db.create_unique(m2m_table_name, ['service_id', 'servicegroup_id'])


    def backwards(self, orm):
        # Deleting model 'ContactGroup'
        db.delete_table('argus_services_contactgroup')

        # Deleting model 'Contact'
        db.delete_table('argus_services_contact')

        # Deleting model 'ServicePluginConfiguration'
        db.delete_table('argus_services_servicepluginconfiguration')

        # Deleting model 'HttpPluginConfig'
        db.delete_table('argus_services_httppluginconfig')

        # Deleting model 'PingPluginConfig'
        db.delete_table('argus_services_pingpluginconfig')

        # Deleting model 'PortPluginConfig'
        db.delete_table('argus_services_portpluginconfig')

        # Deleting model 'NoOpPluginConfig'
        db.delete_table('argus_services_nooppluginconfig')

        # Deleting model 'SQLQueryPluginConfig'
        db.delete_table('argus_services_sqlquerypluginconfig')

        # Deleting model 'ServiceGroup'
        db.delete_table('argus_services_servicegroup')

        # Deleting model 'Service'
        db.delete_table('argus_services_service')

        # Removing M2M table for field groups on 'Service'
        db.delete_table(db.shorten_name('argus_services_service_groups'))


    models = {
        'argus_service_configurations.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'api_can_trigger_events': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'check_interval': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_template': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'max_retries_soft': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'passive_check_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'passive_check_api_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'passive_check_ips': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'retry_interval_hard': ('django.db.models.fields.PositiveIntegerField', [], {'default': '600'}),
            'retry_interval_soft': ('django.db.models.fields.PositiveIntegerField', [], {'default': '120'})
        },
        'argus_services.contact': {
            'Meta': {'object_name': 'Contact'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['argus_services.ContactGroup']", 'blank': 'True', 'related_name': "'contacts'"}),
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
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'argus_services.nooppluginconfig': {
            'Meta': {'object_name': 'NoOpPluginConfig', '_ormbases': ['argus_services.ServicePluginConfiguration']},
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True'})
        },
        'argus_services.pingpluginconfig': {
            'Meta': {'object_name': 'PingPluginConfig', '_ormbases': ['argus_services.ServicePluginConfiguration']},
            'cmd': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'null': 'True', 'max_length': '15', 'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'argus_services.portpluginconfig': {
            'Meta': {'object_name': 'PortPluginConfig', '_ormbases': ['argus_services.ServicePluginConfiguration']},
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '80'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '10'})
        },
        'argus_services.service': {
            'Meta': {'object_name': 'Service'},
            'celery_task_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'default': "''", 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'related_name': "'services'", 'to': "orm['argus_services.ServiceGroup']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_checked': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_issued': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_ok': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_state_change': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'num_retries': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['argus_services.Service']", 'blank': 'True', 'related_name': "'children'"}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'plugin_config': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']", 'related_name': "'service'"}),
            'service_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['argus_service_configurations.ServiceConfiguration']", 'related_name': "'services'"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'state': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'state_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'argus_services.servicegroup': {
            'Meta': {'object_name': 'ServiceGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'null': 'True', 'to': "orm['argus_services.ServiceGroup']", 'blank': 'True', 'related_name': "'children'"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'argus_services.servicepluginconfiguration': {
            'Meta': {'object_name': 'ServicePluginConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['contenttypes.ContentType']", 'related_name': "'polymorphic_argus_services.servicepluginconfiguration_set'"})
        },
        'argus_services.sqlquerypluginconfig': {
            'Meta': {'object_name': 'SQLQueryPluginConfig', '_ormbases': ['argus_services.ServicePluginConfiguration']},
            'database': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'database_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'port': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3306'}),
            'query': ('django.db.models.fields.TextField', [], {}),
            'query_eval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query_replace_time': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'query_replace_timedelta': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'servicepluginconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['argus_services.ServicePluginConfiguration']", 'primary_key': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'validation': ('django.db.models.fields.TextField', [], {}),
            'validation_mode': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'blank': 'True', 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'blank': 'True', 'symmetrical': 'False'}),
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