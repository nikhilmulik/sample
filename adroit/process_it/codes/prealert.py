# Create your views here.
from django.template import RequestContext
from process_it.models import MawbDetail
from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime


def refreshScreen(request):
    if request.method == 'POST':
        MawbDetail.objects.filter(updateTodayFlag=True).update(updateTodayFlag=False)
        return HttpResponse(True)

def bbPrealert(request):			#  	LAX and SFO
    if 'username' not in request.session:
        csrfContext = RequestContext(request)
        return render_to_response('process_it/loginPage.html', csrfContext)
    request.session['curr_page'] = 'pp'
    kwargs = {}
    sort_by = ''
    if request.method == 'POST':
        if request.POST.get('sort_by',''):
            sort_by = request.POST['sort_by']
        if request.POST.get('stationFilter',''):
            if request.POST['stationFilter'] == '...':
                kwargs['station'] = None
            else:
                kwargs['station'] = request.POST['stationFilter']
                
        if request.POST.get('lastUpdatedTimeFromFilter',''):
            if request.POST['lastUpdatedTimeFromFilter'] == '...':
                kwargs['lastUpdatedTime__isnull'] = True
            else:
                kwargs['lastUpdatedTime__gte'] = datetime.strptime(request.POST['lastUpdatedTimeFromFilter'], "%H%M") 
                
        if request.POST.get('lastUpdatedTimeToFilter',''):
            if request.POST['lastUpdatedTimeToFilter'] == '...':
                kwargs['lastUpdatedTime__isnull'] = True
            else:
                kwargs['lastUpdatedTime__lte'] = datetime.strptime(request.POST['lastUpdatedTimeToFilter'], "%H%M")
                
        if request.POST.get('lastUpdatedDateFromFilter',''):
            if request.POST['lastUpdatedDateFromFilter'] == '9999':
                kwargs['lastUpdatedDate__isnull'] = True
            else:
                kwargs['lastUpdatedDate__gte'] = datetime.strptime(request.POST['lastUpdatedDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('lastUpdatedDateToFilter',''):
            if request.POST['lastUpdatedDateToFilter'] == '9999':
                kwargs['lastUpdatedDate__isnull'] = True
            else:
                kwargs['lastUpdatedDate__lte'] = datetime.strptime(request.POST['lastUpdatedDateToFilter'], "%m-%d-%y")
              
        if request.POST.get('lastUpdatedByUserFilter',''):
            if request.POST['lastUpdatedByUserFilter'] == '...':
                kwargs['lastUpdatedByUser'] = None
            else:
                kwargs['lastUpdatedByUser__contains'] = request.POST['lastUpdatedByUserFilter']
            
        if request.POST.get('mawbNumFilter',''):
            if request.POST['mawbNumFilter'] == '...':
                kwargs['mawbNum'] = None
            else:
                kwargs['mawbNum__contains'] = request.POST['mawbNumFilter']
            
        if request.POST.get('itInfoFilter',''):
            if request.POST['itInfoFilter'] == '...':
                kwargs['itInfo'] = None
            else:
                kwargs['itInfo__contains'] = request.POST['itInfoFilter']
            
        if request.POST.get('consoleNumberFilter',''):
            if request.POST['consoleNumberFilter'] == '...':
                kwargs['consoleNumber__isnull'] = True
            else:
                kwargs['consoleNumber'] = request.POST['consoleNumberFilter']
            
        if request.POST.get('customerFilter',''):
            if request.POST['customerFilter'] == '...':
                kwargs['customer'] = None
            else:
                kwargs['customer__contains'] = request.POST['customerFilter']
            
        if request.POST.get('etdDateFromFilter',''):
            if request.POST['etdDateFromFilter'] == '...':
                kwargs['etdDate__isnull'] = True
            else:
                kwargs['etdDate__gte'] = datetime.strptime(request.POST['etdDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('etdDateToFilter',''):
            if request.POST['etdDateToFilter'] == '...':
                kwargs['etdDate__isnull'] = True
            else:
                kwargs['etdDate__lte'] = datetime.strptime(request.POST['etdDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('etdTimeFromFilter',''):
            if request.POST['etdTimeFromFilter'] == '...':
                kwargs['etdTime__isnull'] = True
            else:
                kwargs['etdTime__gte'] = datetime.strptime(request.POST['etdTimeFromFilter'], "%H%M")
            
        if request.POST.get('etdTimeToFilter',''):
            if request.POST['etdTimeToFilter'] == '...':
                kwargs['etdTime__isnull'] = True
            else:
                kwargs['etdTime__lte'] = datetime.strptime(request.POST['etdTimeToFilter'], "%H%M")
            
        if request.POST.get('etaDateFromFilter',''):
            if request.POST['etaDateFromFilter'] == '9999':
                kwargs['etaDate__isnull'] = True
            else:
                kwargs['etaDate__gte'] = datetime.strptime(request.POST['etaDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('etaDateToFilter',''):
            if request.POST['etaDateToFilter'] == '9999':
                kwargs['etaDate__isnull'] = True
            else:
                kwargs['etaDate__lte'] = datetime.strptime(request.POST['etaDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('etaTimeFromFilter',''):
            if request.POST['etaTimeFromFilter'] == '...':
                kwargs['etaTime__isnull'] = True
            else:
                kwargs['etaTime__gte'] = datetime.strptime(request.POST['etaTimeFromFilter'], "%H%M")
            
        if request.POST.get('etaTimeToFilter',''):
            if request.POST['etaTimeToFilter'] == '...':
                kwargs['etaTime__isnull'] = True
            else:
                kwargs['etaTime__lte'] = datetime.strptime(request.POST['etaTimeToFilter'], "%H%M")
            
        if request.POST.get('ataDateFromFilter',''):
            if request.POST['ataDateFromFilter'] == '...':
                kwargs['ataDate__isnull'] = True
            else:
                kwargs['ataDate__gte'] = datetime.strptime(request.POST['ataDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('ataDateToFilter',''):
            if request.POST['ataDateToFilter'] == '...':
                kwargs['ataDate__isnull'] = True
            else:
                kwargs['ataDate__lte'] = datetime.strptime(request.POST['ataDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('ataTimeFromFilter',''):
            if request.POST['ataTimeFromFilter'] == '...':
                kwargs['ataTime__isnull'] = True
            else:
                kwargs['ataTime__gte'] = datetime.strptime(request.POST['ataTimeFromFilter'], "%H%M")
            
        if request.POST.get('ataTimeToFilter',''):
            if request.POST['ataTimeToFilter'] == '...':
                kwargs['ataTime__isnull'] = True
            else:
                kwargs['ataTime__lte'] = datetime.strptime(request.POST['ataTimeToFilter'], "%H%M")
            
        if request.POST.get('flightCodeFilter',''):
            if request.POST['flightCodeFilter'] == '...':
                kwargs['flightCode'] = None
            else:
                kwargs['flightCode__contains'] = request.POST['flightCodeFilter']
            
        if request.POST.get('flightNumFilter',''):
            if request.POST['flightNumFilter'] == '...':
                kwargs['flightNum'] = None
            else:
                kwargs['flightNum'] = request.POST['flightNumFilter']
            
        if request.POST.get('slacFilter',''):
            if request.POST['slacFilter'] == '...':
                kwargs['slac__isnull'] = True
            else:
                kwargs['slac'] = request.POST['slacFilter']
                    
        if request.POST.get('pmcOrLooseFilter',''):
            if request.POST['pmcOrLooseFilter'] == '...':
                kwargs['pmcOrLoose'] = None
            else:
                kwargs['pmcOrLoose'] = request.POST['pmcOrLooseFilter']
            
        if request.POST.get('chgWeightFilter',''):
            if request.POST['chgWeightFilter'] == '...':
                kwargs['chgWeight__isnull'] = True
            else:
                kwargs['chgWeight'] = request.POST['chgWeightFilter']
            
        if request.POST.get('remarksInClassFilter',''):
            if request.POST['remarksInClassFilter'] == '...':
                kwargs['remarksInClass'] = None
            else: 
                kwargs['remarksInClass__contains'] = request.POST['remarksInClassFilter']
            
        if request.POST.get('shipmentStatusFilter',''):
            if request.POST['shipmentStatusFilter'] == '...':
                kwargs['shipmentStatus'] = None
            else:
                kwargs['shipmentStatus'] = request.POST['shipmentStatusFilter']
            
        if request.POST.get('trackSourceFilter',''):
            if request.POST['trackSourceFilter'] == '...':
                kwargs['trackSource'] = None
            else:
                kwargs['trackSource'] = request.POST['trackSourceFilter']
            
        if request.POST.get('speakWithFilter',''):
            if request.POST['speakWithFilter'] == '...':
                kwargs['speakWith'] = None
            else:
                kwargs['speakWith'] = request.POST['speakWithFilter']
            
        if request.POST.get('cobDateFromFilter',''):
            if request.POST['cobDateFromFilter'] == '...':
                kwargs['cobDate__isnull'] = True
            else:
                kwargs['cobDate__gte'] = datetime.strptime(request.POST['cobDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('cobDateToFilter',''):
            if request.POST['cobDateToFilter'] == '...':
                kwargs['cobDate__isnull'] = True
            else:
                kwargs['cobDate__lte'] = datetime.strptime(request.POST['cobDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('recoveryNumFilter',''):
            if request.POST['recoveryNumFilter'] == '...':
                kwargs['recoveryNum'] = None
            else:
                kwargs['recoveryNum'] = request.POST['recoveryNumFilter']
            
        if request.POST.get('oneFStatusFilter',''):
            if request.POST['oneFStatusFilter'] == '...':
                kwargs['oneFStatus'] = None
            else:
                kwargs['oneFStatus'] = request.POST['oneFStatusFilter']
            
        if request.POST.get('oneFStatusCommentFilter',''):
            if request.POST['oneFStatusCommentFilter'] == '...':
                kwargs['oneFStatusComment'] = None
            else: 
                kwargs['oneFStatusComment__contains'] = request.POST['oneFStatusCommentFilter']
                
        if request.POST.get('fnbStatusFilter',''):
            if request.POST['fnbStatusFilter'] == '...':
                kwargs['spProStatus'] = None
            else: 
                kwargs['spProStatus'] = request.POST['fnbStatusFilter']	                 

        if sort_by:
            arr = MawbDetail.objects.filter( **kwargs ).order_by(sort_by).exclude(papFlag=False).exclude(station='DFW/U').exclude(station='DFW').exclude(station='IAH').exclude(station='TUL').exclude(station='AUS').exclude(station='MSY').exclude(station='SAT').exclude(station='OKC')
            
        else:
            arr = MawbDetail.objects.filter( **kwargs ).order_by('-etaDate', '-etaTime',).exclude(papFlag=False).exclude(station='DFW/U').exclude(station='IAH').exclude(station='DFW').exclude(station='TUL').exclude(station='AUS').exclude(station='MSY').exclude(station='SAT').exclude(station='OKC')
            
        #set1 = sorted(settings.values(), key=lambda item: item['col_order'])
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
        initialData = {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'sort_by' : sort_by, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
        csrfContext = RequestContext(request, initialData)
        request.session['kwargs'] = kwargs
        return render_to_response('process_it/prealertProcessingBlock.html', csrfContext)
    else:
        arr = MawbDetail.objects.all().order_by('-etaDate', '-etaTime',).exclude(papFlag=False).exclude(station='DFW').exclude(station='DFW/U').exclude(station='IAH').exclude(station='TUL').exclude(station='AUS').exclude(station='MSY').exclude(station='SAT').exclude(station='OKC')
        
        
        #set1 = sorted(settings.values(), key=lambda item: item['col_order'])
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
        initialData =   {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'sort_by' : sort_by, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
        csrfContext = RequestContext(request, initialData)
        request.session['kwargs'] = kwargs 
        return render_to_response('process_it/prealertProcessingBlock.html', csrfContext)
    
def showAll(request):
    arr = MawbDetail.objects.all()
    initialData =   {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
    csrfContext = RequestContext(request, initialData)
    return render_to_response('process_it/showAllMaster.html', csrfContext)

def temp0189(request):
    if 'username' not in request.session:
        csrfContext = RequestContext(request)
        return render_to_response('process_it/loginPage.html', csrfContext)
    request.session['curr_page'] = 'pp'
    kwargs = {}
    sort_by = ''
    if request.method == 'POST':
        if request.POST.get('sort_by',''):
            sort_by = request.POST['sort_by']
        if request.POST.get('stationFilter',''):
            if request.POST['stationFilter'] == '...':
                kwargs['station'] = None
            else:
                kwargs['station'] = request.POST['stationFilter']
                
        if request.POST.get('lastUpdatedTimeFromFilter',''):
            if request.POST['lastUpdatedTimeFromFilter'] == '...':
                kwargs['lastUpdatedTime__isnull'] = True
            else:
                kwargs['lastUpdatedTime__gte'] = datetime.strptime(request.POST['lastUpdatedTimeFromFilter'], "%H%M") 
                
        if request.POST.get('lastUpdatedTimeToFilter',''):
            if request.POST['lastUpdatedTimeToFilter'] == '...':
                kwargs['lastUpdatedTime__isnull'] = True
            else:
                kwargs['lastUpdatedTime__lte'] = datetime.strptime(request.POST['lastUpdatedTimeToFilter'], "%H%M")
                
        if request.POST.get('lastUpdatedDateFromFilter',''):
            if request.POST['lastUpdatedDateFromFilter'] == '9999':
                kwargs['lastUpdatedDate__isnull'] = True
            else:
                kwargs['lastUpdatedDate__gte'] = datetime.strptime(request.POST['lastUpdatedDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('lastUpdatedDateToFilter',''):
            if request.POST['lastUpdatedDateToFilter'] == '9999':
                kwargs['lastUpdatedDate__isnull'] = True
            else:
                kwargs['lastUpdatedDate__lte'] = datetime.strptime(request.POST['lastUpdatedDateToFilter'], "%m-%d-%y")
              
        if request.POST.get('lastUpdatedByUserFilter',''):
            if request.POST['lastUpdatedByUserFilter'] == '...':
                kwargs['lastUpdatedByUser'] = None
            else:
                kwargs['lastUpdatedByUser__contains'] = request.POST['lastUpdatedByUserFilter']
            
        if request.POST.get('mawbNumFilter',''):
            if request.POST['mawbNumFilter'] == '...':
                kwargs['mawbNum'] = None
            else:
                kwargs['mawbNum__contains'] = request.POST['mawbNumFilter']
            
        if request.POST.get('itInfoFilter',''):
            if request.POST['itInfoFilter'] == '...':
                kwargs['itInfo'] = None
            else:
                kwargs['itInfo__contains'] = request.POST['itInfoFilter']
            
        if request.POST.get('consoleNumberFilter',''):
            if request.POST['consoleNumberFilter'] == '...':
                kwargs['consoleNumber__isnull'] = True
            else:
                kwargs['consoleNumber'] = request.POST['consoleNumberFilter']
            
        if request.POST.get('customerFilter',''):
            if request.POST['customerFilter'] == '...':
                kwargs['customer'] = None
            else:
                kwargs['customer__contains'] = request.POST['customerFilter']
            
        if request.POST.get('etdDateFromFilter',''):
            if request.POST['etdDateFromFilter'] == '...':
                kwargs['etdDate__isnull'] = True
            else:
                kwargs['etdDate__gte'] = datetime.strptime(request.POST['etdDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('etdDateToFilter',''):
            if request.POST['etdDateToFilter'] == '...':
                kwargs['etdDate__isnull'] = True
            else:
                kwargs['etdDate__lte'] = datetime.strptime(request.POST['etdDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('etdTimeFromFilter',''):
            if request.POST['etdTimeFromFilter'] == '...':
                kwargs['etdTime__isnull'] = True
            else:
                kwargs['etdTime__gte'] = datetime.strptime(request.POST['etdTimeFromFilter'], "%H%M")
            
        if request.POST.get('etdTimeToFilter',''):
            if request.POST['etdTimeToFilter'] == '...':
                kwargs['etdTime__isnull'] = True
            else:
                kwargs['etdTime__lte'] = datetime.strptime(request.POST['etdTimeToFilter'], "%H%M")
            
        if request.POST.get('etaDateFromFilter',''):
            if request.POST['etaDateFromFilter'] == '9999':
                kwargs['etaDate__isnull'] = True
            else:
                kwargs['etaDate__gte'] = datetime.strptime(request.POST['etaDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('etaDateToFilter',''):
            if request.POST['etaDateToFilter'] == '9999':
                kwargs['etaDate__isnull'] = True
            else:
                kwargs['etaDate__lte'] = datetime.strptime(request.POST['etaDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('etaTimeFromFilter',''):
            if request.POST['etaTimeFromFilter'] == '...':
                kwargs['etaTime__isnull'] = True
            else:
                kwargs['etaTime__gte'] = datetime.strptime(request.POST['etaTimeFromFilter'], "%H%M")
            
        if request.POST.get('etaTimeToFilter',''):
            if request.POST['etaTimeToFilter'] == '...':
                kwargs['etaTime__isnull'] = True
            else:
                kwargs['etaTime__lte'] = datetime.strptime(request.POST['etaTimeToFilter'], "%H%M")
            
        if request.POST.get('ataDateFromFilter',''):
            if request.POST['ataDateFromFilter'] == '...':
                kwargs['ataDate__isnull'] = True
            else:
                kwargs['ataDate__gte'] = datetime.strptime(request.POST['ataDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('ataDateToFilter',''):
            if request.POST['ataDateToFilter'] == '...':
                kwargs['ataDate__isnull'] = True
            else:
                kwargs['ataDate__lte'] = datetime.strptime(request.POST['ataDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('ataTimeFromFilter',''):
            if request.POST['ataTimeFromFilter'] == '...':
                kwargs['ataTime__isnull'] = True
            else:
                kwargs['ataTime__gte'] = datetime.strptime(request.POST['ataTimeFromFilter'], "%H%M")
            
        if request.POST.get('ataTimeToFilter',''):
            if request.POST['ataTimeToFilter'] == '...':
                kwargs['ataTime__isnull'] = True
            else:
                kwargs['ataTime__lte'] = datetime.strptime(request.POST['ataTimeToFilter'], "%H%M")
            
        if request.POST.get('flightCodeFilter',''):
            if request.POST['flightCodeFilter'] == '...':
                kwargs['flightCode'] = None
            else:
                kwargs['flightCode__contains'] = request.POST['flightCodeFilter']
            
        if request.POST.get('flightNumFilter',''):
            if request.POST['flightNumFilter'] == '...':
                kwargs['flightNum'] = None
            else:
                kwargs['flightNum'] = request.POST['flightNumFilter']
            
        if request.POST.get('slacFilter',''):
            if request.POST['slacFilter'] == '...':
                kwargs['slac__isnull'] = True
            else:
                kwargs['slac'] = request.POST['slacFilter']
                    
        if request.POST.get('pmcOrLooseFilter',''):
            if request.POST['pmcOrLooseFilter'] == '...':
                kwargs['pmcOrLoose'] = None
            else:
                kwargs['pmcOrLoose'] = request.POST['pmcOrLooseFilter']
            
        if request.POST.get('chgWeightFilter',''):
            if request.POST['chgWeightFilter'] == '...':
                kwargs['chgWeight__isnull'] = True
            else:
                kwargs['chgWeight'] = request.POST['chgWeightFilter']
            
        if request.POST.get('remarksInClassFilter',''):
            if request.POST['remarksInClassFilter'] == '...':
                kwargs['remarksInClass'] = None
            else: 
                kwargs['remarksInClass__contains'] = request.POST['remarksInClassFilter']
            
        if request.POST.get('shipmentStatusFilter',''):
            if request.POST['shipmentStatusFilter'] == '...':
                kwargs['shipmentStatus'] = None
            else:
                kwargs['shipmentStatus'] = request.POST['shipmentStatusFilter']
            
        if request.POST.get('trackSourceFilter',''):
            if request.POST['trackSourceFilter'] == '...':
                kwargs['trackSource'] = None
            else:
                kwargs['trackSource'] = request.POST['trackSourceFilter']
            
        if request.POST.get('speakWithFilter',''):
            if request.POST['speakWithFilter'] == '...':
                kwargs['speakWith'] = None
            else:
                kwargs['speakWith'] = request.POST['speakWithFilter']
            
        if request.POST.get('cobDateFromFilter',''):
            if request.POST['cobDateFromFilter'] == '...':
                kwargs['cobDate__isnull'] = True
            else:
                kwargs['cobDate__gte'] = datetime.strptime(request.POST['cobDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('cobDateToFilter',''):
            if request.POST['cobDateToFilter'] == '...':
                kwargs['cobDate__isnull'] = True
            else:
                kwargs['cobDate__lte'] = datetime.strptime(request.POST['cobDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('recoveryNumFilter',''):
            if request.POST['recoveryNumFilter'] == '...':
                kwargs['recoveryNum'] = None
            else:
                kwargs['recoveryNum'] = request.POST['recoveryNumFilter']
            
        if request.POST.get('oneFStatusFilter',''):
            if request.POST['oneFStatusFilter'] == '...':
                kwargs['oneFStatus'] = None
            else:
                kwargs['oneFStatus'] = request.POST['oneFStatusFilter']
            
        if request.POST.get('oneFStatusCommentFilter',''):
            if request.POST['oneFStatusCommentFilter'] == '...':
                kwargs['oneFStatusComment'] = None
            else: 
                kwargs['oneFStatusComment__contains'] = request.POST['oneFStatusCommentFilter']
        if sort_by:
            arr = MawbDetail.objects.filter( **kwargs ).order_by(sort_by).exclude(papFlag=False)
            
        else:
            arr = MawbDetail.objects.filter( **kwargs ).order_by('-etaDate', '-etaTime',).exclude(papFlag=False)
            
        #set1 = sorted(settings.values(), key=lambda item: item['col_order'])
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
        initialData = {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'sort_by' : sort_by, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
        csrfContext = RequestContext(request, initialData)
        request.session['kwargs'] = kwargs
        return render_to_response('process_it/temp.html', csrfContext)
    else:
        arr = MawbDetail.objects.all().order_by('-etaDate', '-etaTime',).exclude(papFlag=False)
        
        
        #set1 = sorted(settings.values(), key=lambda item: item['col_order'])
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
        initialData =   {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'sort_by' : sort_by, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
        csrfContext = RequestContext(request, initialData)
        request.session['kwargs'] = kwargs 
        return render_to_response('process_it/temp.html', csrfContext)












def DFWbbPrealert(request):			#  	DFW
    if 'username' not in request.session:
        csrfContext = RequestContext(request)
        return render_to_response('process_it/loginPage.html', csrfContext)
    request.session['curr_page'] = 'pp'
    kwargs = {}
    sort_by = ''
    if request.method == 'POST':
        if request.POST.get('sort_by',''):
            sort_by = request.POST['sort_by']
            
        if request.POST.get('stationFilter',''):        
            if request.POST['stationFilter'] == '...':
                kwargs['station'] = None
#            elif request.POST['stationFilter'] == 'LAX':
#                msg="Cannot Access LAX from DFW."
#                return render_to_response('process_it/DFWprealertProcessingBlock.html', locals())
            else:
                kwargs['station'] = request.POST['stationFilter']

#		if request.POST.get('stationFilter',''):
#			if request.POST['stationFilter'] == '...':
#				kwargs['station'] = None
#			else:
#				if request.POST['stationFilter'] in request.session['ADROIT_STATION_ACCESS']:
#				 	kwargs['station'] = request.POST['stationFilter']
#				else
#					return "Not allaowed to this station"
      
                
        if request.POST.get('lastUpdatedTimeFromFilter',''):
            if request.POST['lastUpdatedTimeFromFilter'] == '...':
                kwargs['lastUpdatedTime__isnull'] = True
            else:
                kwargs['lastUpdatedTime__gte'] = datetime.strptime(request.POST['lastUpdatedTimeFromFilter'], "%H%M") 
                
        if request.POST.get('lastUpdatedTimeToFilter',''):
            if request.POST['lastUpdatedTimeToFilter'] == '...':
                kwargs['lastUpdatedTime__isnull'] = True
            else:
                kwargs['lastUpdatedTime__lte'] = datetime.strptime(request.POST['lastUpdatedTimeToFilter'], "%H%M")
                
        if request.POST.get('lastUpdatedDateFromFilter',''):
            if request.POST['lastUpdatedDateFromFilter'] == '9999':
                kwargs['lastUpdatedDate__isnull'] = True
            else:
                kwargs['lastUpdatedDate__gte'] = datetime.strptime(request.POST['lastUpdatedDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('lastUpdatedDateToFilter',''):
            if request.POST['lastUpdatedDateToFilter'] == '9999':
                kwargs['lastUpdatedDate__isnull'] = True
            else:
                kwargs['lastUpdatedDate__lte'] = datetime.strptime(request.POST['lastUpdatedDateToFilter'], "%m-%d-%y")
              
        if request.POST.get('lastUpdatedByUserFilter',''):
            if request.POST['lastUpdatedByUserFilter'] == '...':
                kwargs['lastUpdatedByUser'] = None
            else:
                kwargs['lastUpdatedByUser__contains'] = request.POST['lastUpdatedByUserFilter']
            
        if request.POST.get('mawbNumFilter',''):
            if request.POST['mawbNumFilter'] == '...':
                kwargs['mawbNum'] = None
            else:
                kwargs['mawbNum__contains'] = request.POST['mawbNumFilter']
            
        if request.POST.get('itInfoFilter',''):
            if request.POST['itInfoFilter'] == '...':
                kwargs['itInfo'] = None
            else:
                kwargs['itInfo__contains'] = request.POST['itInfoFilter']
            
        if request.POST.get('consoleNumberFilter',''):
            if request.POST['consoleNumberFilter'] == '...':
                kwargs['consoleNumber__isnull'] = True
            else:
                kwargs['consoleNumber'] = request.POST['consoleNumberFilter']
            
        if request.POST.get('customerFilter',''):
            if request.POST['customerFilter'] == '...':
                kwargs['customer'] = None
            else:
                kwargs['customer__contains'] = request.POST['customerFilter']
            
        if request.POST.get('etdDateFromFilter',''):
            if request.POST['etdDateFromFilter'] == '...':
                kwargs['etdDate__isnull'] = True
            else:
                kwargs['etdDate__gte'] = datetime.strptime(request.POST['etdDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('etdDateToFilter',''):
            if request.POST['etdDateToFilter'] == '...':
                kwargs['etdDate__isnull'] = True
            else:
                kwargs['etdDate__lte'] = datetime.strptime(request.POST['etdDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('etdTimeFromFilter',''):
            if request.POST['etdTimeFromFilter'] == '...':
                kwargs['etdTime__isnull'] = True
            else:
                kwargs['etdTime__gte'] = datetime.strptime(request.POST['etdTimeFromFilter'], "%H%M")
            
        if request.POST.get('etdTimeToFilter',''):
            if request.POST['etdTimeToFilter'] == '...':
                kwargs['etdTime__isnull'] = True
            else:
                kwargs['etdTime__lte'] = datetime.strptime(request.POST['etdTimeToFilter'], "%H%M")
            
        if request.POST.get('etaDateFromFilter',''):
            if request.POST['etaDateFromFilter'] == '9999':
                kwargs['etaDate__isnull'] = True
            else:
                kwargs['etaDate__gte'] = datetime.strptime(request.POST['etaDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('etaDateToFilter',''):
            if request.POST['etaDateToFilter'] == '9999':
                kwargs['etaDate__isnull'] = True
            else:
                kwargs['etaDate__lte'] = datetime.strptime(request.POST['etaDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('etaTimeFromFilter',''):
            if request.POST['etaTimeFromFilter'] == '...':
                kwargs['etaTime__isnull'] = True
            else:
                kwargs['etaTime__gte'] = datetime.strptime(request.POST['etaTimeFromFilter'], "%H%M")
            
        if request.POST.get('etaTimeToFilter',''):
            if request.POST['etaTimeToFilter'] == '...':
                kwargs['etaTime__isnull'] = True
            else:
                kwargs['etaTime__lte'] = datetime.strptime(request.POST['etaTimeToFilter'], "%H%M")
            
        if request.POST.get('ataDateFromFilter',''):
            if request.POST['ataDateFromFilter'] == '...':
                kwargs['ataDate__isnull'] = True
            else:
                kwargs['ataDate__gte'] = datetime.strptime(request.POST['ataDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('ataDateToFilter',''):
            if request.POST['ataDateToFilter'] == '...':
                kwargs['ataDate__isnull'] = True
            else:
                kwargs['ataDate__lte'] = datetime.strptime(request.POST['ataDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('ataTimeFromFilter',''):
            if request.POST['ataTimeFromFilter'] == '...':
                kwargs['ataTime__isnull'] = True
            else:
                kwargs['ataTime__gte'] = datetime.strptime(request.POST['ataTimeFromFilter'], "%H%M")
            
        if request.POST.get('ataTimeToFilter',''):
            if request.POST['ataTimeToFilter'] == '...':
                kwargs['ataTime__isnull'] = True
            else:
                kwargs['ataTime__lte'] = datetime.strptime(request.POST['ataTimeToFilter'], "%H%M")
            
        if request.POST.get('flightCodeFilter',''):
            if request.POST['flightCodeFilter'] == '...':
                kwargs['flightCode'] = None
            else:
                kwargs['flightCode__contains'] = request.POST['flightCodeFilter']
            
        if request.POST.get('flightNumFilter',''):
            if request.POST['flightNumFilter'] == '...':
                kwargs['flightNum'] = None
            else:
                kwargs['flightNum'] = request.POST['flightNumFilter']
            
        if request.POST.get('slacFilter',''):
            if request.POST['slacFilter'] == '...':
                kwargs['slac__isnull'] = True
            else:
                kwargs['slac'] = request.POST['slacFilter']
                    
        if request.POST.get('pmcOrLooseFilter',''):
            if request.POST['pmcOrLooseFilter'] == '...':
                kwargs['pmcOrLoose'] = None
            else:
                kwargs['pmcOrLoose'] = request.POST['pmcOrLooseFilter']
            
        if request.POST.get('chgWeightFilter',''):
            if request.POST['chgWeightFilter'] == '...':
                kwargs['chgWeight__isnull'] = True
            else:
                kwargs['chgWeight'] = request.POST['chgWeightFilter']
            
        if request.POST.get('remarksInClassFilter',''):
            if request.POST['remarksInClassFilter'] == '...':
                kwargs['remarksInClass'] = None
            else: 
                kwargs['remarksInClass__contains'] = request.POST['remarksInClassFilter']
            
        if request.POST.get('shipmentStatusFilter',''):
            if request.POST['shipmentStatusFilter'] == '...':
                kwargs['shipmentStatus'] = None
            else:
                kwargs['shipmentStatus'] = request.POST['shipmentStatusFilter']
            
        if request.POST.get('trackSourceFilter',''):
            if request.POST['trackSourceFilter'] == '...':
                kwargs['trackSource'] = None
            else:
                kwargs['trackSource'] = request.POST['trackSourceFilter']
            
        if request.POST.get('speakWithFilter',''):
            if request.POST['speakWithFilter'] == '...':
                kwargs['speakWith'] = None
            else:
                kwargs['speakWith'] = request.POST['speakWithFilter']
            
        if request.POST.get('cobDateFromFilter',''):
            if request.POST['cobDateFromFilter'] == '...':
                kwargs['cobDate__isnull'] = True
            else:
                kwargs['cobDate__gte'] = datetime.strptime(request.POST['cobDateFromFilter'], "%m-%d-%y")
            
        if request.POST.get('cobDateToFilter',''):
            if request.POST['cobDateToFilter'] == '...':
                kwargs['cobDate__isnull'] = True
            else:
                kwargs['cobDate__lte'] = datetime.strptime(request.POST['cobDateToFilter'], "%m-%d-%y")
            
        if request.POST.get('recoveryNumFilter',''):
            if request.POST['recoveryNumFilter'] == '...':
                kwargs['recoveryNum'] = None
            else:
                kwargs['recoveryNum'] = request.POST['recoveryNumFilter']
            
        if request.POST.get('oneFStatusFilter',''):
            if request.POST['oneFStatusFilter'] == '...':
                kwargs['oneFStatus'] = None
            else:
                kwargs['oneFStatus'] = request.POST['oneFStatusFilter']
            
        if request.POST.get('oneFStatusCommentFilter',''):
            if request.POST['oneFStatusCommentFilter'] == '...':
                kwargs['oneFStatusComment'] = None
            else: 
                kwargs['oneFStatusComment__contains'] = request.POST['oneFStatusCommentFilter']
                
        if request.POST.get('fnbStatusFilter',''):
            if request.POST['fnbStatusFilter'] == '...':
                kwargs['spProStatus'] = None
            else: 
                kwargs['spProStatus'] = request.POST['fnbStatusFilter']     
          
        if sort_by:
            arr = MawbDetail.objects.filter( **kwargs ).order_by(sort_by).exclude(papFlag=False).exclude(station='LAX').exclude(station='SFO')
            
        else:
#            arr = MawbDetail.objects.filter( **kwargs ).order_by('-etaDate', '-etaTime',).exclude(papFlag=False)
            arr = MawbDetail.objects.filter( **kwargs ).order_by('-etaDate', '-etaTime',).exclude(papFlag=False).exclude(station='LAX').exclude(station='SFO')
            

        initialData = {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'sort_by' : sort_by, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
        csrfContext = RequestContext(request, initialData)
        request.session['kwargs'] = kwargs
        return render_to_response('process_it/DFWprealertProcessingBlock.html', csrfContext)
    else:
#        arr = MawbDetail.objects.all().order_by('-etaDate', '-etaTime',).exclude(papFlag=False)
        arr = MawbDetail.objects.all().order_by('-etaDate', '-etaTime',).exclude(papFlag=False).exclude(station='LAX').exclude(station='SFO').exclude(station=' ').exclude(station='')

        initialData =   {'uid':request.session['uid'],'arr' : arr, 'username' : request.session['username'],'access_rights':request.session['accessrights'], 'kwargs' : kwargs, 'sort_by' : sort_by, 'class_uname' : request.session['class_uname'], 'class_pass' : request.session['class_pass'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']}
        csrfContext = RequestContext(request, initialData)
        request.session['kwargs'] = kwargs 
        return render_to_response('process_it/DFWprealertProcessingBlock.html', csrfContext)




















