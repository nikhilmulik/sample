# Create your views here.
from django.template import RequestContext
from process_it.models import MawbDetail
from django.shortcuts import render_to_response
from datetime import datetime

def bbPrealertMaster(request):
	
#	print "--->>  ",request.POST.get
	
	if 'username' not in request.session:
		csrfContext = RequestContext(request)
		return render_to_response('process_it/loginPage.html', csrfContext)
	request.session['curr_page'] = 'pp'
	#request.session['pp_settings'] = db.settings.find({"_id":"pp_LAX"})
	#store_settings(request)
	kwargs = {}
	kwargs['pamFlag'] = True
	if request.method == 'POST':
		if request.POST.get('station',''):
			kwargs['station'] = request.POST['station']
		if request.POST.get('preAlertReceivedDateFrom',''):
			kwargs['preAlertReceivedDate__gte'] = datetime.strptime(request.POST['preAlertReceivedDateFrom'], "%m-%d-%y") 
		if request.POST.get('preAlertReceivedDateTo',''):
			kwargs['preAlertReceivedDate__lte'] = datetime.strptime(request.POST['preAlertReceivedDateTo'], "%m-%d-%y") 
		if request.POST.get('lastUpdatedByUser',''):
			kwargs['lastUpdatedByUser'] = request.POST['lastUpdatedByUser']
		if request.POST.get('mawbNum',''):
			kwargs['mawbNum'] = request.POST['mawbNum']
		if request.POST.get('consoleNumber',''):
			kwargs['consoleNumber'] = request.POST['consoleNumber']
		if request.POST.get('customer',''):
			kwargs['customer'] = request.POST['customer']
		if request.POST.get('etdDateFrom',''):
			kwargs['etdDate__gte'] = datetime.strptime(request.POST['etdDateFrom'], "%m-%d-%y")
		if request.POST.get('etdDateTo',''):
			kwargs['etdDate__lte'] = datetime.strptime(request.POST['etdDateTo'], "%m-%d-%y")
		if request.POST.get('etdTimeFrom',''):
			kwargs['etdTime__gte'] = datetime.strptime(request.POST['etdTimeFrom'], "%H:%M")
		if request.POST.get('etdTimeTo',''):
			kwargs['etdTime__lte'] = datetime.strptime(request.POST['etdTimeTo'], "%H:%M")
		if request.POST.get('etaDateFrom',''):
			kwargs['etaDate__gte'] = datetime.strptime(request.POST['etaDateFrom'], "%m-%d-%y")
		if request.POST.get('etaDateTo',''):
			kwargs['etaDate__lte'] = datetime.strptime(request.POST['etaDateTo'], "%m-%d-%y")
		if request.POST.get('etaTimeFrom',''):
			kwargs['etaTime__gte'] = datetime.strptime(request.POST['etaTimeFrom'], "%H:%M")
		if request.POST.get('etaTimeTo',''):
			kwargs['etaTime__lte'] = datetime.strptime(request.POST['etaTimeTo'], "%H:%M")
		if request.POST.get('ataDateFrom',''):
			kwargs['ataDate__gte'] = datetime.strptime(request.POST['ataDateFrom'], "%m-%d-%y")
		if request.POST.get('ataDateTo',''):
			kwargs['ataDate__lte'] = datetime.strptime(request.POST['ataDateTo'], "%m-%d-%y")
		if request.POST.get('ataTimeFrom',''):
			kwargs['ataTime__gte'] = datetime.strptime(request.POST['ataTimeFrom'], "%H:%M")
		if request.POST.get('ataTimeTo',''):
			kwargs['ataTime__lte'] = datetime.strptime(request.POST['ataTimeTo'], "%H:%M")
		if request.POST.get('flightCode',''):
			kwargs['flightCode'] = request.POST['flightCode']
		if request.POST.get('flightNum',''):
			kwargs['flightNum'] = request.POST['flightNum']
		if request.POST.get('slac',''):
			kwargs['slac'] = request.POST['slac']
		if request.POST.get('pmcOrLoose',''):
			kwargs['pmcOrLoose'] = request.POST['pmcOrLoose']
		if request.POST.get('chgWeight',''):
			kwargs['chgWeight'] = request.POST['chgWeight']
		if request.POST.get('remarksInClass',''):
			kwargs['remarksInClass'] = request.POST['remarksInClass']
		if request.POST.get('shipmentStatus',''):
			kwargs['shipmentStatus'] = request.POST['shipmentStatus']
			
		if request.POST.get('trackSource',''):
			kwargs['trackSource'] = request.POST['trackSource']	
			
		if request.POST.get('speakWith',''):
			kwargs['speakWith'] = request.POST['speakWith']	
			
		if request.POST.get('cobDateFrom',''):
			kwargs['cobDate__gte'] = datetime.strptime(request.POST['cobDateFrom'], "%m-%d-%y")
		if request.POST.get('cobDateTo',''):
			kwargs['cobDate__lte'] = datetime.strptime(request.POST['cobDateTo'], "%m-%d-%y")		
		if request.POST.get('recoveryNum',''):
			kwargs['recoveryNum'] = request.POST['recoveryNum']
		if request.POST.get('oneFStatus',''):
			kwargs['oneFStatus'] = request.POST['oneFStatus']
		if request.POST.get('oneFStatusComment',''):
			kwargs['oneFStatusComment'] = request.POST['oneFStatusComment']
	else:
		pass
	request.session['kwargs'] = kwargs
	arr = MawbDetail.objects.filter( **kwargs ).order_by('-etaDate', '-etaTime', 'mawbNum').exclude(station='DFW').exclude(station='DFW/U').exclude(station='IAH')

	'''
	paginator = Paginator(arr, 24)
	page = request.GET.get('page')
	try:
		final_arr = paginator.page(page)
	except PageNotAnInteger:
		final_arr = paginator.page(1)
	except EmptyPage:
		final_arr = paginator.page(paginator.num_pages)
	'''	
	#set1 = sorted(settings.values(), key=lambda item: item['col_order'])
	initialData = {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
	csrfContext = RequestContext(request, initialData)
	return render_to_response('process_it/prealertMasterBlock.html', csrfContext)




'''

	initialData =   {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
	csrfContext = RequestContext(request, initialData)
	request.session['kwargs'] = kwargs 
	return render_to_response('process_it/prealertProcessingBlock.html', csrfContext)

'''




def DFWbbPrealertMaster(request):
	if 'username' not in request.session:
		csrfContext = RequestContext(request)
		return render_to_response('process_it/loginPage.html', csrfContext)
	request.session['curr_page'] = 'pp'
	kwargs = {}
	kwargs['pamFlag'] = True
	if request.method == 'POST':
		if request.POST.get('station',''):
			kwargs['station'] = request.POST['station']
		if request.POST.get('preAlertReceivedDateFrom',''):
			kwargs['preAlertReceivedDate__gte'] = datetime.strptime(request.POST['preAlertReceivedDateFrom'], "%m-%d-%y") 
		if request.POST.get('preAlertReceivedDateTo',''):
			kwargs['preAlertReceivedDate__lte'] = datetime.strptime(request.POST['preAlertReceivedDateTo'], "%m-%d-%y") 
		if request.POST.get('lastUpdatedByUser',''):
			kwargs['lastUpdatedByUser'] = request.POST['lastUpdatedByUser']
		if request.POST.get('mawbNum',''):
			kwargs['mawbNum'] = request.POST['mawbNum']
		if request.POST.get('consoleNumber',''):
			kwargs['consoleNumber'] = request.POST['consoleNumber']
		if request.POST.get('customer',''):
			kwargs['customer'] = request.POST['customer']
		if request.POST.get('etdDateFrom',''):
			kwargs['etdDate__gte'] = datetime.strptime(request.POST['etdDateFrom'], "%m-%d-%y")
		if request.POST.get('etdDateTo',''):
			kwargs['etdDate__lte'] = datetime.strptime(request.POST['etdDateTo'], "%m-%d-%y")
		if request.POST.get('etdTimeFrom',''):
			kwargs['etdTime__gte'] = datetime.strptime(request.POST['etdTimeFrom'], "%H:%M")
		if request.POST.get('etdTimeTo',''):
			kwargs['etdTime__lte'] = datetime.strptime(request.POST['etdTimeTo'], "%H:%M")
		if request.POST.get('etaDateFrom',''):
			kwargs['etaDate__gte'] = datetime.strptime(request.POST['etaDateFrom'], "%m-%d-%y")
		if request.POST.get('etaDateTo',''):
			kwargs['etaDate__lte'] = datetime.strptime(request.POST['etaDateTo'], "%m-%d-%y")
		if request.POST.get('etaTimeFrom',''):
			kwargs['etaTime__gte'] = datetime.strptime(request.POST['etaTimeFrom'], "%H:%M")
		if request.POST.get('etaTimeTo',''):
			kwargs['etaTime__lte'] = datetime.strptime(request.POST['etaTimeTo'], "%H:%M")
		if request.POST.get('ataDateFrom',''):
			kwargs['ataDate__gte'] = datetime.strptime(request.POST['ataDateFrom'], "%m-%d-%y")
		if request.POST.get('ataDateTo',''):
			kwargs['ataDate__lte'] = datetime.strptime(request.POST['ataDateTo'], "%m-%d-%y")
		if request.POST.get('ataTimeFrom',''):
			kwargs['ataTime__gte'] = datetime.strptime(request.POST['ataTimeFrom'], "%H:%M")
		if request.POST.get('ataTimeTo',''):
			kwargs['ataTime__lte'] = datetime.strptime(request.POST['ataTimeTo'], "%H:%M")
		if request.POST.get('flightCode',''):
			kwargs['flightCode'] = request.POST['flightCode']
		if request.POST.get('flightNum',''):
			kwargs['flightNum'] = request.POST['flightNum']
		if request.POST.get('slac',''):
			kwargs['slac'] = request.POST['slac']
		if request.POST.get('pmcOrLoose',''):
			kwargs['pmcOrLoose'] = request.POST['pmcOrLoose']
		if request.POST.get('chgWeight',''):
			kwargs['chgWeight'] = request.POST['chgWeight']
		if request.POST.get('remarksInClass',''):
			kwargs['remarksInClass'] = request.POST['remarksInClass']
		if request.POST.get('shipmentStatus',''):
			kwargs['shipmentStatus'] = request.POST['shipmentStatus']
		if request.POST.get('trackSource',''):
			kwargs['trackSource'] = request.POST['trackSource']	
		if request.POST.get('speakWith',''):
			kwargs['speakWith'] = request.POST['speakWith']	
		if request.POST.get('cobDateFrom',''):
			kwargs['cobDate__gte'] = datetime.strptime(request.POST['cobDateFrom'], "%m-%d-%y")
		if request.POST.get('cobDateTo',''):
			kwargs['cobDate__lte'] = datetime.strptime(request.POST['cobDateTo'], "%m-%d-%y")		
		if request.POST.get('recoveryNum',''):
			kwargs['recoveryNum'] = request.POST['recoveryNum']
		if request.POST.get('oneFStatus',''):
			kwargs['oneFStatus'] = request.POST['oneFStatus']
		if request.POST.get('oneFStatusComment',''):
			kwargs['oneFStatusComment'] = request.POST['oneFStatusComment']
	else:
		pass
	request.session['kwargs'] = kwargs
	arr = MawbDetail.objects.filter( **kwargs ).order_by('-etaDate', '-etaTime', 'mawbNum').exclude(station='LAX').exclude(station='SFO').exclude(station=' ').exclude(station='')

	
	'''
	paginator = Paginator(arr, 24)
	page = request.GET.get('page')
	try:
		final_arr = paginator.page(page)
	except PageNotAnInteger:
		final_arr = paginator.page(1)
	except EmptyPage:
		final_arr = paginator.page(paginator.num_pages)
	'''	
	#set1 = sorted(settings.values(), key=lambda item: item['col_order'])
	initialData = {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
	csrfContext = RequestContext(request, initialData)
	return render_to_response('process_it/DFWprealertMasterBlock.html', csrfContext)




