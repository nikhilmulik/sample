# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MawbDetail.totalHblNum'
        db.alter_column('process_it_mawbdetail', 'totalHblNum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=0))

        # Changing field 'MawbDetail.ataDate'
        db.alter_column('process_it_mawbdetail', 'ataDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

        # Changing field 'MawbDetail.slac'
        db.alter_column('process_it_mawbdetail', 'slac', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=0))

        # Changing field 'MawbDetail.etdTime'
        db.alter_column('process_it_mawbdetail', 'etdTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True))

        # Changing field 'MawbDetail.etaDate'
        db.alter_column('process_it_mawbdetail', 'etaDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

        # Changing field 'MawbDetail.consoleNumber'
        db.alter_column('process_it_mawbdetail', 'consoleNumber', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=0))

        # Changing field 'MawbDetail.pendingHblNum'
        db.alter_column('process_it_mawbdetail', 'pendingHblNum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=0))

        # Changing field 'MawbDetail.cobDate'
        db.alter_column('process_it_mawbdetail', 'cobDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

        # Changing field 'MawbDetail.etdDate'
        db.alter_column('process_it_mawbdetail', 'etdDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

        # Changing field 'MawbDetail.flightCode'
        db.alter_column('process_it_mawbdetail', 'flightCode', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=2, decimal_places=0))

        # Changing field 'MawbDetail.chgWeight'
        db.alter_column('process_it_mawbdetail', 'chgWeight', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=0))

        # Changing field 'MawbDetail.flightNum'
        db.alter_column('process_it_mawbdetail', 'flightNum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=0))

        # Changing field 'MawbDetail.etaTime'
        db.alter_column('process_it_mawbdetail', 'etaTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True))

        # Changing field 'MawbDetail.ataTime'
        db.alter_column('process_it_mawbdetail', 'ataTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'MawbDetail.totalHblNum'
        db.alter_column('process_it_mawbdetail', 'totalHblNum', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=2, decimal_places=0))

        # Changing field 'MawbDetail.ataDate'
        db.alter_column('process_it_mawbdetail', 'ataDate', self.gf('django.db.models.fields.DateField')())

        # Changing field 'MawbDetail.slac'
        db.alter_column('process_it_mawbdetail', 'slac', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=5, decimal_places=0))

        # Changing field 'MawbDetail.etdTime'
        db.alter_column('process_it_mawbdetail', 'etdTime', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'MawbDetail.etaDate'
        db.alter_column('process_it_mawbdetail', 'etaDate', self.gf('django.db.models.fields.DateField')())

        # Changing field 'MawbDetail.consoleNumber'
        db.alter_column('process_it_mawbdetail', 'consoleNumber', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=6, decimal_places=0))

        # Changing field 'MawbDetail.pendingHblNum'
        db.alter_column('process_it_mawbdetail', 'pendingHblNum', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=2, decimal_places=0))

        # Changing field 'MawbDetail.cobDate'
        db.alter_column('process_it_mawbdetail', 'cobDate', self.gf('django.db.models.fields.DateField')())

        # Changing field 'MawbDetail.etdDate'
        db.alter_column('process_it_mawbdetail', 'etdDate', self.gf('django.db.models.fields.DateField')())

        # Changing field 'MawbDetail.flightCode'
        db.alter_column('process_it_mawbdetail', 'flightCode', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=2, decimal_places=0))

        # Changing field 'MawbDetail.chgWeight'
        db.alter_column('process_it_mawbdetail', 'chgWeight', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=5, decimal_places=0))

        # Changing field 'MawbDetail.flightNum'
        db.alter_column('process_it_mawbdetail', 'flightNum', self.gf('django.db.models.fields.DecimalField')(default=None, max_digits=4, decimal_places=0))

        # Changing field 'MawbDetail.etaTime'
        db.alter_column('process_it_mawbdetail', 'etaTime', self.gf('django.db.models.fields.TimeField')())

        # Changing field 'MawbDetail.ataTime'
        db.alter_column('process_it_mawbdetail', 'ataTime', self.gf('django.db.models.fields.TimeField')())

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
            'ataDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ataTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'chgWeight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            'cobDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'consoleNumber': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0'}),
            'customer': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'etaDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'etaTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'etdDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'etdTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'flightCode': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '0'}),
            'flightNum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdatedByUser': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mawbNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'oneFStatus': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'oneFStatusComment': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pendingHblNum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '0'}),
            'pmcOrLoose': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ppComments': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ppCommentsAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ppCommentsBy': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'preAlertReceivedDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'recoveryNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'recoveryOrBO': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'remarksInClass': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'shipmentStatus': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slac': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            'spCommentOfCeva': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spCommentOfCevaAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'spCommentOfCevaBy': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spCommentOfHcl': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spCommentOfHclAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'spCommentOfHclBy': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'spProStatus': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'station': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'totalHblNum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '0'})
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