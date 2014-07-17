# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Service.active'
        db.add_column('arguswatch_service', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Service.created_at'
        db.add_column('arguswatch_service', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, default=datetime.datetime(2014, 7, 17, 0, 0), auto_now_add=True),
                      keep_default=False)

        # Adding field 'Service.updated_at'
        db.add_column('arguswatch_service', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True, default=datetime.datetime(2014, 7, 17, 0, 0)),
                      keep_default=False)

        # Adding field 'Service.created_by'
        db.add_column('arguswatch_service', 'created_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Service.active'
        db.delete_column('arguswatch_service', 'active')

        # Deleting field 'Service.created_at'
        db.delete_column('arguswatch_service', 'created_at')

        # Deleting field 'Service.updated_at'
        db.delete_column('arguswatch_service', 'updated_at')

        # Deleting field 'Service.created_by'
        db.delete_column('arguswatch_service', 'created_by_id')


    models = {
        'arguswatch.httppluginconfig': {
            'Meta': {'object_name': 'HttpPluginConfig', '_ormbases': ['arguswatch.ServiceConfiguration']},
            'response_code': ('django.db.models.fields.IntegerField', [], {'default': '200'}),
            'response_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'serviceconfiguration_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['arguswatch.ServiceConfiguration']", 'unique': 'True', 'primary_key': 'True'}),
            'timeout': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500'})
        },
        'arguswatch.service': {
            'Meta': {'object_name': 'Service'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['arguswatch.ServiceConfiguration']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['arguswatch.Service']", 'blank': 'True', 'null': 'True'}),
            'plugin': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'arguswatch.serviceconfiguration': {
            'Meta': {'object_name': 'ServiceConfiguration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'related_name': "'polymorphic_arguswatch.serviceconfiguration_set'", 'null': 'True'})
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
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'", 'blank': 'True'}),
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

    complete_apps = ['arguswatch']