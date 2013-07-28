# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Carrier'
        db.create_table(u'pester_carrier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('gateway', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'pester', ['Carrier'])

        # Adding model 'User'
        db.create_table(u'pester_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('join_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('carrier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pester.Carrier'])),
        ))
        db.send_create_signal(u'pester', ['User'])

        # Adding model 'Recipient'
        db.create_table(u'pester_recipient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('carrier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pester.Carrier'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pester.User'])),
        ))
        db.send_create_signal(u'pester', ['Recipient'])

        # Adding model 'Pattern'
        db.create_table(u'pester_pattern', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'pester', ['Pattern'])

        # Adding model 'Pestering'
        db.create_table(u'pester_pestering', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pester.User'])),
            ('recipient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pester.Recipient'])),
            ('search_term', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pester.Pattern'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('notify_user_method', self.gf('django.db.models.fields.CharField')(default='E', max_length=1)),
            ('notify_recipient_method', self.gf('django.db.models.fields.CharField')(default='E', max_length=1)),
        ))
        db.send_create_signal(u'pester', ['Pestering'])

        # Adding model 'Image'
        db.create_table(u'pester_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('search_term', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'pester', ['Image'])

        # Adding model 'SentPestering'
        db.create_table(u'pester_sentpestering', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pestering', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pester.Pestering'])),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pester.Image'])),
            ('send_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('success', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'pester', ['SentPestering'])


    def backwards(self, orm):
        # Deleting model 'Carrier'
        db.delete_table(u'pester_carrier')

        # Deleting model 'User'
        db.delete_table(u'pester_user')

        # Deleting model 'Recipient'
        db.delete_table(u'pester_recipient')

        # Deleting model 'Pattern'
        db.delete_table(u'pester_pattern')

        # Deleting model 'Pestering'
        db.delete_table(u'pester_pestering')

        # Deleting model 'Image'
        db.delete_table(u'pester_image')

        # Deleting model 'SentPestering'
        db.delete_table(u'pester_sentpestering')


    models = {
        u'pester.carrier': {
            'Meta': {'object_name': 'Carrier'},
            'gateway': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'pester.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'pester.pattern': {
            'Meta': {'object_name': 'Pattern'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'pester.pestering': {
            'Meta': {'object_name': 'Pestering'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify_recipient_method': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'notify_user_method': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pester.Pattern']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pester.Recipient']"}),
            'search_term': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pester.User']"})
        },
        u'pester.recipient': {
            'Meta': {'object_name': 'Recipient'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pester.Carrier']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pester.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        u'pester.sentpestering': {
            'Meta': {'object_name': 'SentPestering'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pester.Image']"}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pestering': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pester.Pestering']"}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {}),
            'success': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pester.user': {
            'Meta': {'object_name': 'User'},
            'carrier': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pester.Carrier']"}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['pester']