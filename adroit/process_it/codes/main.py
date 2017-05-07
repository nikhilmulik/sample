# Create your views here.
from django.template import RequestContext
from process_it.models import MawbDetail
from django.shortcuts import render_to_response
from datetime import datetime,timedelta
from django.http import HttpResponse
from django.utils import simplejson as json
from xlwt import Workbook
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import pymongo
from django.utils.simplejson import dumps
import gridfs
from threading import Thread
from django.core.cache import cache
from process_it.lib.encryption import Encryption
from urllib2 import urlopen
from binascii import b2a_hex,a2b_hex
from zlib import compress,decompress
from django.views.generic import TemplateView
import time
from django.db import connection
from datetime import date
import socket
from uuid import getnode as get_mac

# this is commmetn
conn = pymongo.Connection("",27017)
db = conn.process_test
bb_attachments = gridfs.GridFS(db,"bb_attachments")

class AboutView(TemplateView):
	template_name = "process_it/temp.html"








def index(request):
	if 'username' in request.session:
		return render_to_response('process_it/frontPage.html', {'username': request.session['username'],'access_rights':request.session['accessrights']})
	csrfContext = RequestContext(request)
	return render_to_response('process_it/loginPage.html', csrfContext)


def validate(request):

	cursor = connection.cursor()
	TODAY = date.today()
	NOW = datetime.now().strftime("%H:%M:%S")
	ip = request.META['REMOTE_ADDR']
	mac = hex(get_mac())
# 	hostName=request.META['COMPUTERNAME']
	appVersion=request.META['HTTP_USER_AGENT']



	if request.method == 'POST':
		userid = request.POST['username'].strip(' ') #get userid from login page
		password = request.POST['password'].strip(' ') #get password from login page

		if userid <> '' and password <> '':
			objEncode = Encryption()
	
			requestVar = b2a_hex(objEncode.Encode(compress(json.dumps({"action":"signin","user":userid,"password":password,"app":"Adroit","date":str(TODAY) ,"time":str(NOW),"ip":str(ip),"mac":str(mac),"hostname":" ","appVersion":appVersion,"transactionType":"LogIn" })))) #encrypt data
			try :	
				#html = urlopen('http://172.16.15.28/GISS_Dev/remotelogin.php?var='+requestVar)
				html = urlopen('http://giss.live.invoize.com/remotelogin.php?var='+requestVar) #send to the login server
				responseVar = html.read() #read response
				responseVar = json.loads(decompress(objEncode.Encode(a2b_hex(responseVar)))) #decrypt data

				result = responseVar.get("result")
				userid = responseVar.get("userid")
				firstName =  responseVar.get("firstname")
				lastName =  responseVar.get("lastname")
				accessrights = responseVar.get("accessrights")[0]
				email = responseVar.get("email")
				
				request.session['accessrights'] = []
				request.session['class_uname'] = ''
				request.session['class_pass'] = ''
				request.session['screen_width'] = request.POST['screen_width']
				request.session['screen_height'] = request.POST['screen_height']
				request.session['password'] = password
				request.session.set_expiry(0)		#	session closed when browse
									
				if accessrights.has_key('ADROIT_PRE_ALERT_PROCESSING'): #if allowed for module ADROIT_PRE_ALERT_PROCESSING
					request.session['accessrights'].append('ADROIT_PRE_ALERT_PROCESSING')
				if result == '1': #if allowed to login					
					request.session['username'] = firstName+' '+lastName 
					request.session['uid'] = userid

					cursor = connection.cursor()		 
					query="INSERT INTO user_LogIn (userName,DATE,TIME,ip,macAddr,transactionType,hostName,appVersion) VALUES('"+firstName+' '+lastName+"','"+str(TODAY)+"', '"+str(NOW)+"','"+str(ip)+"',' ','Log In',' ','"+appVersion+"' );"
					cursor = connection.cursor()						
					cursor.execute(query)
								
					return render_to_response('process_it/frontPage.html', {'uid':userid,'username': firstName+' '+lastName,'access_rights':request.session['accessrights'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']})
				else : #if not allowed to login 
					initialData = {'error_message': "Username does not exists !",}
			except Exception, e:
				initialData = {'error_message': "Username Password does not matching!",}		
		else:
			initialData = {'error_message': "Please Enter Username and Password!",} #if userid and password is not enterd
		csrfContext = RequestContext(request, initialData)
		return render_to_response('process_it/loginPage.html', csrfContext)
	if 'username' not in request.session:
		csrfContext = RequestContext(request)
		return render_to_response('process_it/loginPage.html', csrfContext)
	else:
		return render_to_response('process_it/frontPage.html', {'username': request.session['username'],'access_rights':request.session['accessrights'],'screen_width':request.session['screen_width'],'screen_height':request.session['screen_height']})



def aiLog(request):
	cursor = connection.cursor()
	firstName = request.session['username']
	if request.method == 'POST':
		mawb = request.POST['mawb'].strip(' ') #get userid from login page

	query = "UPDATE process_it_mawbdetail SET aiDesc='"+firstName+"' WHERE mawbNum IN ('" + mawb.strip("'").replace(",","','") + "');"			
	cursor.execute(query)
	return ("Done")
				

def signOut(request):
	cursor = connection.cursor()
	TODAY = date.today()
	NOW = datetime.now().strftime("%H:%M:%S")
	ip = request.META['REMOTE_ADDR']
# 	mac = hex(get_mac())
	
	try:	
		password = request.session['password']
		if 'username' in request.session:
			username=request.session['username']
			username = username.lower().replace(" ",".")
	# 		username=request.META['USERNAME']
			#hostName=request.META['COMPUTERNAME']
			appVersion=request.META['HTTP_USER_AGENT']
			
			objEncode = Encryption()
			requestVar = b2a_hex(objEncode.Encode(compress(json.dumps({"action":"SignOut","user":username,"password":password,"app":"Adroit","date":str(TODAY) ,"time":str(NOW),"ip":str(ip),"mac":"","appVersion":appVersion,"transactionType":"LogOut" })))) #encrypt data
			html = urlopen(''+requestVar) #send to the login server
			
			responseVar = html.read() #read response
			responseVar = json.loads(decompress(objEncode.Encode(a2b_hex(responseVar)))) #decrypt data
			
			query="INSERT INTO user_LogIn (userName,DATE,TIME,ip,macAddr,transactionType,hostName,appVersion) VALUES('"+username+"','"+str(TODAY)+"', '"+str(NOW)+"','"+str(ip)+"',' ','Log Out',' ','"+appVersion+"' );"
			cursor = connection.cursor()		 
			cursor.execute(query)
				
			del request.session['username']
			
	except:
		del request.session['username']		

	initialData = {'error_message': "Logout successful",}
	csrfContext = RequestContext(request, initialData)
	return render_to_response('process_it/loginPage.html', csrfContext)











