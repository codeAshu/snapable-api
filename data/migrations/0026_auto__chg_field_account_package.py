# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Account.package'
        db.alter_column('data_account', 'package_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.Package'], null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Account.package'
        raise RuntimeError("Cannot reverse this migration. 'Account.package' and its values cannot be restored.")

    models = {
        'data.account': {
            'Meta': {'object_name': 'Account'},
            'addons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.Addon']", 'through': "orm['data.AccountAddon']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['data.Package']", 'null': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.User']", 'through': "orm['data.AccountUser']", 'symmetrical': 'False'}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'})
        },
        'data.accountaddon': {
            'Meta': {'object_name': 'AccountAddon'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Account']"}),
            'addon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Addon']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'data.accountuser': {
            'Meta': {'object_name': 'AccountUser'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Account']"}),
            'admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.User']"})
        },
        'data.addon': {
            'Meta': {'object_name': 'Addon'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'data.address': {
            'Meta': {'object_name': 'Address'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'}),
            'lng': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '6'})
        },
        'data.album': {
            'Meta': {'object_name': 'Album'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['data.Photo']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Type']"})
        },
        'data.albumphoto': {
            'Meta': {'object_name': 'AlbumPhoto'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Album']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Photo']"})
        },
        'data.event': {
            'Meta': {'object_name': 'Event'},
            'access_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Account']"}),
            'addons': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['data.Addon']", 'through': "orm['data.EventAddon']", 'symmetrical': 'False'}),
            'cover': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'pin': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tz_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'data.eventaddon': {
            'Meta': {'object_name': 'EventAddon'},
            'addon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Addon']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'data.guest': {
            'Meta': {'object_name': 'Guest'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Type']"})
        },
        'data.order': {
            'Meta': {'object_name': 'Order'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Account']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('jsonfield.fields.JSONField', [], {}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_gateway_invoice_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'print_gateway_invoice_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'shipping': ('jsonfield.fields.JSONField', [], {'null': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'total_price': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.User']", 'null': 'True'})
        },
        'data.package': {
            'Meta': {'object_name': 'Package'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '5', 'null': 'True'}),
            'interval_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'items': ('jsonfield.fields.JSONField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'trial_period_days': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'data.passwordnonce': {
            'Meta': {'object_name': 'PasswordNonce'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonce': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.User']"}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'data.photo': {
            'Meta': {'object_name': 'Photo'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Event']"}),
            'guest': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['data.Guest']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrics': ('django.db.models.fields.TextField', [], {}),
            'streamable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.Type']"})
        },
        'data.type': {
            'Meta': {'object_name': 'Type'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'data.user': {
            'Meta': {'object_name': 'User'},
            'billing_zip': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_access': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'payment_gateway_user_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'terms': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['data']