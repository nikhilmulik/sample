import imaplib
import smtplib
from email.mime.text import MIMEText
import datetime
from dateutil import parser
from pytz import timezone

smtp_host = "smtp.gmail.com"
imap_host = 'imap.gmail.com'
password = ""
me = ""

def mail(mail_flag, mail_count):
	if mail_flag == True:
		payload = "POP Service of Adroit couldn't process  "+str(len(mail_count[1][0].split()))+"  mails. Please scann them manually."
		msg = MIMEText(payload)

		msg["Subject"] = "Adroit POP Service Missed Mails"
		msg["From"] = me
		msg["To"] = ", ".join(recipients)

		s = smtplib.SMTP('smtp.gmail.com', 587 )	#use this on aws server
		# s = smtplib.SMTP(smtp_host)  #use this on aws server
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login(me, password)
		s.sendmail(me, recipients, msg.as_string())
		s.quit()

recipients = ['']

mail_flag = False
obj = imaplib.IMAP4_SSL(imap_host, '993')
obj.login(me,password)
obj.select()
date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")

total_mails = obj.search(None,'UnSeen')
print "Total Unseen MAils: ",len(total_mails[1][0].split())
yesterdays_unread_mail = obj.search(None, ('UNSEEN'), '(SENTON {0})'.format(date))
print 'yesterdays_unread_mail: ',yesterdays_unread_mail,len(yesterdays_unread_mail[1][0].split())
mail_count = total_mails
try:
	if len(total_mails[1][0].split()) > 0:
		for e_id in total_mails[1][0].split():
			typ , response = obj.fetch(e_id, '(BODY.PEEK[HEADER])')
			raw_mail_date=response[0][1][:response[0][1].find("GMT")-1][-response[0][1][:response[0][1].find("GMT")-1][::-1].find(';'):].strip()
			date1 = parser.parse(raw_mail_date).replace(tzinfo=None)
			raw_date2 = datetime.datetime.utcnow()
			datetime_obj_pacific = (timezone('US/Pacific').localize(raw_date2)).replace(tzinfo=None)
			date2 = datetime_obj_pacific.strftime("%Y-%m-%d %H:%M:%S %Z%z")
			if datetime_obj_pacific-date1 > datetime.timedelta(minutes=15):
				mail_flag = True
				print "MAIL"
except:
	pass
mail(mail_flag, mail_count)


