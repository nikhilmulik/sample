from django.template import Library
from datetime import datetime
import base64
register = Library()

@register.filter
def splitRemark(value1):
    return value1.split(',')[0]

@register.filter
def emptyString(s):
    return '' if s is None else str(s)

@register.filter
def stripString(s):
    return '' if s is None else s.strip(' ').strip('\n')