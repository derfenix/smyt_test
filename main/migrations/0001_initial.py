# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'users'
        db.create_table(u'main_users', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('paycheck', self.gf('django.db.models.fields.IntegerField')()),
            ('date_joined', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'main', ['users'])

        # Adding model 'rooms'
        db.create_table(u'main_rooms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('spots', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'main', ['rooms'])


    def backwards(self, orm):
        # Deleting model 'users'
        db.delete_table(u'main_users')

        # Deleting model 'rooms'
        db.delete_table(u'main_rooms')


    models = {
        u'main.rooms': {
            'Meta': {'object_name': 'rooms'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {})
        },
        u'main.users': {
            'Meta': {'object_name': 'users'},
            'date_joined': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['main']