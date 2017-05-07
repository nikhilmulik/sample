import pymongo,MySQLdb
from datetime import datetime,timedelta
import imaplib
import smtplib
from email.mime.text import MIMEText
from dateutil import parser
from pytz import timezone

smtp_host = "smtp.gmail.com"
imap_host = 'imap.gmail.com'
password = ""
me = ""
recipients = ['']
# recipients = ['nikhil.mulik@searce.com','siddharth.parekh@searce.com','abhishek.alladi@searce.com','archana.roy@searce.com','abhay.degloorkar@searce.com']


conn = pymongo.Connection("" ,27017)

dbObj = conn.process_it


querydate = datetime.now() - timedelta(hours=24)
querydateStart = querydate.strftime("%Y%m%d") + "010000"
querydatePlus1 = datetime.now()# + timedelta(hours=24)
querydateEnd = querydatePlus1.strftime("%Y%m%d") + "010000"
total_count = dbObj.ds.find({"date":{'$gte':querydateStart,'$lte':querydateEnd}}).count()

print "Total Mails in on",str(querydate.strftime("%Y %b %d"))," :",total_count 

conn1 = MySQLdb.connect(host="",user = "adroit_rw",passwd = "",db="ADROIT")
cursor = conn1.cursor()
cursor.execute ("SELECT count(*) FROM process_it_mawbdetail where preAlertReceivedDate='%s';"%querydate.strftime("%Y-%m-%d"))
row = int(cursor.fetchone()[0])  
print "Total Mails Processed: " ,row
cursor.close()
conn1.close()

payload = """Total Mails recived on %s are %s
Total Mails Processed are %s
"""%(str(querydate.strftime("%Y %b %d")),str(total_count),str(row))

msg = MIMEText(payload)
msg["Subject"] = "Daily Adroit Mails Count Alert"
msg["From"] = me
msg["To"] = ", ".join(recipients)

# s = smtplib.SMTP('smtp.gmail.com', 587 )	#use this on aws server
s = smtplib.SMTP(smtp_host)  #use this on aws server
s.ehlo()
s.starttls()
s.ehlo()
s.login(me, password)
s.sendmail(me, recipients, msg.as_string())
print "Mail Sent"
s.quit()

