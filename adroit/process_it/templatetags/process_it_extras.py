from django.template import Library
from datetime import datetime
import base64
register = Library()

'''	
@register.filter
def truncateAttchmentName(value):
	val_lst = value.split('__')
	return base64.decodestring(base64.encodestring(val_lst[1]))#base64.encodestring().decode('utf8','ignore')#base64.decodestring(
'''


@register.filter
def truncateAttchmentName(value):
	try:
		val_lst = value.split('__')
		return base64.decodestring(base64.encodestring(val_lst[1]))
	except UnicodeEncodeError:
		val_lst = value.split('__')
		val_lst='unknown file name'
#		val_lst.decode('utf-8','ignore')
		val_lst.encode('ascii', 'replace')	
		pass 



@register.filter
def sub(value1,value2):
	return value1 - value2
	
@register.filter
def time(value):
	return datetime.strptime(value,"%Y%m%d%H%M%S").strftime("%I:%M %p")

@register.filter
def date(value):
	return datetime.strptime(value,"%Y%m%d%H%M%S").strftime("%d-%m-%Y")
