# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MawbDetail'
        db.create_table('process_it_mawbdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('preAlertReceivedDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('lastUpdatedByUser', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mawbNum', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('station', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('consoleNumber', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=0)),
            ('customer', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('etdDate', self.gf('django.db.models.fields.DateField')()),
            ('etdTime', self.gf('django.db.models.fields.TimeField')()),
            ('etaDate', self.gf('django.db.models.fields.DateField')()),
            ('etaTime', self.gf('django.db.models.fields.TimeField')()),
            ('ataDate', self.gf('django.db.models.fields.DateField')()),
            ('ataTime', self.gf('django.db.models.fields.TimeField')()),
            ('flightCode', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=0)),
            ('flightNum', self.gf('django.db.models.fields.DecimalField')(max_digits=4, decimal_places=0)),
            ('slac', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=0)),
            ('chgWeight', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=0)),
            ('pmcOrLoose', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('remarksInClass', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('shipmentStatus', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('cobDate', self.gf('django.db.models.fields.DateField')()),
            ('recoveryNum', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('oneFStatus', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('oneFStatusComment', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ppComments', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ppCommentsBy', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ppCommentsAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('totalHblNum', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=0)),
            ('pendingHblNum', self.gf('django.db.models.fields.DecimalField')(max_digits=2, decimal_places=0)),
            ('spProStatus', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('spCommentOfHcl', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('spCommentOfHclBy', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('spCommentOfHclAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('spCommentOfCeva', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('spCommentOfCevaBy', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('spCommentOfCevaAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('recoveryOrBO', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('process_it', ['MawbDetail'])

        # Adding model 'HawbDetail'
        db.create_table('process_it_hawbdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mawbNum', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('hawbNum', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('consignee', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wpStatus', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wpComments', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wpCommentsBy', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('wpCommentsAt', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('process_it', ['HawbDetail'])

        # Adding model 'UserCountDetail'
        db.create_table('process_it_usercountdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userName', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('totalCounts', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('avgTime', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
        ))
        db.send_create_signal('process_it', ['UserCountDetail'])


    def backwards(self, orm):
        # Deleting model 'MawbDetail'
        db.delete_table('process_it_mawbdetail')

        # Deleting model 'HawbDetail'
        db.delete_table('process_it_hawbdetail')

        # Deleting model 'UserCountDetail'
        db.delete_table('process_it_usercountdetail')


    models = {
        'process_it.hawbdetail': {
            'Meta': {'object_name': 'HawbDetail'},
            'consignee': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'hawbNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mawbNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wpComments': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wpCommentsAt': ('django.db.models.fields.DateTimeField', [], {}),
            'wpCommentsBy': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'wpStatus': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'process_it.mawbdetail': {
            'Meta': {'object_name': 'MawbDetail'},
            'ataDate': ('django.db.models.fields.DateField', [], {}),
            'ataTime': ('django.db.models.fields.TimeField', [], {}),
            'chgWeight': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '0'}),
            'cobDate': ('django.db.models.fields.DateField', [], {}),
            'consoleNumber': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '0'}),
            'customer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'etaDate': ('django.db.models.fields.DateField', [], {}),
            'etaTime': ('django.db.models.fields.TimeField', [], {}),
            'etdDate': ('django.db.models.fields.DateField', [], {}),
            'etdTime': ('django.db.models.fields.TimeField', [], {}),
            'flightCode': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '0'}),
            'flightNum': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdatedByUser': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mawbNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'oneFStatus': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'oneFStatusComment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pendingHblNum': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '0'}),
            'pmcOrLoose': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ppComments': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ppCommentsAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ppCommentsBy': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'preAlertReceivedDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'recoveryNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'recoveryOrBO': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'remarksInClass': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'shipmentStatus': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slac': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '0'}),
            'spCommentOfCeva': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spCommentOfCevaAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'spCommentOfCevaBy': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spCommentOfHcl': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spCommentOfHclAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'spCommentOfHclBy': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spProStatus': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'station': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'totalHblNum': ('django.db.models.fields.DecimalField', [], {'max_digits': '2', 'decimal_places': '0'})
        },
        'process_it.usercountdetail': {
            'Meta': {'object_name': 'UserCountDetail'},
            'avgTime': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'totalCounts': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'userName': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['process_it']