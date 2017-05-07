
# Create your views here.

from process_it.models import MawbDetail
from django.db import connection, transaction
from django.shortcuts import render_to_response
from datetime import datetime
from django.http import HttpResponse
import pymongo
from django.utils.simplejson import dumps
import gridfs
from datetime import *; 
from dateutil.relativedelta import *

# this is commmetn
conn = pymongo.Connection("", 27017)
db = conn.process_test
bb_attachments = gridfs.GridFS(db, "bb_attachments")



'''
def userLog(logmsg):
    
#    logFile = open( "/apps/webapps/Adroit/dev/adroit/LogFiles/" + 'deleteFileRecords.log', 'a')

    logFile = open( "D:/Nikhil.Mulik/Adroit/adroit/LogFile/" + 'deleteFileRecords.log', 'a')
    logFile.write(logmsg)
    logFile.close()
'''


def insertMawb(request):
    t = {}
    if request.method == 'POST':
        if request.POST.get('mawbNum', ''):
            try:
                mawb = MawbDetail.objects.get(mawbNum=request.POST['mawbNum'])
                t['key'] = 0
            except MawbDetail.DoesNotExist:
                mawb = MawbDetail(mawbNum=request.POST['mawbNum'])
                mawb.save()
                t['key'] = 1
            return HttpResponse(dumps(t), content_type='application/json')


def chkHasMawb(request):
    t = {}
    if request.method == 'POST':
        if request.POST.get('chkmawb', ''):
            try:
                # if db.ds.find({"Mawb":request.POST['chkmawb']}).count():
                mawb = MawbDetail.objects.get(mawbNum=request.POST['chkmawb'])
                if mawb.papFlag == True:
                    t['papFlag']=True
                else:
                    t['papFlag']=False
                t['key'] = 1
                # else:
                    # #mawb = MawbDetail(mawbNum=request.POST['chkmawb'])
                    # #mawb.save()
                #    t['key'] = 0
            except MawbDetail.DoesNotExist:
                # mawb = MawbDetail(mawbNum=request.POST['chkmawb'])
                # mawb.save()
                t['key'] = 0
            db.ds.update({"_id":request.POST['id']}, {"$set":{"Mawb":request.POST['chkmawb'], "categories":[]}}, False, True)
            return HttpResponse(dumps(t), content_type='application/json')

def updateMawbEntry(request):
    mblid = request.POST['mawb_id']
    mawb = MawbDetail.objects.get(id=mblid)
    mawb.lastUpdatedByUser = request.session['username']
    mawb.lastUpdatedDate = datetime.now().strftime("%Y-%m-%d")
    mawb.lastUpdatedTime = datetime.now().strftime("%H:%M:%S")
    mawb.updateTodayFlag = True
    msg = {}
    
    lastUpdatedByUser = request.session['username']
    TODAY = date.today()
    NOW = datetime.now().strftime("%H:%M:%S")
    mawbNum = request.POST['mawbNum']
 
    
    if request.POST.get('station', ''):
        mawb.station = request.POST['station']
        station = str(request.POST['station'])
    else:
        mawb.station = None
        station = ""

    if request.POST.get('mawbNum', ''):
        mawb.mawbNum = request.POST['mawbNum']
        mawbNum = str(request.POST['mawbNum'])
    else:
        mawb.mawbNum = None
        mawbNum = ""

    if request.POST.get('consoleNumber', ''):
        mawb.consoleNumber = request.POST['consoleNumber']
        consoleNumber = str(request.POST['consoleNumber'])
    else:
        mawb.consoleNumber = None
        consoleNumber = ""

    if request.POST.get('itInfo', ''):
        mawb.itInfo = request.POST['itInfo']
        itInfo = str(request.POST['itInfo'])
    else:
        mawb.itInfo = None
        itInfo = ""

    if request.POST.get('customer', ''):
        mawb.customer = request.POST['customer']
        customer = str(request.POST['customer'])
    else:
        mawb.customer = None
        customer = ""

    if request.POST.get('etdDate', ''):
        mawb.etdDate = datetime.strptime(request.POST['etdDate'], "%m-%d-%y")
    else:
        mawb.etdDate = None

    if request.POST.get('etdTime', ''):
        mawb.etdTime = datetime.strptime(request.POST['etdTime'], "%H%M")
    else:
        mawb.etdTime = None

    if request.POST.get('etaDate', ''):
        mawb.etaDate = datetime.strptime(request.POST['etaDate'], "%m-%d-%y")
        etaDate = str(datetime.strptime(request.POST['etaDate'], "%m-%d-%y"))
    else:
        mawb.etaDate = None
        etaDate = ""

    if request.POST.get('etaTime', ''):
        mawb.etaTime = datetime.strptime(request.POST['etaTime'], "%H%M")
        etaTime = str(datetime.strptime(request.POST['etaTime'], "%H%M"))
    else:
        mawb.etaTime = None
        etaTime = ""

    if request.POST.get('ataDate', ''):
        mawb.ataDate = datetime.strptime(request.POST['ataDate'], "%m-%d-%y")
    else:
        mawb.ataDate = None

    if request.POST.get('ataTime', ''):
        mawb.ataTime = datetime.strptime(request.POST['ataTime'], "%H%M")
    else:
        mawb.ataTime = None

    if request.POST.get('flightCode', ''):
        mawb.flightCode = request.POST['flightCode']
        flightCode = str(request.POST['flightCode'])
    else:
        mawb.flightCode = None
        flightCode = ""

    if request.POST.get('flightNum', ''):
        mawb.flightNum = request.POST['flightNum']
        flightNum = str(request.POST['flightNum'])
    else:
        mawb.flightNum = None
        flightNum = ""

    if request.POST.get('slac', ''):
        mawb.slac = request.POST['slac']
        slac = str(request.POST['slac'])
    else:
        mawb.slac = None
        slac = ""

    if request.POST.get('pmcOrLoose', ''):
        mawb.pmcOrLoose = request.POST['pmcOrLoose']
        pmcOrLoose = str(request.POST['pmcOrLoose'])
    else:
        mawb.pmcOrLoose = None
        pmcOrLoose = ""

    if request.POST.get('chgWeight', ''):
        mawb.chgWeight = request.POST['chgWeight']
        chgWeight = str(request.POST['chgWeight'])
    else:
        mawb.chgWeight = None
        chgWeight = ""

    if request.POST.get('remarksInClass', ''):
        mawb.remarksInClass = request.POST['remarksInClass']
        remarksInClass = str(request.POST['remarksInClass'])
    else:
        mawb.remarksInClass = None
        remarksInClass = ""

    if request.POST.get('shipmentStatus', ''):
        mawb.shipmentStatus = request.POST['shipmentStatus']
        shipmentStatus = str(request.POST['shipmentStatus'])
        if request.POST['shipmentStatus'] == 'COB' and request.POST['chgWeight'] != '' and request.POST['slac'] != '' and request.POST['pmcOrLoose'] != '':
            msg['cob'] = 1
            mawb.pamFlag = 1
            mawb.papFlag = 0
              
            cursor = connection.cursor()          
            query =  "INSERT INTO operational_log (mawbNum,userName,date,time, operations) VALUES('" +mawbNum+ "','"+lastUpdatedByUser+"','"+str(TODAY)+"', '"+str(NOW)+"' ,'COB moved to Pre-Alert Master Sheet');"
            cursor.execute(query)  
            
        else:
            msg['cob'] = 0
    else:
        mawb.shipmentStatus = None
        shipmentStatus = ""

    if request.POST.get('recoveryNum', ''):
        mawb.recoveryNum = request.POST['recoveryNum']
    else:
        mawb.recoveryNum = None

    if request.POST.get('trackSource', ''):
        mawb.trackSource = request.POST['trackSource']
        trackSource = str(request.POST['trackSource'])
    else:
        mawb.trackSource = None
        trackSource = ""

    if request.POST.get('speakWith', ''):
        mawb.speakWith = request.POST['speakWith']
        speakWith = str(request.POST['speakWith'])
    else:
        mawb.speakWith = None
        speakWith = ""

    if request.POST.get('oneFStatus', ''):
        mawb.oneFStatus = request.POST['oneFStatus']
        oneFStatus = str(request.POST['oneFStatus'])
    else:
        mawb.oneFStatus = None
        oneFStatus = ""

    if request.POST.get('oneFStatusComment', ''):
        mawb.oneFStatusComment = request.POST['oneFStatusComment']
        oneFStatusComment = str(request.POST['oneFStatusComment'])
    else:
        mawb.oneFStatusComment = None
        oneFStatusComment = ""
    mawb.save()

    msg['name'] = request.session['username']
    msg['date'] = datetime.now().strftime("%m-%d-%y")
    msg['time'] = datetime.now().strftime("%H%M")
    # import pdb; pdb.set_trace()
    values = '{station='+station+';mawbNum='+mawbNum+';consoleNumber='+consoleNumber+';customer='+customer+';flightCode='+flightCode+';flightNum='+flightNum+';etaDate='+etaDate+';etaTime='+etaTime+';itInfo='+itInfo+';shipmentStatus='+shipmentStatus+';trackSource='+trackSource+';speakWith='+speakWith+';pmcOrLoose='+pmcOrLoose+';slac='+slac+';chgWeight='+chgWeight+';remarksInClass='+remarksInClass+';oneFStatus='+oneFStatus+';lastUpdatedByUser='+lastUpdatedByUser+';oneFStatusComment='+oneFStatusComment+'}'


    writeLog(values)
    
    return HttpResponse(dumps(msg), content_type='application/json')


def writeLog(logdata):
    # import pdb; pdb.set_trace()
    logFile = open("/apps/webapps/Adroit/live/ACTIVITY_LOG/activity_log_"+datetime.now().strftime("%d%m%y")+".log", 'a')
    logFile.write(datetime.now().strftime("%Y%m%d %H%M%S")+':: '+logdata+'\r\n')
    logFile.close()



def rebookEntry(request):
    msg = {}
    
    lastUpdatedByUser = request.session['username']
    TODAY = date.today()
    NOW = datetime.now().strftime("%H:%M:%S")
 
    if request.method == 'POST':
        if request.POST.get('reebookdMawbNum', ''):
            mblid = request.POST['reebookdMawbNum']
            

    
            try:
                mawb = MawbDetail.objects.get(mawbNum=mblid)
                if mawb.papFlag != True:
                    cursor = connection.cursor()
                    query =  "INSERT INTO operational_log (mawbNum,userName,date,time, operations) VALUES('" +mblid+ "','"+lastUpdatedByUser+"','"+str(TODAY)+"', '"+str(NOW)+"' ,'Rebooked');"
                    cursor.execute(query)
                    mawb.papFlag = 1
                    mawb.lastUpdatedByUser = request.session['username']
                    mawb.save()
                    msg['exists'] = 1
                
            except MawbDetail.DoesNotExist:
                msg['exists'] = 0
    return HttpResponse(dumps(msg), content_type='application/json')

def addMawbEntry(request):
    kwargs = {'lastUpdatedByUser':request.session['username'], }
    kwargs['papFlag'] = 1
    if request.method == 'POST':
        if request.POST.get('mawbNum', ''):
            if request.POST.get('station', ''):
                kwargs['station'] = request.POST['station']
            if request.POST.get('preAlertReceivedDate', ''):
                kwargs['preAlertReceivedDate'] = datetime.strptime(request.POST['preAlertReceivedDate'], "%m-%d-%y")
            if request.POST.get('mawbNum', ''):
                kwargs['mawbNum'] = request.POST['mawbNum']
            if request.POST.get('consoleNumber', ''):
                kwargs['consoleNumber'] = request.POST['consoleNumber']
            if request.POST.get('customer', ''):
                kwargs['customer'] = request.POST['customer']
            if request.POST.get('etaDate', ''):
                kwargs['etaDate'] = datetime.strptime(request.POST['etaDate'], "%m-%d-%y")
            if request.POST.get('etaTime', ''):
                kwargs['etaTime'] = datetime.strptime(request.POST['etaTime'], "%H%M")
            if request.POST.get('itInfo', ''):
                kwargs['itInfo'] = request.POST['itInfo']
            if request.POST.get('flightCode', ''):
                kwargs['flightCode'] = request.POST['flightCode']
            if request.POST.get('flightNum', ''):
                kwargs['flightNum'] = request.POST['flightNum']
            if request.POST.get('slac', ''):
                kwargs['slac'] = request.POST['slac']
            if request.POST.get('pmcOrLoose', ''):
                kwargs['pmcOrLoose'] = request.POST['pmcOrLoose']
            if request.POST.get('chgWeight', ''):
                kwargs['chgWeight'] = request.POST['chgWeight']
            if request.POST.get('remarksInClass', ''):
                kwargs['remarksInClass'] = request.POST['remarksInClass']
            if request.POST.get('trackSource', ''):
                kwargs['trackSource'] = request.POST['trackSource']
            if request.POST.get('speakWith', ''):
                kwargs['speakWith'] = request.POST['speakWith']
            if request.POST.get('shipmentStatus', ''):
                kwargs['shipmentStatus'] = request.POST['shipmentStatus']
            if request.POST.get('cobDate', ''):
                kwargs['cobDate'] = datetime.strptime(request.POST['cobDate'], "%m-%d-%y")
            if request.POST.get('recoveryNum', ''):
                kwargs['recoveryNum'] = request.POST['recoveryNum']
            if request.POST.get('oneFStatus', ''):
                kwargs['oneFStatus'] = request.POST['oneFStatus']
            if request.POST.get('oneFStatusComment', ''):
                kwargs['oneFStatusComment'] = request.POST['oneFStatusComment']
            ins_arr = MawbDetail(**kwargs)
            
            # print "kwargs",kwargs
            writeLog(str(kwargs))

            ins_arr.save()
    return render_to_response('process_it/mailActionResponse.html', locals())

def deleteMasters(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        mawb_string = request.POST['mawb_arr'].rstrip(",").replace(",", "','")
        lastUpdatedByUser = request.session['username']
        updateDateTime= datetime.today()
        TODAY = date.today()
        NOW = datetime.now().strftime("%H:%M:%S")
        
        query = "UPDATE process_it_mawbdetail SET papFlag=0, pamFlag=0, deletedFlag=1,lastUpdatedByUser='"+lastUpdatedByUser+"' WHERE mawbNum in ('" + mawb_string + "')"
        cursor.execute(query) 
          

        for logMawbNum in mawb_string.split("','"):
            query =  "INSERT INTO operational_log (mawbNum,userName,date,time, operations) VALUES('" +logMawbNum+ "','"+lastUpdatedByUser+"','"+str(TODAY)+"', '"+str(NOW)+"' ,'Deleted');"
            #print  '===>',query
            cursor.execute(query)  
  
        # print "====", query 
        transaction.commit_unless_managed()
        return render_to_response('process_it/mailActionResponse.html', locals())


def moveMastersToPAP(request):
    lastUpdatedByUser = request.session['username']
    TODAY = date.today()
    NOW = datetime.now().strftime("%H:%M:%S")

 
    if request.method == 'POST':
        cursor = connection.cursor()
        mawb_string = request.POST['mawb_arr'].rstrip(",").replace(",", "','")
        query = "UPDATE process_it_mawbdetail SET papFlag=1, pamFlag=0 WHERE mawbNum in ('" + mawb_string + "')"
        #print "====", query
        cursor.execute(query)
        transaction.commit_unless_managed()
        
        cursor = connection.cursor()          
        query =  "INSERT INTO operational_log (mawbNum,userName,date,time, operations) VALUES('" +mawb_string+ "','"+lastUpdatedByUser+"','"+str(TODAY)+"', '"+str(NOW)+"' ,'COB moved to Pre-Alert Processing');"
        cursor.execute(query)  
        
    
        return render_to_response('process_it/mailActionResponse.html', locals())

def completeCOBToMasters(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        mawb_string = request.POST['mawb_arr'].rstrip(",").replace(",", "','")
        query = "UPDATE process_it_mawbdetail SET papFlag=0, pamFlag=0 WHERE mawbNum in ('" + mawb_string + "')"
        # print "====", query
        cursor.execute(query)
        transaction.commit_unless_managed()
        return render_to_response('process_it/mailActionResponse.html', locals())

def mawbAction(request):
    t = {}
    if request.method == 'POST':
        actionType = request.POST['actionType']
        mawb_id = request.POST['mawb_id']
        if actionType == 'delete':
            mawb = MawbDetail.objects.get(mawbNum=mawb_id)
            mawb.delete()
            # for mblid in mawb_id:
            #    mawb = MawbDetail.objects.get(mawbNum=mblid)
            #    mawb.delete()
            return render_to_response('process_it/mailActionResponse.html', locals())
        elif actionType == 'movebacktopap':
            mawb = MawbDetail.objects.get(mawbNum=mawb_id)
            mawb.pamFlag = False
            mawb.papFlag = True
            mawb.save()
            # for mblid in mawb_id:
            #    mawb = MawbDetail.objects.get(mawbNum=mblid)
            #    mawb.pamFlag = False
            #    mawb.papFlag = True
            #    mawb.save()
            return render_to_response('process_it/mailActionResponse.html', locals())
        elif actionType == 'update':
            mblid = request.POST['mawb_id']
            mawb = MawbDetail.objects.get(mawbNum=mblid)
            mawb.lastUpdatedByUser = request.session['username']
            if request.POST.get('station', ''):
                mawb.station = request.POST['station']
            if request.POST.get('preAlertReceivedDate', ''):
                mawb.preAlertReceivedDate = datetime.strptime(request.POST['preAlertReceivedDate'], "%d-%m-%Y")
            if request.POST.get('mawbNum', ''):
                mawb.mawbNum = request.POST['mawbNum']
            if request.POST.get('consoleNumber', ''):
                mawb.consoleNumber = request.POST['consoleNumber']
            if request.POST.get('customer', ''):
                mawb.customer = request.POST['customer']
            if request.POST.get('etdDate', ''):
                mawb.etdDate = datetime.strptime(request.POST['etdDate'], "%d-%m-%Y")
            if request.POST.get('etdTime', ''):
                mawb.etdTime = datetime.strptime(request.POST['etdTime'], "%H%M")
            if request.POST.get('etaDate', ''):
                mawb.etaDate = datetime.strptime(request.POST['etaDate'], "%d-%m-%Y")
            if request.POST.get('etaTime', ''):
                mawb.etaTime = datetime.strptime(request.POST['etaTime'], "%H%M")
            if request.POST.get('ataDate', ''):
                mawb.ataDate = datetime.strptime(request.POST['ataDate'], "%d-%m-%Y")
            if request.POST.get('ataTime', ''):
                mawb.ataTime = datetime.strptime(request.POST['ataTime'], "%H%M")
            if request.POST.get('flightCode', ''):
                mawb.flightCode = request.POST['flightCode']
            if request.POST.get('flightNum', ''):
                mawb.flightNum = request.POST['flightNum']
            if request.POST.get('slac', ''):
                mawb.slac = request.POST['slac']
            if request.POST.get('pmcOrLoose', ''):
                mawb.pmcOrLoose = request.POST['pmcOrLoose']
            if request.POST.get('chgWeight', ''):
                mawb.chgWeight = request.POST['chgWeight']
            if request.POST.get('remarksInClass', ''):
                mawb.remarksInClass = request.POST['remarksInClass']
            if request.POST.get('shipmentStatus', ''):
                mawb.shipmentStatus = request.POST['shipmentStatus']
                if request.POST['shipmentStatus'] == 'COB' and request.POST['chgWeight'] != '' and request.POST['slac'] != '' and request.POST['pmcOrLoose'] != '':
                    mawb.pamFlag = True
                    mawb.papFlag = False
            if request.POST.get('cobDate', ''):
                mawb.cobDate = datetime.strptime(request.POST['cobDate'], "%d-%m-%Y")
            if request.POST.get('recoveryNum', ''):
                mawb.recoveryNum = request.POST['recoveryNum']
            if request.POST.get('oneFStatus', ''):
                mawb.oneFStatus = request.POST['oneFStatus']
            if request.POST.get('oneFStatusComment', ''):
                mawb.oneFStatusComment = request.POST['oneFStatusComment']
            mawb.save()
            return render_to_response('process_it/mailActionResponse.html', locals())
        else:
            actionType = 0
            return render_to_response('process_it/mailActionResponse.html', locals())
