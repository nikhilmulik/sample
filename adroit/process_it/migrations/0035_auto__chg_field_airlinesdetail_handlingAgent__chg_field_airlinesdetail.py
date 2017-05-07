# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AirLinesDetail.handlingAgent'
        db.alter_column('process_it_airlinesdetail', 'handlingAgent', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.businessHrs'
        db.alter_column('process_it_airlinesdetail', 'businessHrs', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.otherNum'
        db.alter_column('process_it_airlinesdetail', 'otherNum', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.freeDays'
        db.alter_column('process_it_airlinesdetail', 'freeDays', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.phoneNum'
        db.alter_column('process_it_airlinesdetail', 'phoneNum', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.stnName'
        db.alter_column('process_it_airlinesdetail', 'stnName', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.airlineName'
        db.alter_column('process_it_airlinesdetail', 'airlineName', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.prefixNum'
        db.alter_column('process_it_airlinesdetail', 'prefixNum', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.extNum'
        db.alter_column('process_it_airlinesdetail', 'extNum', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.prefix'
        db.alter_column('process_it_airlinesdetail', 'prefix', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.iscChgsPyblTo'
        db.alter_column('process_it_airlinesdetail', 'iscChgsPyblTo', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.storagePyblTo'
        db.alter_column('process_it_airlinesdetail', 'storagePyblTo', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.firms'
        db.alter_column('process_it_airlinesdetail', 'firms', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.chgsPyblTo'
        db.alter_column('process_it_airlinesdetail', 'chgsPyblTo', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

        # Changing field 'AirLinesDetail.faxNum'
        db.alter_column('process_it_airlinesdetail', 'faxNum', self.gf('django.db.models.fields.CharField')(default=None, max_length=200))

    def backwards(self, orm):

        # Changing field 'AirLinesDetail.handlingAgent'
        db.alter_column('process_it_airlinesdetail', 'handlingAgent', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.businessHrs'
        db.alter_column('process_it_airlinesdetail', 'businessHrs', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.otherNum'
        db.alter_column('process_it_airlinesdetail', 'otherNum', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.freeDays'
        db.alter_column('process_it_airlinesdetail', 'freeDays', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.phoneNum'
        db.alter_column('process_it_airlinesdetail', 'phoneNum', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.stnName'
        db.alter_column('process_it_airlinesdetail', 'stnName', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.airlineName'
        db.alter_column('process_it_airlinesdetail', 'airlineName', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.prefixNum'
        db.alter_column('process_it_airlinesdetail', 'prefixNum', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.extNum'
        db.alter_column('process_it_airlinesdetail', 'extNum', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.prefix'
        db.alter_column('process_it_airlinesdetail', 'prefix', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.iscChgsPyblTo'
        db.alter_column('process_it_airlinesdetail', 'iscChgsPyblTo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.storagePyblTo'
        db.alter_column('process_it_airlinesdetail', 'storagePyblTo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.firms'
        db.alter_column('process_it_airlinesdetail', 'firms', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.chgsPyblTo'
        db.alter_column('process_it_airlinesdetail', 'chgsPyblTo', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'AirLinesDetail.faxNum'
        db.alter_column('process_it_airlinesdetail', 'faxNum', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    models = {
        'process_it.airlinesdetail': {
            'Meta': {'object_name': 'AirLinesDetail'},
            'airlineName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'businessHrs': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'chgsPyblTo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'extNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'faxNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'firms': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'freeDays': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'handlingAgent': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iscChgsPyblTo': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'otherNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phoneNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'prefixNum': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'stnName': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'storagePyblTo': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
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
            'aiDesc': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'ataDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'ataTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'chgWeight': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '0'}),
            'cobDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'consoleNumber': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '0'}),
            'createAIDesc': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'createAIStatus': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'customer': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'deletedFlag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'etaDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'etaTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'etdDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'etdTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'flightCode': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'flightNum': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'getConsoleDesc': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'getConsoleStatus': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'itInfo': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'lastUpdatedByUser': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'lastUpdatedDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'lastUpdatedTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'mawbNum': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'oneFStatus': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'oneFStatusComment': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'paLocked': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'paLockedByUser': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'pamFlag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'papFlag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'pendingHblNum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '0'}),
            'pmcOrLoose': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'ppComments': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'ppCommentsAt': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'ppCommentsBy': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'preAlertReceivedDate': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'preAlertReceivedTime': ('django.db.models.fields.TimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
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
            'speakWith': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'station': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'totalHblNum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '2', 'decimal_places': '0'}),
            'trackSource': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'updateRemarkStatus': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'updateRemarksDesc': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'updateTodayFlag': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'})
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