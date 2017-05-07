# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MawbDetail.spCommentOfHclBy'
        db.alter_column('process_it_mawbdetail', 'spCommentOfHclBy', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.recoveryNum'
        db.alter_column('process_it_mawbdetail', 'recoveryNum', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.spCommentOfCevaBy'
        db.alter_column('process_it_mawbdetail', 'spCommentOfCevaBy', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.ataDate'
        db.alter_column('process_it_mawbdetail', 'ataDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True))

        # Changing field 'MawbDetail.mawbNum'
        db.alter_column('process_it_mawbdetail', 'mawbNum', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.oneFStatus'
        db.alter_column('process_it_mawbdetail', 'oneFStatus', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.ppCommentsBy'
        db.alter_column('process_it_mawbdetail', 'ppCommentsBy', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.remarksInClass'
        db.alter_column('process_it_mawbdetail', 'remarksInClass', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.pmcOrLoose'
        db.alter_column('process_it_mawbdetail', 'pmcOrLoose', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.oneFStatusComment'
        db.alter_column('process_it_mawbdetail', 'oneFStatusComment', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.shipmentStatus'
        db.alter_column('process_it_mawbdetail', 'shipmentStatus', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.station'
        db.alter_column('process_it_mawbdetail', 'station', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.preAlertReceivedDate'
        db.alter_column('process_it_mawbdetail', 'preAlertReceivedDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True))

        # Changing field 'MawbDetail.recoveryOrBO'
        db.alter_column('process_it_mawbdetail', 'recoveryOrBO', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.etdTime'
        db.alter_column('process_it_mawbdetail', 'etdTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, null=True))

        # Changing field 'MawbDetail.spProStatus'
        db.alter_column('process_it_mawbdetail', 'spProStatus', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.etaDate'
        db.alter_column('process_it_mawbdetail', 'etaDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True))

        # Changing field 'MawbDetail.cobDate'
        db.alter_column('process_it_mawbdetail', 'cobDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True))

        # Changing field 'MawbDetail.etdDate'
        db.alter_column('process_it_mawbdetail', 'etdDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, null=True))

        # Changing field 'MawbDetail.spCommentOfHclAt'
        db.alter_column('process_it_mawbdetail', 'spCommentOfHclAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MawbDetail.spCommentOfCevaAt'
        db.alter_column('process_it_mawbdetail', 'spCommentOfCevaAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MawbDetail.lastUpdatedByUser'
        db.alter_column('process_it_mawbdetail', 'lastUpdatedByUser', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.customer'
        db.alter_column('process_it_mawbdetail', 'customer', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.ppCommentsAt'
        db.alter_column('process_it_mawbdetail', 'ppCommentsAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True))

        # Changing field 'MawbDetail.etaTime'
        db.alter_column('process_it_mawbdetail', 'etaTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, null=True))

        # Changing field 'MawbDetail.spCommentOfHcl'
        db.alter_column('process_it_mawbdetail', 'spCommentOfHcl', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.ataTime'
        db.alter_column('process_it_mawbdetail', 'ataTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, null=True))

        # Changing field 'MawbDetail.ppComments'
        db.alter_column('process_it_mawbdetail', 'ppComments', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'MawbDetail.spCommentOfCeva'
        db.alter_column('process_it_mawbdetail', 'spCommentOfCeva', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    def backwards(self, orm):

        # Changing field 'MawbDetail.spCommentOfHclBy'
        db.alter_column('process_it_mawbdetail', 'spCommentOfHclBy', self.gf('django.db.models.fields.CharField')(default='Null', max_length=200))

        # Changing field 'MawbDetail.recoveryNum'
        db.alter_column('process_it_mawbdetail', 'recoveryNum', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.spCommentOfCevaBy'
        db.alter_column('process_it_mawbdetail', 'spCommentOfCevaBy', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.ataDate'
        db.alter_column('process_it_mawbdetail', 'ataDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=None))

        # Changing field 'MawbDetail.mawbNum'
        db.alter_column('process_it_mawbdetail', 'mawbNum', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.oneFStatus'
        db.alter_column('process_it_mawbdetail', 'oneFStatus', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.ppCommentsBy'
        db.alter_column('process_it_mawbdetail', 'ppCommentsBy', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.remarksInClass'
        db.alter_column('process_it_mawbdetail', 'remarksInClass', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.pmcOrLoose'
        db.alter_column('process_it_mawbdetail', 'pmcOrLoose', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.oneFStatusComment'
        db.alter_column('process_it_mawbdetail', 'oneFStatusComment', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.shipmentStatus'
        db.alter_column('process_it_mawbdetail', 'shipmentStatus', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.station'
        db.alter_column('process_it_mawbdetail', 'station', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.preAlertReceivedDate'
        db.alter_column('process_it_mawbdetail', 'preAlertReceivedDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=None))

        # Changing field 'MawbDetail.recoveryOrBO'
        db.alter_column('process_it_mawbdetail', 'recoveryOrBO', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.etdTime'
        db.alter_column('process_it_mawbdetail', 'etdTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, default=None))

        # Changing field 'MawbDetail.spProStatus'
        db.alter_column('process_it_mawbdetail', 'spProStatus', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.etaDate'
        db.alter_column('process_it_mawbdetail', 'etaDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=None))

        # Changing field 'MawbDetail.cobDate'
        db.alter_column('process_it_mawbdetail', 'cobDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=None))

        # Changing field 'MawbDetail.etdDate'
        db.alter_column('process_it_mawbdetail', 'etdDate', self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=None))

        # Changing field 'MawbDetail.spCommentOfHclAt'
        db.alter_column('process_it_mawbdetail', 'spCommentOfHclAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=None))

        # Changing field 'MawbDetail.spCommentOfCevaAt'
        db.alter_column('process_it_mawbdetail', 'spCommentOfCevaAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=None))

        # Changing field 'MawbDetail.lastUpdatedByUser'
        db.alter_column('process_it_mawbdetail', 'lastUpdatedByUser', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.customer'
        db.alter_column('process_it_mawbdetail', 'customer', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.ppCommentsAt'
        db.alter_column('process_it_mawbdetail', 'ppCommentsAt', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=None))

        # Changing field 'MawbDetail.etaTime'
        db.alter_column('process_it_mawbdetail', 'etaTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, default=None))

        # Changing field 'MawbDetail.spCommentOfHcl'
        db.alter_column('process_it_mawbdetail', 'spCommentOfHcl', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.ataTime'
        db.alter_column('process_it_mawbdetail', 'ataTime', self.gf('django.db.models.fields.TimeField')(auto_now_add=True, default=None))

        # Changing field 'MawbDetail.ppComments'
        db.alter_column('process_it_mawbdetail', 'ppComments', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'MawbDetail.spCommentOfCeva'
        db.alter_column('process_it_mawbdetail', 'spCommentOfCeva', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

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
            'ataDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'ataTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'chgWeight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            'cobDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'consoleNumber': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0'}),
            'customer': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'etaDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'etaTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'etdDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'etdTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'flightCode': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '0'}),
            'flightNum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastUpdatedByUser': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'mawbNum': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'oneFStatus': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'oneFStatusComment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'pendingHblNum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '0'}),
            'pmcOrLoose': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'ppComments': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'ppCommentsAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'ppCommentsBy': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'preAlertReceivedDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'recoveryNum': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'recoveryOrBO': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'remarksInClass': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'shipmentStatus': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'slac': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            'spCommentOfCeva': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'spCommentOfCevaAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'spCommentOfCevaBy': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'spCommentOfHcl': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'spCommentOfHclAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'spCommentOfHclBy': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'spProStatus': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'station': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
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