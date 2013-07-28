# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Pattern.name'
        db.alter_column(u'pester_pattern', 'name', self.gf('django.db.models.fields.CharField')(max_length=32))

    def backwards(self, orm):

        # Changing field 'Pattern.name'
        db.alter_column(u'pester_pattern', 'name', self.gf('django.db.models.fields.CharField')(max_length=16))

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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
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