# Create your views here.

from process_it.models import MawbDetail, AirLinesDetail
from datetime import date, timedelta as td
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from xlwt import Workbook
from django.utils.simplejson import dumps
import pymongo
import gridfs
import cgitb
from django.db import connection
from datetime import *
import xlwt
from datetime import date
from collections import Counter
import json
import random
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


cgitb.enable()
# this is commmetn
conn = pymongo.Connection("", 27017)
# conn = pymongo.Connection("localhost",27017)
db = conn.process_test
bb_attachments = gridfs.GridFS(db, "bb_attachments") 


msg1=""



def individualProcess(request):
	print "----|------------|------------|---------------|--------------|-------------|--------------|------------------"
	cursor = connection.cursor()
	cursor.execute('SELECT DISTINCT lastUpdatedByUser FROM process_it_mawbdetail ;')
# 	data = cursor.fetchall()
	dnames = [item[0] for item in cursor.fetchall()]

	initialData= {'dnames' : dnames, 'username': request.session['username'],'access_rights':request.session['accessrights'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
	return render_to_response('process_it/individualProcess.html', initialData)



def extAiReport(request):
	global msg1
	
	fromDateFilter = request.POST.get('fromDateFilter', '')
	toDateFilter = request.POST.get('toDateFilter', '')
	usersList = request.POST.get('usersList', '')
	stationOfAi= request.POST.get('stationOfAi', '')
	msg1={}

	cursor = connection.cursor()
	query="SELECT COUNT(aiDesc) FROM process_it_mawbdetail WHERE lastUpdatedDate BETWEEN '"+fromDateFilter+"' AND  '"+toDateFilter+"' AND station='"+stationOfAi+"' AND aiDesc='"+usersList+"' ;"
	print query
	cursor.execute(query)
	noOfAI = cursor.fetchall()
	
	query="SELECT COUNT(shipmentStatus) FROM process_it_mawbdetail WHERE lastUpdatedDate BETWEEN '"+fromDateFilter+"'  AND '"+toDateFilter+"' AND lastUpdatedByUser='"+usersList+"'  AND station='"+stationOfAi+"' AND shipmentStatus='COB' ;"
	print query
	cursor.execute(query)
	totalCobEd = cursor.fetchall()
	
	query="SELECT COUNT(shipmentStatus) FROM process_it_mawbdetail WHERE lastUpdatedDate BETWEEN '"+fromDateFilter+"'  AND '"+toDateFilter+"' AND lastUpdatedByUser='"+usersList+"'  AND station='"+stationOfAi+"' AND shipmentStatus='COB' AND pamFlag='1' ;"
	print query
	cursor.execute(query)
	cobEdRec = cursor.fetchall()
	
	query="SELECT COUNT(aiDesc) FROM process_it_mawbdetail WHERE lastUpdatedDate BETWEEN '"+fromDateFilter+"' AND  '"+toDateFilter+"' AND station='"+stationOfAi+"' ;"
	print query
	cursor.execute(query)
	totalAi = cursor.fetchall()

	msg1['fromDateFilter'] = fromDateFilter
	msg1['toDateFilter'] = toDateFilter
	msg1['noOfAI'] = noOfAI[0][0]	
	msg1['usersList'] = usersList
	msg1['totalCobEd'] = totalCobEd[0][0]
	msg1['stationOfAi'] = stationOfAi	
	msg1['cobEdRec'] = cobEdRec[0][0]
	msg1['totalAi'] = totalAi[0][0]
	
	print "FINAL>> ",msg1
	return HttpResponse(dumps(msg1), content_type='application/json')



def performEvalutation(request):
# 	kwargs = request.session['kwargs']
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	cursor = connection.cursor()
	dateRangeStr=""
	noOfAIStr=""
	cobEdRecStr=""
	mawbNumList=""
	counter=0
	counterP=0	
	
	font = xlwt.Font()  # Create the Font
	font.name = 'Tahoma'
	font.height = 200
	font.bold = True	
	style = xlwt.XFStyle()  # Create the Style
	style.font = font  # Apply the Font to the Style
	
	fromDateFilter = msg1['fromDateFilter']
	toDateFilter = msg1['toDateFilter']
	
	
	
	response['Content-Disposition'] = 'attachment; filename=Performance_Evalutation.xls'
	wb = Workbook()
	ws1 = wb.add_sheet('Non-Confirm')
# 	kwargs['papFlag'] = True
	nonconf_items = ['Date','Masters', 'Name of Processor', 'Station', 'No. of AI Created', 'No. of shipments COBed in Recovery ', 'Total COBed']

	for ids, val in enumerate(nonconf_items):
		ws1.write(0, ids, val,style)
			
	
	
	d1 = datetime.strptime(fromDateFilter, "%Y-%m-%d").date() 
	d2 = datetime.strptime(toDateFilter, "%Y-%m-%d").date()
	print ":::::::::>",d1,d2
	delta = d2 - d1
	for i in range(delta.days + 1):
		print "!~~~~~~~~~~~~~~>",d1 + td(days=i)
		dateRange = d1 + td(days=i)	

		query="SELECT mawbNum FROM process_it_mawbdetail WHERE lastUpdatedDate='"+str(dateRange)+"' AND station='"+msg1['stationOfAi']+"' AND aiDesc='"+msg1['usersList']+"' ;"
		print query
		cursor.execute(query)
		mawbNumL = cursor.fetchall()
		
		query="SELECT COUNT(aiDesc),mawbNum FROM process_it_mawbdetail WHERE lastUpdatedDate='"+str(dateRange)+"' AND station='"+msg1['stationOfAi']+"' AND aiDesc='"+msg1['usersList']+"' ;"
		print query
		cursor.execute(query)
		noOfAI = cursor.fetchall()

		query="SELECT COUNT(shipmentStatus) FROM process_it_mawbdetail WHERE lastUpdatedDate='"+str(dateRange)+"' AND lastUpdatedByUser='"+msg1['usersList']+"'  AND station='"+msg1['stationOfAi']+"' AND shipmentStatus='COB' AND pamFlag='1' ;"
		print query
		cursor.execute(query)
		cobEdRec = cursor.fetchall()
		

		dateRangeStr += str(dateRange)+', '
		noOfAIStr += str(noOfAI[0][0])+', '
		cobEdRecStr += str(cobEdRec[0][0])+', '
		mawbNumList += str(mawbNumL)+', '
		
			
# 		for i,j,k,l in itertools.izip_longest(dateRangeStr.split(", "),noOfAIStr.split(", "),cobEdRecStr.split(", "),mawbNumList.split(", ")):
# 			print i," -- ",j," -- ",k," -- ",l
# 		


		ws1.write(counter+ counterP + 1, 0, str(dateRange)) 
	
		ws1.write(counter + counterP + 1, 2, str(msg1['usersList']))
		ws1.write(counter + counterP + 1, 4, noOfAI[0][0])	
		ws1.write(counter + counterP + 1, 5, str(cobEdRec[0][0]))	
		ws1.write(counter + counterP + 1, 3, str(msg1['stationOfAi'])) 	
		ws1.write(counter + counterP + 1, 6, msg1['totalCobEd'])
		

		for i in mawbNumL:
			ws1.write(counter + counterP + 1, 1, str(i).replace("(u'","").replace("',)","").replace("(","").replace(")",""))
			counterP +=1
					
		
		
		
		counter+=1			
		
		


	print dateRangeStr," ||| ",noOfAIStr," ||| " ,cobEdRecStr," ||| " ,	mawbNumList
	
	

		

	
	wb.save(response)
	return response







def charts(request):
	
	count= request.POST.get('count', '')
	mawb= request.POST.get('mawb', '')
	etaDate_list= request.POST.get('etaDate_list', '') 
	process_status= request.POST.get('process_status', '')

	mawb=str(mawb)
	etaDate_list=str(etaDate_list)
	process_status=str(process_status)
	
# 	print mawb
# 	print etaDate_list 	print process_status
	
	zipped=zip(mawb.split(','),etaDate_list.split(','),process_status.split(','))
#	print "Zzipped: ",zipped	

	
	res = {}
	json=[]
	for _, pDate, vStatus in zipped:
		if pDate not in res:
# 			res[pDate] = [[vStatus], 1]			
			if vStatus == 'Processed':
				res[pDate] = [1,0]
			else:
				res[pDate] = [0,1]            
		else:       
			if vStatus == 'Processed':
				res[pDate][0] += 1
			else:
				res[pDate][1] += 1  
# 			res[pDate][0].append(vStatus)
# 			res[pDate][1] += 1
							
#	print "RES: ",res
	
	json.append(["Date", "Processed", "Pending"])
	for pDate,vStatus in res.iteritems():
		temp=[pDate,vStatus]
#		print temp
		t=[temp[0]]
		t.extend(temp[1])
#		print "T:",t
		json+=[t]
#	print "~~~~~>",json
	return HttpResponse(dumps(json),content_type='application/json')



def mawbByDate(request): 
	global data
	cursor = connection.cursor() 
	
	if request.method == 'POST':
		try:
			dateRet = request.POST['dateRet']
			mawListDwStation = request.POST['mawListDwStation']
			# dateRet= '2013-03-13'
			cursor.execute("SELECT mawbNum,station,consoleNumber,etaDate FROM process_it_mawbdetail WHERE preAlertReceivedDate='" + dateRet + "' AND station='"+ mawListDwStation +"' ;")
			data = cursor.fetchall()
		except:
			dateRet = datetime.now().strftime("%Y-%m-%d")
			mawListDwStation = 'LAX'
			print "Date:::::",dateRet		
			cursor.execute("SELECT mawbNum,station,consoleNumber,etaDate FROM process_it_mawbdetail WHERE preAlertReceivedDate='" + dateRet + "'AND station='"+ mawListDwStation +"' ;")
			data = cursor.fetchall()	
	x = 1
	y = 0
	z = 0
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=mawbSheet.xls' 	
	font = xlwt.Font()  # Create the Font
	font.name = 'Times New Roman'
	font.bold = True
	style = xlwt.XFStyle()  # Create the Style
	style.font = font  # Apply the Font to the Style
	workbook = Workbook()
	worksheet = workbook.add_sheet(datetime.now().strftime("%Y-%m-%d"))
	head = ['Master', 'Station', 'Console No.','Eta Date']
	for h in head:
		worksheet.write(0, z, h, style)
		z += 1	
	for i in data:
		print ">",i
		for j in i:
			worksheet.write(x, y, j)
			y += 1
			if y >= 4:
				y = 0
				x += 1	
	workbook.save(response)	
	return response


def displayAllLog(request): 	 	
	''' View All Logs '''
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM operational_log ORDER BY id DESC ;')
	data1 = cursor.fetchall()	
	contact_list = data1
	paginator = Paginator(contact_list, 25) 
	page = request.GET.get('page')
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)
		
	initialData= {'data' : data, 'username': request.session['username'],'access_rights':request.session['accessrights'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
	return render_to_response('process_it/displayLog.html', initialData)







def displayLog(request):			
	'''  Search Logs '''
	cursor = connection.cursor()
	data = []
	if request.method == 'POST':
		mawb = request.POST['mawb']		
		query="SELECT * FROM operational_log WHERE mawbNum=('"+mawb+"');"
		print "Query: ",query;
	else:
		query="SELECT * FROM operational_log ORDER BY id DESC;"
		
	cursor.execute(query)	
	data1 = cursor.fetchall()
	
	contact_list = data1
	paginator = Paginator(contact_list, 25) 
	page = request.GET.get('page')
	try:
		data = paginator.page(page)
	except PageNotAnInteger:
		data = paginator.page(1)
	except EmptyPage:
		data = paginator.page(paginator.num_pages)
	
	
	
	initialData= {'data' : data, 'username': request.session['username'],'access_rights':request.session['accessrights'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
	return render_to_response('process_it/displayLog.html', initialData)



def airLinesDetails(request):
	if 'username' not in request.session:
		csrfContext = RequestContext(request)
		return render_to_response('process_it/loginPage.html', csrfContext)
	arr = AirLinesDetail.objects.all()
	initialData = {'arr' : arr, 'username' : request.session['username'], 'access_rights':request.session['accessrights'], 'screen_width':request.session['screen_width'], 'screen_height':request.session['screen_height']}
	csrfContext = RequestContext(request, initialData)
	return render_to_response('process_it/airLinesDetail.html', csrfContext)

def setClassCredentials(request):
	if request.method == 'POST': 
		if request.POST.get('class_uname', ''):
			request.session['class_uname'] = request.POST['class_uname']
		if request.POST.get('class_pass', ''):
			request.session['class_pass'] = request.POST['class_pass']
		actionType = 'update'
		return render_to_response('process_it/mailActionResponse.html', locals())

def downloadAttachment(request):
	file_data = db.bb_attachments.files.find({"_id":request.GET['id']})[0]
	response = HttpResponse(bb_attachments.get(request.GET['id']).read(), content_type=file_data['contentType'])
	response['Content-Disposition'] = 'attachment; filename=' + request.GET['nm']
	return response




def exportExcel(request):				
	''' Pre-alert Master Sheet Download function. '''
	kwargs = request.session['kwargs']
	blank_list = []
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=LAX_recovery.xls'
	
	font = xlwt.Font()  # Create the Font
	font.name = 'Tahoma'
	font.height = 200
	font.bold = True	
	
	style = xlwt.XFStyle()  # Create the Style
#	style = xlwt.easyxf('pattern: pattern solid; font:height 720;')
#	style.pattern.pattern_fore_colour =46
	style.font = font  # Apply the Font to the Style

	wb = Workbook()
	ws = wb.add_sheet('Confirm')		
	#ws.col(0).width = 9999 # 3333 = 1" (one inch).

	conf_items = ['MAWB #', 'File / Consolidation #', 'PMC', 'Loose', 'Total Pcs', 'Total Weight ', 'Firms Code', 'Est. Arrival/Landing Date', 'Est. Arrival/Landing Time', 'OFF SHORE COMMENTS', 'Remarks/Issues', 'HBL Count']
	for ids, val in enumerate(conf_items):
		ws.write(0, ids, val,style)
		
	mawbs = MawbDetail.objects.filter(**kwargs).order_by('-etaDate', '-etaTime', 'mawbNum').exclude(station='DFW').exclude(station='DFW/U').exclude(station='IAH').values()
	# update_mawbs = MawbDetail.objects.filter( **kwargs ).update(pamFlag=False)
	for ids, mbl in enumerate(mawbs):		
#		mawbSplit= mbl['mawbNum'].split('-')
#		ws.write(ids + 1, 0, mawbSplit[0])
		ws.write(ids + 1, 0, mbl['mawbNum'])
		ws.write(ids + 1, 1, mbl['consoleNumber'])
		if mbl['pmcOrLoose'] == 'Loose':
			ws.write(ids + 10, 3, 'X')
		else:
			ws.write(ids + 1, 2, mbl['pmcOrLoose'])
		ws.write(ids + 1, 4, mbl['slac'])
		ws.write(ids + 1, 5, mbl['chgWeight'])
		ws.write(ids + 1, 6, 'Z493')
		if mbl['etaDate'] is not None: ws.write(ids + 1, 7, (mbl['etaDate']).strftime("%d"))  # .strftime("%d")
		if mbl['etaTime'] is not None: ws.write(ids + 1, 8, (mbl['etaTime']).strftime("%H%M"))  # .strftime("%H%M")
		if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
			
#			tempstr1 = "COB " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
			

			for icount in mbl['mawbNum']:  # COB 
				blank_list.append(icount)
				check = blank_list[-1]
				
				if mbl['flightCode']=='TRUCK':
					
					if mbl['trackSource'] == 'WEB':
						
						if check.isdigit() is False:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  #  COB TRUCK/23@1740 PER WEB [Part D]
								tempstr1 = str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) +  "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource']) + " [Part " + check + "] PC=" +str(mbl['slac'])
							else:
								tempstr1 = ""
						else:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  #  COB TRUCK/23@1740 PER WEB
								tempstr1 =  str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
							else:
								tempstr1 = ""
					else:
						if check.isdigit() is False:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  #  COB TRUCK/23@1740 PER CALL NIK [Part D]
								tempstr1 =  str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])+ " "+str(mbl['speakWith']) + " [Part " + check + "] PC="+str(mbl['slac'])
							else:
								tempstr1 = ""
						else:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  #  COB TRUCK/23@1740 PER CALL NIK
								tempstr1 =  str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])+" " +str(mbl['speakWith'])
							else:
								tempstr1 = ""		
								
				else:	
					if mbl['trackSource'] == 'WEB':
						
						if check.isdigit() is False:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  #  COB NH1006/23@1740 PER WEB [Part D]
								tempstr1 =  str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource']) + " [Part " + check + "] PC=" +str(mbl['slac'])
							else:
								tempstr1 = ""
						else:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  #  COB NH1006/23@1740 PER WEB
								tempstr1 = str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
							else:
								tempstr1 = ""
								
					else:
						if check.isdigit() is False:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  #  COB NH1006/23@1740 PER CALL NIK [Part D]
								tempstr1 =  str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])+ " "+str(mbl['speakWith']) + " [Part " + check + "] PC="+str(mbl['slac'])
							else:
								tempstr1 = ""
						else:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  #  COB NH1006/23@1740 PER CALL NIK
								tempstr1 = str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])+" " +str(mbl['speakWith'])
							else:
								tempstr1 = ""					
		
			
			
			
		else:
			tempstr1 = ""
		ws.write(ids + 1, 10, tempstr1)
#		ws.write(ids + 1, 11, mbl['remarksInClass'])
		ws.write(ids + 1, 11, mbl['oneFStatus'])


	ws1 = wb.add_sheet('Non-Confirm')
	del kwargs['pamFlag']
	kwargs['papFlag'] = True
	nonconf_items = ['MAWB #', 'File / Consolidation #', 'Firms Code', 'Flight Code', 'Flight Num', 'Est. Arrival/Landing Date', 'Est. Arrival/Landing Time', 'Shipment status', 'OFF SHORE COMMENTS', 'Remarks/Issues', 'Station']
	for ids, val in enumerate(nonconf_items):
		ws1.write(0, ids, val)
	mawbs = MawbDetail.objects.filter(**kwargs).order_by('-etaDate', '-etaTime', 'mawbNum').exclude(station='DFW').exclude(station='DFW/U').exclude(station='IAH').values()
	for ids, mbl in enumerate(mawbs):
		ws1.write(ids + 1, 0, mbl['mawbNum'])
		ws1.write(ids + 1, 1, mbl['consoleNumber'])
		ws1.write(ids + 1, 2, 'Z493')
		ws1.write(ids + 1, 3, mbl['flightCode'])
		ws1.write(ids + 1, 4, mbl['flightNum'])
		if mbl['etaDate'] is not None: ws1.write(ids + 1, 5, (mbl['etaDate']).strftime("%d"))
		if mbl['etaTime'] is not None: ws1.write(ids + 1, 6, (mbl['etaTime']).strftime("%H%M"))
		ws1.write(ids + 1, 7, mbl['shipmentStatus'])
		if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
			tempstr = "BO " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
		else:
			tempstr = ""
		if mbl['etaDate'] is not None: ws1.write(ids + 1, 8, tempstr)
		ws1.write(ids + 1, 9, mbl['remarksInClass'])
		ws1.write(ids + 1, 10, mbl['station'])
	wb.save(response)
	return response



def DFWexportExcel(request):				
	''' DFW/IAH Master Sheet Download function. '''
	etaDate=""
	etaTime=""
	kwargs = request.session['kwargs']
	blank_list = []
	response = HttpResponse(mimetype='application/vnd.ms-excel')
	response['Content-Disposition'] = 'attachment; filename=DFW_recovery.xls'
	
	font = xlwt.Font()  # Create the Font
	font.name = 'Tahoma'
	font.height = 200
	font.bold = True	
	
	style = xlwt.XFStyle()  # Create the Style

	style.font = font  # Apply the Font to the Style

	wb = Workbook()
	ws = wb.add_sheet('DFW_Confirm')		
	TODAY = date.today()	

	ws.write(1, 0, 'In Bond Transfer', style)
	ws.write(2, 0, "Delivery Address:  Eagle Global Logistics 1901 West Airfield Drive DFW Airport, TX 75261", style)
	ws.write(3, 0, 'Firms Code: V484', style)	
	ws.write(4, 0, " ***Nominate bond transfer to Eagle firms code V484***", style)
	ws.write(5, 0, "Transfer Date:", style)
	ws.write(5, 1, TODAY, style)
	conf_items = ['Pre-Fix','MAWB #', 'File / Consolidation #', 'PMC', 'Loose', 'Total Pcs', 'Total Weight ', 'Firms Code', 'Est. Arrival/Landing Time', 'OFF SHORE COMMENTS', 'Remarks/Issues', 'HBL Count']
	for ids, val in enumerate(conf_items):
		ws.write(9, ids, val,style)		
	mawbs = MawbDetail.objects.filter(**kwargs).order_by('-etaDate', '-etaTime', 'mawbNum').exclude(station='LAX').exclude(station='SFO').exclude(station='IAH').values()
	for ids, mbl in enumerate(mawbs):		
		mawbSplit= mbl['mawbNum'].split('-')
		ws.write(ids + 10, 0, mawbSplit[0])
		ws.write(ids + 10, 1, mawbSplit[1])
		ws.write(ids + 10, 2, mbl['consoleNumber'])
		
# 		if mbl['pmcOrLoose'] == 'LOOSE':
# 			ws.write(ids + 10, 4, 'X')
# 		else:
# 			ws.write(ids + 10, 3, mbl['pmcOrLoose'])

		if mbl['pmcOrLoose'] == 'LOOSE':
			ws.write(ids + 10, 4, 'Y')
			ws.write(ids + 10, 3, "N")			
		else:
			ws.write(ids + 10, 3, "Y")
			ws.write(ids + 10, 4, "N")				
			
		ws.write(ids + 10, 5, mbl['slac'])
		ws.write(ids + 10, 6, mbl['chgWeight'])
		ws.write(ids + 10, 7, ' ')
#		if mbl['etaDate'] is not None: ws.write(ids + 10, 8, (mbl['etaDate']).strftime("%d"))  # .strftime("%d")
#		if mbl['etaTime'] is not None: ws.write(ids + 10, 9, (mbl['etaTime']).strftime("%H%M"))  # .strftime("%H%M")
		if mbl['etaDate'] is not None: 
			etaDate= (mbl['etaDate']).strftime("%d")  
		if mbl['etaTime'] is not None: 
			etaTime= (mbl['etaTime']).strftime("%H%M")
		ws.write(ids + 10, 8, etaTime+'/'+etaDate)		

		if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
			tempstr1 = "COB " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
		else:
			tempstr1 = ""
		ws.write(ids + 10, 9, tempstr1)
#		ws.write(ids + 1, 11, mbl['remarksInClass'])
		ws.write(ids + 10, 11, mbl['oneFStatus'])

	ws0 = wb.add_sheet('IAH_Confirm')
	ws0.write(1, 0, 'In Bond Transfer', style)
	ws0.write(2, 0, "Delivery Address:  Eagle Global Logistics 15370 Vickery Dr,Houston,TX 77032", style)
	ws0.write(3, 0, 'Firms Code: V435', style)		
	ws0.write(4, 0, " ***Nominate bond transfer to Eagle firms code V435***", style)
	ws0.write(5, 0, "Transfer Date:", style)
	ws0.write(5, 1, TODAY, style)
	conf_items = ['Pre-Fix','MAWB #', 'File / Consolidation #', 'PMC', 'Loose', 'Total Pcs', 'Total Weight ', 'Firms Code', 'Est. Arrival/Landing Time', 'OFF SHORE COMMENTS', 'Remarks/Issues', 'HBL Count']
	for ids, val in enumerate(conf_items):
		ws0.write(9, ids, val,style)		
	mawbs = MawbDetail.objects.filter(**kwargs).order_by('-etaDate', '-etaTime', 'mawbNum').exclude(station='LAX').exclude(station='SFO').exclude(station='DFW').values()
	for ids, mbl in enumerate(mawbs):		
		mawbSplit= mbl['mawbNum'].split('-')
		ws0.write(ids + 10, 0, mawbSplit[0])
		ws0.write(ids + 10, 1, mawbSplit[1])
		ws0.write(ids + 10, 2, mbl['consoleNumber'])
		
		if mbl['pmcOrLoose'] == 'LOOSE':
			ws0.write(ids + 10, 4, 'Y')
			ws0.write(ids + 10, 3, "N")			
		else:
			ws0.write(ids + 10, 3, "Y")
			ws0.write(ids + 10, 4, "N")	
			
		ws0.write(ids + 10, 5, mbl['slac'])
		ws0.write(ids + 10, 6, mbl['chgWeight'])
		ws0.write(ids + 10, 7, ' ')
		if mbl['etaDate'] is not None: 
			etaDate= (mbl['etaDate']).strftime("%d")  
		if mbl['etaTime'] is not None: 
			etaTime= (mbl['etaTime']).strftime("%H%M")
		ws0.write(ids + 10, 8, etaTime+'/'+etaDate)					
		if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
			tempstr1 = "COB " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
		else:
			tempstr1 = ""
		ws0.write(ids + 10, 9, tempstr1)
		ws0.write(ids + 10, 11, mbl['oneFStatus'])

	ws1 = wb.add_sheet('Non-Confirm')
	del kwargs['pamFlag']
	kwargs['papFlag'] = True
	nonconf_items = ['MAWB #', 'File / Consolidation #', 'Firms Code', 'Flight Code', 'Flight Num', 'Est. Arrival/Landing Date', 'Est. Arrival/Landing Time', 'Shipment status', 'OFF SHORE COMMENTS', 'Remarks/Issues', 'Station', 'HBL Count']
	for ids, val in enumerate(nonconf_items):
		ws1.write(0, ids, val, style)
	mawbs = MawbDetail.objects.filter(**kwargs).filter(shipmentStatus="ETA").order_by('-etaDate', '-etaTime', 'mawbNum').exclude(station='LAX').exclude(station='SFO').values()
	for ids, mbl in enumerate(mawbs):
		ws1.write(ids + 1, 0, mbl['mawbNum'])
		ws1.write(ids + 1, 1, mbl['consoleNumber'])
		ws1.write(ids + 1, 2, ' ')
		ws1.write(ids + 1, 3, mbl['flightCode'])
		ws1.write(ids + 1, 4, mbl['flightNum'])
		if mbl['etaDate'] is not None: ws1.write(ids + 1, 5, (mbl['etaDate']).strftime("%d"))
		if mbl['etaTime'] is not None: ws1.write(ids + 1, 6, (mbl['etaTime']).strftime("%H%M"))
		ws1.write(ids + 1, 7, mbl['shipmentStatus'])
		if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
			tempstr = "BO " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
		else:
			tempstr = ""
		if mbl['etaDate'] is not None: ws1.write(ids + 1, 8, tempstr)
		ws1.write(ids + 1, 9, mbl['remarksInClass'])
		ws1.write(ids + 1, 10, mbl['station'])
		ws1.write(ids + 1, 11, mbl['oneFStatus'])
	wb.save(response)
	return response



def preAlertExcel(request):
	kwargs = request.session['kwargs']
	response = HttpResponse(mimetype='application/vnd.ms-excel')

	response['Content-Disposition'] = 'attachment; filename=BookingOnly.xls'
	wb = Workbook()
	ws1 = wb.add_sheet('Non-Confirm')
	kwargs['papFlag'] = True
	nonconf_items = ['Station', 'MAWB #', 'File / Consolidation #', 'Customer', 'It Information', 'Flight Code', 'Flight #', 'ETA Date', 'ETA Time', 'Shipment Status', 'PER', 'S/W', 'PMC/Loose', 'SLAC', 'Chg. Wght.', 'OFF SHORE COMMENTS', '1F Status', 'Last Updated Date', 'Last Updated Time', 'Last Upated By', 'Comment.']
	# nonconf_items = ['Station','MAWB #','File / Consolidation #','Firms Code','Est. Arrival/Landing Date','Est. Arrival/Landing Time','OFF SHORE COMMENTS','Remarks/Issues']
	for ids, val in enumerate(nonconf_items):
		ws1.write(0, ids, val)
	mawbs = MawbDetail.objects.filter(**kwargs).order_by('-etaDate', '-etaTime', 'mawbNum').values()
	for ids, mbl in enumerate(mawbs):
		ws1.write(ids + 1, 0, mbl['station'])
		ws1.write(ids + 1, 1, mbl['mawbNum'])
		ws1.write(ids + 1, 2, mbl['consoleNumber'])
		ws1.write(ids + 1, 3, mbl['customer'])
		ws1.write(ids + 1, 4, mbl['itInfo'])
		ws1.write(ids + 1, 5, mbl['flightCode'])
		ws1.write(ids + 1, 6, mbl['flightNum'])
		if mbl['etaDate'] is not None: ws1.write(ids + 1, 7, (mbl['etaDate']).strftime("%d"))
		if mbl['etaTime'] is not None: ws1.write(ids + 1, 8, (mbl['etaTime']).strftime("%H%M"))
		ws1.write(ids + 1, 9, mbl['shipmentStatus'])
		ws1.write(ids + 1, 10, mbl['trackSource'])
		ws1.write(ids + 1, 11, mbl['speakWith'])
		ws1.write(ids + 1, 12, mbl['pmcOrLoose'])
		ws1.write(ids + 1, 13, mbl['slac'])
		ws1.write(ids + 1, 14, mbl['chgWeight'])
		ws1.write(ids + 1, 15, mbl['remarksInClass'])
		ws1.write(ids + 1, 16, mbl['oneFStatus'])
		if mbl['lastUpdatedDate'] is not None: ws1.write(ids + 1, 17, (mbl['lastUpdatedDate']).strftime("%d"))
		if mbl['lastUpdatedTime'] is not None: ws1.write(ids + 1, 18, (mbl['lastUpdatedTime']).strftime("%H%M"))
		ws1.write(ids + 1, 19, mbl['lastUpdatedByUser'])
		ws1.write(ids + 1, 20, mbl['oneFStatusComment'])
	wb.save(response)
	return response



def validateMawbEntry(request):
	msg = {}
	if request.method == 'POST':
		if request.POST.get('mawbNum', ''):
# 			mawbObj = MawbDetail.objects.get(mawbNum=request.POST['mawbNum'])
# 			pap = mawbObj.papFlag
# 			print "---", pap

			try:
				mawbObj = MawbDetail.objects.get(mawbNum=request.POST['mawbNum'])
				pap = mawbObj.papFlag
				print "--->", mawbObj , "---", pap
				if mawbObj.papFlag == True:
					msg['exists'] = 1
				else:
					msg['exists'] = 2
			except MawbDetail.DoesNotExist:
				print "except block"
				msg['exists'] = 0
	return HttpResponse(dumps(msg), content_type='application/json')


'''
def uploadBOSheet(request):
	msg = {}
	if request.method == 'POST':
		form_data = cgi.FieldStorage()
		docfile = form_data['boFile']
		#docfile = request.FILES['boFile'] #request.POST['boFile']
		msg['filename'] = os.path.basename(docfile.filename)	
		
	return HttpResponse(dumps(msg),content_type='application/json')



def insertInCache(querydateStart,querydateEnd):
	data = db.ds.find({"date":{'$gte':querydateStart,'$lte':querydateEnd}},{"html_text":1,"body_text":1,"id":1})
	for entry in data: #db.ds.find({"date":{'$gte':querydateStart,'$lte':querydateEnd}},{"html_text":1,"body_text":1,"id":1}):
		cache.set(entry['id'], entry, 1500)


def deleteMawb(mblid):
	mawb = MawbDetail.objects.get(mawbNum=mblid)
	mawb.delete()

def moveToMaster(mblid):
	mawb = MawbDetail.objects.get(mawbNum=mblid)
	mawb.pamFlag = True
	mawb.papFlag = False
	mawb.save()
	
def moveBack(mblid):
	mawb = MawbDetail.objects.get(mawbNum=mblid)
	mawb.pamFlag = False
	mawb.papFlag = True
	mawb.save()

def moveInscope(request):
	idval = request.POST['id']
	doc = db.ds.find({"_id":idval})[0]
	try:
		msg = "This mawb is already exists in Pre Alert page."		
		data = MawbDetail.objects.get(mawbNum=unicode(doc['Mawb']))
		data.preAlertReceivedDate = datetime.strptime(doc['date'],"%m-%d-%Y")
		data.mawbNum = doc['Mawb']
		data.etdDate = datetime.strptime(doc['etd'],"%d-%b-%Y %H:%M").strftime("%Y-%m-%d")
		data.etdTime = datetime.strptime(doc['etd'],"%d-%b-%Y %H:%M").strftime("%H:%M")
		data.etaDate = datetime.strptime(doc['eta'],"%d-%b-%Y %H:%M").strftime("%Y-%m-%d")
		data.etaTime = datetime.strptime(doc['eta'],"%d-%b-%Y %H:%M").strftime("%H:%M")
		data.flightNum = doc['flight_num']
		data.save()
		return render_to_response('process_it/temp.html', locals())
	except MawbDetail.DoesNotExist:
		msg = "This mawb is moved to Pre Alert page."
		data = MawbDetail(preAlertReceivedDate=doc['date'],mawbNum=doc['Mawb'],etdDate=datetime.strptime(doc['etd'],"%d-%b-%Y %H:%M").strftime("%m-%d-%Y"),etdTime=datetime.strptime(doc['etd'],"%d-%b-%Y %H:%M").strftime("%H:%M"),etaDate=datetime.strptime(doc['eta'],"%d-%b-%Y %H:%M").strftime("%m-%d-%Y"),etaTime=datetime.strptime(doc['eta'],"%d-%b-%Y %H:%M").strftime("%H:%M"),flightNum=doc['flight_num'],)
		data.save()
		return render_to_response('process_it/temp.html', locals())
		
	
	#writer = csv.writer(response)
	#field_items = ['station','preAlertReceivedDate','mawbNum','etaDate','etaTime','etdDate','etdTime','flightNum']
	#field_names = map(lambda x: MawbDetailkeys[x] , field_items)
	# Write a first row with header information	
	#writer.writerow(field_names)	
	#mawbs = MawbDetail.objects.filter( **kwargs ).values(*field_items)
	#for mbl in mawbs:
	#	writer.writerow(map(lambda x: mbl[x] , field_items)) 
	
	return response

def updateEntry(request):
	file_data = db.bb_attachments.files.find({"_id":request.GET['id']})[0]
	response = HttpResponse(bb_attachments.get(request.GET['id']).read(), content_type=file_data['contentType'])
	response['Content-Disposition'] = 'attachment; filename='+request.GET['nm']
	return response	

mawb_dict = {}			
def updateMawbStatus(mbl,request,mawb_dict):
	mawb = MawbDetail.objects.get(mawbNum=mbl)
	if not mawb.paLocked:
		mawb.paLocked = True
		mawb.paLockedByUser = request.session['username']
		mawb.save()
		mawb_dict[mbl] = 1
	elif mawb.paLocked == True and mawb.paLockedByUser == request.session['username']:
		mawb.paLocked = False
		mawb.paLockedByUser = ''
		mawb.save()
		mawb_dict[mbl] = 2
	else:
		mawb_dict[mbl] = 0
'''



def export_excel_new(request):
	blank_list = []
	kwargs = request.session['kwargs']
	response = HttpResponse(mimetype='application/vnd.ms-excel')

	response['Content-Disposition'] = 'attachment; filename=BookingOnly.xls'
	wb = Workbook()
	ws11 = wb.add_sheet('Non-Confirm')
	kwargs['papFlag'] = True
	nonconf_items = ['Station', 'MAWB #', 'File / Consolidation #', 'Customer', 'It Information', 'Flight Code', 'Flight #', 'ETA Date', 'ETA Time', 'Shipment Status', 'PER', 'S/W', 'PMC/Loose', 'SLAC', 'Chg. Wght.', 'OFF SHORE COMMENTS', '1F Status', 'Last Updated Date', 'Last Updated Time', 'Last Upated By', 'Comment.']
	# nonconf_items = ['Station','MAWB #','File / Consolidation #','Firms Code','Est. Arrival/Landing Date','Est. Arrival/Landing Time','OFF SHORE COMMENTS','Remarks/Issues']
	for ids, val in enumerate(nonconf_items):
		ws11.write(0, ids, val)
	mawbs = MawbDetail.objects.filter(**kwargs).order_by('-etaDate', '-etaTime', 'mawbNum').values()
	for ids, mbl in enumerate(mawbs):
		ws11.write(ids + 1, 0, mbl['station'])
		ws11.write(ids + 1, 1, mbl['mawbNum'])
		ws11.write(ids + 1, 2, mbl['consoleNumber'])
		ws11.write(ids + 1, 3, mbl['customer'])
		ws11.write(ids + 1, 4, mbl['itInfo'])
		ws11.write(ids + 1, 5, mbl['flightCode'])
		ws11.write(ids + 1, 6, mbl['flightNum'])
		if mbl['etaDate'] is not None: ws11.write(ids + 1, 7, (mbl['etaDate']).strftime("%d"))
		if mbl['etaTime'] is not None: ws11.write(ids + 1, 8, (mbl['etaTime']).strftime("%H%M"))
		ws11.write(ids + 1, 9, mbl['shipmentStatus'])
		ws11.write(ids + 1, 10, mbl['trackSource'])
		ws11.write(ids + 1, 11, mbl['speakWith'])
		ws11.write(ids + 1, 12, mbl['pmcOrLoose'])
		ws11.write(ids + 1, 13, mbl['slac'])
		ws11.write(ids + 1, 14, mbl['chgWeight'])



########################## SFO

# 		if str(mbl['station']) == 'SFO' or 'SFO ' or ' SFO' or ' SFO ':
# 			if str(mbl['shipmentStatus']) == 'NB' :
# 				for icount in mbl['mawbNum']:
# 					blank_list.append(icount)
# 					check = blank_list[-1]
# 					if check.isdigit() is False:
# 						if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
# 							if mbl['trackSource'] == 'WEB':
# 								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO BOOKING " + " PER " + str(mbl['trackSource']) + " [Part " + check + "]"
# 							else:
# 								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO BOOKING " + " S/W " + str(mbl['speakWith'])
# 						else:
# 							tempstr1 = ""
#
# 					else:
# 						if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
# 							if mbl['trackSource'] == 'WEB':
# 								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO BOOKING " + " PER " + str(mbl['trackSource'])
# 							else:
# 								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO BOOKING " + " S/W " + str(mbl['speakWith'])
#
# 						else:
# 							tempstr1 = ""
#
# 			elif str(mbl['shipmentStatus']) == 'NI':
# 				for icount in mbl['mawbNum']:
# 					blank_list.append(icount)
# 					check = blank_list[-1]
# 					if check.isdigit() is False:
# 						if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
# 							if mbl['trackSource'] == 'WEB':  # 1930  NO INFORMATION  PER WEB [Part D]
# 									tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO INFORMATION " + " PER " + str(mbl['trackSource']) + " [Part " + check + "]"
# 							else:
# 									tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO INFORMATION " + " S/W " + str(mbl['speakWith'])
# 						else:
# 							tempstr1 = ""
# 					else:
# 						if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
# 							if mbl['trackSource'] == 'WEB':
# 									tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO INFORMATION " + " PER " + str(mbl['trackSource'])
# 							else:
# 									tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO INFORMATION " + " S/W " + str(mbl['speakWith'])
# 						else:
# 							tempstr1 = ""

# 			elif str(mbl['shipmentStatus']) == 'BO' :
# 				for icount in mbl['mawbNum']:
# 					blank_list.append(icount)
# 					check = blank_list[-1]
# 					if check.isdigit() is False:
# 						if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
# 							tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource']) + " [Part " + check + "]"
# 						else:
# 							tempstr1 = ""
# 					else:
# 						if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
# 							tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
# 						else:
# 							tempstr1 = ""


#
# 			else:  # str(mbl['shipmentStatus'])+ == 'COB' :
# 				for icount in mbl['mawbNum']:
# 					blank_list.append(icount)
# 					check = blank_list[-1]
# 					if check.isdigit() is False:
# 						if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
# 							tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource']) + " " + str(mbl['oneFStatusComment']) + " [Part " + check + "]"
# 						else:
# 							tempstr1 = ""
# 					else:
# 						if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
# 							tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource']) + " " + str(mbl['oneFStatusComment'])
# 						else:
# 							tempstr1 = ""



################################## LAX or other
# 		else:
		if str(mbl['shipmentStatus']) == 'NB' :  # or 'NI':
			for icount in mbl['mawbNum']:
				blank_list.append(icount)
				check = blank_list[-1]
				if check.isdigit() is False:
					if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
						if mbl['trackSource'] == 'WEB':
							tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO BOOKING " + " PER " + str(mbl['trackSource']) + " [Part " + check + "]"  # 	1930  NO BOOKING  PER WEB [Part D]
						else:
							tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO BOOKING " + " S/W " + str(mbl['speakWith'])  # 	1748  NO BOOKING  S/W nik
					else:
						tempstr1 = ""

				else:
					if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
						if mbl['trackSource'] == 'WEB':
							tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO BOOKING " + " PER " + str(mbl['trackSource'])  # 	1930  NO BOOKING  PER WEB
						else:
							tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO BOOKING " + " S/W " + str(mbl['speakWith'])  # 	1748  NO BOOKING  S/W nik

					else:
						tempstr1 = ""

		elif str(mbl['shipmentStatus']) == 'NI':
			for icount in mbl['mawbNum']:
				blank_list.append(icount)
				check = blank_list[-1]
				if check.isdigit() is False:
					if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
						if mbl['trackSource'] == 'WEB':  # 1930  NO INFORMATION  PER WEB [Part D]
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO INFORMATION " + " PER " + str(mbl['trackSource']) + " [Part " + check + "]"  # 	1930  NO INFORMATION  PER WEB [Part D]
						else:
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO INFORMATION " + " S/W " + str(mbl['speakWith'])  # 	1748  NO INFORMATION  S/W nik
					else:
						tempstr1 = ""
				else:
					if mbl['etaDate'] is not None and mbl['etaTime'] is not None:
						if mbl['trackSource'] == 'WEB':
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO INFORMATION " + " PER " + str(mbl['trackSource'])  # 	1930  NO INFORMATION  PER WEB
						else:
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + " NO INFORMATION " + " S/W " + str(mbl['speakWith'])  # 	1748  NO INFORMATION  S/W nik
					else:
						tempstr1 = ""

		else:
			for icount in mbl['mawbNum']:  # COB or BO
				blank_list.append(icount)
				check = blank_list[-1]
				
				if mbl['flightCode']=='TRUCK':
					
					if mbl['trackSource'] == 'WEB':
						
						if check.isdigit() is False:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  # 1955 BO TRUCK/23@1740 PER WEB [Part D]
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) +  "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource']) + " [Part " + check + "] PC=" +str(mbl['slac'])
							else:
								tempstr1 = ""
						else:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  # 1955 BO TRUCK/23@1740 PER WEB
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
							else:
								tempstr1 = ""
					else:
						if check.isdigit() is False:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  # 1955 BO TRUCK/23@1740 PER CALL NIK [Part D]
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])+ " "+str(mbl['speakWith']) + " [Part " + check + "] PC="+str(mbl['slac'])
							else:
								tempstr1 = ""
						else:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  # 1955 BO TRUCK/23@1740 PER CALL NIK
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])+" " +str(mbl['speakWith'])
							else:
								tempstr1 = ""		
								
				else:	
					if mbl['trackSource'] == 'WEB':
						
						if check.isdigit() is False:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  # 1955 BO NH1006/23@1740 PER WEB [Part D]
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource']) + " [Part " + check + "] PC=" +str(mbl['slac'])
							else:
								tempstr1 = ""
						else:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  # 1955 BO NH1006/23@1740 PER WEB
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])
							else:
								tempstr1 = ""
								
					else:
						if check.isdigit() is False:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  # 1955 BO NH1006/23@1740 PER CALL NIK [Part D]
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])+ " "+str(mbl['speakWith']) + " [Part " + check + "] PC="+str(mbl['slac'])
							else:
								tempstr1 = ""
						else:
							if mbl['etaDate'] is not None and mbl['etaTime'] is not None:  # 1955 BO NH1006/23@1740 PER CALL NIK
								tempstr1 = str((mbl['lastUpdatedTime']).strftime("%H%M")) + " " + str(mbl['shipmentStatus']) + " " + str(mbl['flightCode']) + str(mbl['flightNum']) + "/" + str((mbl['etaDate']).strftime("%d")) + "@" + str((mbl['etaTime']).strftime("%H%M")) + " PER " + str(mbl['trackSource'])+" " +str(mbl['speakWith'])
							else:
								tempstr1 = ""					
	
	
		ws11.write(ids + 1, 15, tempstr1)
		ws11.write(ids + 1, 16, mbl['oneFStatus'])
		if mbl['lastUpdatedDate'] is not None: ws11.write(ids + 1, 17, (mbl['lastUpdatedDate']).strftime("%d"))
		if mbl['lastUpdatedTime'] is not None: ws11.write(ids + 1, 18, (mbl['lastUpdatedTime']).strftime("%H%M"))

		ws11.write(ids + 1, 19, mbl['lastUpdatedByUser'])
		ws11.write(ids + 1, 20, mbl['oneFStatusComment'])

	wb.save(response)
	return response


























