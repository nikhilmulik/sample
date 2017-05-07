# Create your views here.
from django.template import RequestContext
from process_it.models import MawbDetail
from django.shortcuts import render_to_response
from datetime import datetime,timedelta
from django.http import HttpResponse
from django.utils.simplejson import dumps
import pymongo
import gridfs
from django.db import connection
from datetime import *; 
from dateutil.relativedelta import *


# this is commmetn
conn = pymongo.Connection("",27017)
#conn = pymongo.Connection("localhost",27017)
db = conn.process_test
bb_attachments = gridfs.GridFS(db,"bb_attachments")

def getDashboardCounts(request):
    msg = {}
    querystring = {}
    if request.method == 'POST':
        if request.POST.get('fromDateFilter',''):
            fromDate = datetime.strptime(request.POST['fromDateFilter'],"%m-%d-%Y")
            fromDateStr = datetime.strptime(request.POST['fromDateFilter'],"%m-%d-%Y").strftime("%Y%m%d") + '000000' 
        if request.POST.get('toDateFilter',''):
            toDate = datetime.strptime(request.POST['toDateFilter'],"%m-%d-%Y")
            toDateStr = datetime.strptime(request.POST['toDateFilter'],"%m-%d-%Y").strftime("%Y%m%d") + '000000' 
        querystring['date'] = {'$gte':fromDateStr,'$lte':toDateStr}
        querystring['categories'] = 'green'
        msg['mail_lax_count'] = db.ds.find(querystring).count()

        querystring['categories'] = 'blue'
        msg['mail_sfo_count'] = db.ds.find(querystring).count()

        querystring['categories'] = 'black'
        msg['mail_oos_count'] = db.ds.find(querystring).count()

        querystring['categories'] = []
        msg['mail_uniden_count'] = db.ds.find(querystring).count()

        msg['lax_cob'] = MawbDetail.objects.filter(preAlertReceivedDate__gte=fromDate,preAlertReceivedDate__lte=toDate,station='LAX',shipmentStatus='COB').count()
        msg['lax_bo'] = MawbDetail.objects.filter(preAlertReceivedDate__gte=fromDate,preAlertReceivedDate__lte=toDate,station='LAX',shipmentStatus='BO').count()
        msg['sfo_cob'] = MawbDetail.objects.filter(preAlertReceivedDate__gte=fromDate,preAlertReceivedDate__lte=toDate,station='SFO',shipmentStatus='COB').count()
        msg['sfo_bo'] = MawbDetail.objects.filter(preAlertReceivedDate__gte=fromDate,preAlertReceivedDate__lte=toDate,station='SFO',shipmentStatus='BO').count()
         
        msg['dfw_cob'] = MawbDetail.objects.filter(preAlertReceivedDate__gte=fromDate,preAlertReceivedDate__lte=toDate,station='DFW',shipmentStatus='COB').count()
        msg['dfw_bo'] = MawbDetail.objects.filter(preAlertReceivedDate__gte=fromDate,preAlertReceivedDate__lte=toDate,station='DFW',shipmentStatus='BO').count()
        msg['iah_cob'] = MawbDetail.objects.filter(preAlertReceivedDate__gte=fromDate,preAlertReceivedDate__lte=toDate,station='IAH',shipmentStatus='COB').count()
        msg['iah_bo'] = MawbDetail.objects.filter(preAlertReceivedDate__gte=fromDate,preAlertReceivedDate__lte=toDate,station='IAH',shipmentStatus='BO').count()
        


    return HttpResponse(dumps(msg),content_type='application/json')

def getMailList(request):
    if 'username' not in request.session:
        csrfContext = RequestContext(request)
        return render_to_response('process_it/loginPage.html', csrfContext)
    if request.method == 'POST':
        dic_sub = {}
        dic_mbl = {}
        dic_hbl = {}
        dic_body = {}
        dic_html = {}
        querystring = {}
        recoverytime = 'all'
        if request.POST.get('globalSearch',''):
            dic_sub['subject'] = {'$regex':request.POST['globalSearch']}
            dic_mbl['Mawb'] = {'$regex':request.POST['globalSearch']}
            dic_hbl['Hawb_details.Hawb'] = {'$regex':request.POST['globalSearch']}
            dic_body['body_text'] = {'$regex':request.POST['globalSearch']}
            dic_html['html_text'] = {'$regex':request.POST['globalSearch']}
            querystring['$or'] = [dic_sub, dic_mbl, dic_hbl, dic_body, dic_html]
            readquerystring = {}
            readquerystring.update(querystring)
            readquerystring['read'] = 1 
            initialData = {'uid':request.session['uid'],'blue_counts': 0, 'green_counts': 0, 'querystring': request.POST, 'mail_entries': db.ds.find(querystring,{"html_text":0,"body_text":0}).sort("date",-1).limit(500) , 'counts': db.ds.find(querystring).count(), 'readcounts': 0,'username': request.session['username'],'access_rights':request.session['accessrights'], 'readcounts': db.ds.find(readquerystring).count(),'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']} #
            csrfContext = RequestContext(request, initialData)
            return render_to_response('process_it/mailDetails.html', csrfContext)
        if request.POST.get('mailbox',''):
            querystring['mailbox'] = request.POST['mailbox']
        if request.POST.get('category',''):
            if request.POST['category'] == 'all':
                pass
            elif request.POST['category'] == 'empty':
                querystring['categories'] = []
            else:
                querystring['categories'] = request.POST['category']
        if request.POST.get('from',''):
            querystring['from'] = {'$regex':request.POST['from']}
        if request.POST.get('subject',''):
            querystring['subject'] = {'$regex':request.POST['subject']}
        if request.POST.get('to',''):
            querystring['to'] = {'$regex':request.POST['to']}
        if request.POST.get('mawb',''):
            querystring['Mawb'] = {'$regex':request.POST['mawb']}
        if request.POST.get('hawb',''):
            querystring['Hawb_details.Hawb'] = {'$regex':request.POST['hawb']}
        if 'attach' in request.POST:
            querystring['attachments_list'] = {'$ne':[]}
        if request.POST.get('recoverytime',''):
            recoverytime = request.POST['recoverytime']
        if request.POST.get('date',''):
            querydate = datetime.strptime(request.POST['date'],"%m-%d-%Y").strftime("%Y%m%d")
            if request.POST.get('recoverytime',''):
                if recoverytime == 'first':
                    querydateStart = querydate + "010000"
                    querydateEnd = querydate + "143000"
                elif recoverytime == 'second':
                    querydateStart = querydate + "143000"
                    querydateEnd = querydate + "203000"
                elif recoverytime == 'third':
                    querydateStart = querydate + "203000"
                    querydatePlus1 = datetime.strptime(request.POST['date'],"%m-%d-%Y") + timedelta(hours=24)
                    querydateEnd = querydatePlus1.strftime("%Y%m%d") + "010000"
                elif recoverytime == 'all':
                    querydateStart = querydate + "010000"
                    querydatePlus1 = datetime.strptime(request.POST['date'],"%m-%d-%Y") + timedelta(hours=24)
                    querydateEnd = querydatePlus1.strftime("%Y%m%d") + "010000"
                else:
                    querydate = datetime.now().strftime("%Y%m%d")
                    querydateStart = querydate + "010000"
                    querydatePlus1 = datetime.now() + timedelta(hours=24)
                    querydateEnd = querydatePlus1.strftime("%Y%m%d") + "010000"
            else:
                querydate = datetime.now().strftime("%Y%m%d")
                querydateStart = querydate + "010000"
                querydatePlus1 = datetime.now() + timedelta(hours=24)
                querydateEnd = querydatePlus1.strftime("%Y%m%d") + "010000"
            querystring['date'] = {'$gte':querydateStart,'$lte':querydateEnd}
        #else:
        #    querydate = datetime.now().strftime("%Y%m%d")
        #    querystring['date'] = {'$regex':querydate}
        try:
            readquerystring = {}
            readquerystring.update(querystring)
            readquerystring['read'] = 1
            blue_counts = querystring.copy() 
            green_counts = querystring.copy()
            blue_counts['categories'] = ["blue"]
            green_counts['categories'] = ["green"]
            initialData = {'uid':request.session['uid'],'recoverytime':recoverytime,'blue_counts': db.ds.find(blue_counts).count(), 'green_counts': db.ds.find(green_counts).count(), 'querystring': request.POST, 'date': request.POST['date'], 'mail_entries': db.ds.find(querystring,{"html_text":0,"body_text":0}).sort("date",-1).limit(500) , 'counts': db.ds.find(querystring).count(), 'readcounts': db.ds.find(readquerystring).count(),'username': request.session['username'],'access_rights':request.session['accessrights'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']} #            
        except:
            querydate = datetime.now().strftime("%Y%m%d")
            querydateStart = querydate + "010000"
            querydatePlus1 = datetime.now() + timedelta(hours=24)
            querydateEnd = querydatePlus1.strftime("%Y%m%d") + "010000"
            initialData = {'uid':request.session['uid'],'recoverytime':recoverytime,'blue_counts': db.ds.find({"date":{'$regex':querydate},"categories":['blue']}).count(), 'green_counts': db.ds.find({"date":{'$regex':querydate},"categories":['green']}).count(), 'querystring': request.POST, 'date': datetime.now().strftime("%m-%d-%Y"), 'mail_entries': db.ds.find({"date":{'$gte':querydateStart,'$lte':querydateEnd}},{"html_text":0,"body_text":0}).sort("date",-1).limit(500), 'counts': db.ds.find({"date":{'$regex':querydate}}).count(), 'readcounts': db.ds.find({"date":{'$regex':querydate},"read":1}).count(),'username': request.session['username'],'access_rights':request.session['accessrights'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}    #

    else:
        querydate = datetime.now().strftime("%Y%m%d")
        querydateStart = querydate + "010000"
        querydatePlus1 = datetime.now() + timedelta(hours=24)
        querydateEnd = querydatePlus1.strftime("%Y%m%d") + "010000"
        initialData = {'uid':request.session['uid'],'blue_counts': db.ds.find({"date":{'$regex':querydate},"categories":['blue']}).count(), 'green_counts': db.ds.find({"date":{'$regex':querydate},"categories":['green']}).count(), 'querystring': request.POST, 'date': datetime.now().strftime("%m-%d-%Y"), 'mail_entries': db.ds.find({"date":{'$gte':querydateStart,'$lte':querydateEnd}},{"html_text":0,"body_text":0}).sort("date",-1), 'counts': db.ds.find({"date":{'$regex':querydate}}).count(), 'readcounts': db.ds.find({"date":{'$regex':querydate},"read":1}).count(),'username': request.session['username'],'access_rights':request.session['accessrights'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}    #

        #t = Thread(target=insertInCache, args=(querydateStart,querydateEnd))
        #t.start()

    csrfContext = RequestContext(request, initialData)
    return render_to_response('process_it/mailDetails.html', csrfContext)

def getMailBody(request):
    if 'status' in request.POST:
        val = db.ds.find({"id":request.POST['mail_id']})[0]
        mail_id = request.POST['mail_id']
        if request.POST['status'] == 'read':
            db.ds.update({"_id":mail_id},{"$set":{"read":1}},False,True) 
        else:
            db.ds.update({"_id":mail_id},{"$set":{"read":0}},False,True) 
        return HttpResponse('',content_type="text/html")
    else:
        val = db.ds.find({"id":request.POST['mail_id']})[0]
        mail_id = request.POST['mail_id']
        db.ds.update({"_id":mail_id},{"$set":{"read":1}},False,True)
        return render_to_response('process_it/responseMailBody.html', locals())




def getTasks(request):
    data = {'actionType' : 'getTasks', 'tasks': db.ds.find({"flag":1},{'subject':1}), 'counts': db.ds.find({"from":"Vivian.Wang2@Cevalogistics.com"}).count(),}    
    csrfContext = RequestContext(request, data)
    return render_to_response('process_it/mailActionResponse.html', csrfContext)
    
    
    
    
'''        
        lastUpdatedByUser = request.session['username']
        TODAY = date.today()
        NOW = datetime.now().strftime("%H:%M:%S")
        
        cursor = connection.cursor()          
        query =  "INSERT INTO operational_log (mawbNum,userName,date,time, operations) VALUES('" +mawb_string+ "','"+lastUpdatedByUser+"','"+str(TODAY)+"', '"+str(NOW)+"' ,'COB moved to Pre-Alert Processing');"
        cursor.execute(query)  
'''    
def mailAction(request):
    if request.method == 'POST':
        actionType = request.POST['actionType']
        mail_id = request.POST['mail_id']
        mail = db.ds.find({"_id":mail_id})[0]
        categories = mail['categories']
        error = ""
        if actionType == 'setColor':
            color = request.POST['color_id']
            try:
                mbl_num = mail['Mawb']
            except:
                if color == 'green' or color == 'blue': 
                    error = "Mawb does not exist for this mail!"                    
                    return render_to_response('process_it/mailActionResponse.html', locals())
                
            if categories is []:
                categories = [color]
            else:
                if color in categories:
                    categories.remove(color)
                    remove_color_flag = False
                    #print "REMOVE---->",color
                else:
                    categories.append(color)
                    remove_color_flag = True
                    #print "APPEND----->",color


            if color == 'green':
                try:
                    mawb = MawbDetail.objects.get(mawbNum=mbl_num)
                    mawb.station = 'LAX'
                    mawb.papFlag = remove_color_flag
                    mawb.save()
                except MawbDetail.DoesNotExist:
                    if mbl_num:
                        ins_arr = MawbDetail(mawbNum=mbl_num,station='LAX',papFlag=remove_color_flag)
                        ins_arr.save()

            elif color == 'blue':
                try:
                    mawb = MawbDetail.objects.get(mawbNum=mbl_num)
                    mawb.station = 'SFO'
                    mawb.papFlag = remove_color_flag
                    mawb.save()
                except MawbDetail.DoesNotExist:
                    if mbl_num:
                        ins_arr = MawbDetail(mawbNum=mbl_num,station='SFO',papFlag=remove_color_flag)
                        ins_arr.save()

            db.ds.update({"_id":mail_id},{"$set":{"categories":categories}},False,True)
            return render_to_response('process_it/mailActionResponse.html', locals())
        elif actionType == 'delete':
            db.deleted_ds.insert(db.ds.find({"_id":mail_id})[0])
            db.ds.remove({"_id":mail_id})
            return render_to_response('process_it/mailActionResponse.html', locals())
        elif actionType == '1monthOld':
            db.onemonthold_ds.insert(db.ds.find({"_id":mail_id})[0])
            db.ds.remove({"_id":mail_id})
            return render_to_response('process_it/mailActionResponse.html', locals())
        elif actionType == 'flaging':
            try:
                if db.ds.find({"_id":mail_id})[0]['flag'] == 0:
                    db.ds.update({"_id":mail_id},{"$set":{"flag":1}},False,True)
                    flag = 1
                elif db.ds.find({"_id":mail_id})[0]['flag'] == 1:
                    db.ds.update({"_id":mail_id},{"$set":{"flag":2}},False,True)
                    flag = 2
                elif db.ds.find({"_id":mail_id})[0]['flag'] == 2:
                    db.ds.update({"_id":mail_id},{"$set":{"flag":0}},False,True)
                    flag = 0
            except:
                db.ds.update({"_id":mail_id},{"$set":{"flag":1}},False,True)
                flag = 1
            return render_to_response('process_it/mailActionResponse.html', locals())
        else:        
            actionType = 0
            return render_to_response('process_it/mailActionResponse.html', locals())
