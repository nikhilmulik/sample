#!/usr/bin/env python
import time, os, re, sys, poplib, email, string, pymongo, base64, gridfs, MySQLdb
from datetime import datetime,timedelta
from email.Header import decode_header
from email.utils import parseaddr,parsedate
from StringIO import StringIO
import codecs

#import gridfs

class Pre_Alert_Parser():
    def __init__(self, mongo_host="localhost", mongo_port=27017, root_path="/apps/webapps/utilites/prealerts_parsing"):
        print "Parsing start......"
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.root_path = root_path        
        self.dbObj2 = self.getMongoConn()
        self.dbObj1 = self.getMongoConn1()
        self.bb_attachments = gridfs.GridFS(self.dbObj2,"bb_attachments")
        self.bb_attachments1 = gridfs.GridFS(self.dbObj1,"bb_attachments")
        self.LogFile = "/logs/pre_alert_parsing_"+datetime.now().strftime("%d%m%y")+".log"
    
    def getMongoConn(self):
        """
        This function returns the connection object of mongodb.
        """
        conn = pymongo.Connection(self.mongo_host,self.mongo_port)
        dbObj = conn.process_it
        print "Added into Database : "+dbObj.name
        return dbObj
    
    def getMongoConn1(self):
        """
        This function returns the connection object of mongodb.
        """
        conn = pymongo.Connection(self.mongo_host,self.mongo_port)
        dbObj = conn.process_test
        print "Added into Database : "+dbObj.name
        return dbObj
    
    def writeLog(self, logdata, scriptfilename="pre_alert_parsing.py", DEBUG=0):
        if DEBUG == 1:
            pass
        else:            
            print "There is an error please contact to system admin."
#        logFile = open(self.root_path+self.LogFile, 'a')
#        logFile.write(datetime.now().strftime("%Y%m%d %H%M%S")+'::'+scriptfilename+':'+logdata+'\r\n')
#        logFile.close();
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        logFile = open(self.root_path+self.LogFile, 'a')
        logdata.decode('utf-8','ignore')
        logFile.write(datetime.now().strftime("%Y%m%d %H%M%S")+'::'+scriptfilename+':'+logdata+'\r\n')
        logFile.close();

    def writeDBLog(self, logdata):
        LFile = "/DBlogs/pre_alert_DB_"+datetime.now().strftime("%d%m%y")+".log"
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        logFile = open(self.root_path+LFile, 'a')
        logdata.decode('utf-8','ignore')
        logFile.write(datetime.now().strftime("%Y%m%d %H%M%S")+'::'+logdata+'\r\n')
        logFile.close();

#        try:
#            logFile = open(self.root_path+self.LogFile, 'a')
#            logdata = logdata.decode('utf-8') # 
#            logFile.write(datetime.now().strftime("%Y%m%d %H%M%S")+'::'+scriptfilename+':'+logdata+'\r\n')
#            logFile.close();           
#        except UnicodeEncodeError:
#			pass

        
    def get_charset(self, message, default="ascii"):
        if message.get_content_charset():
            return message.get_content_charset()
        if message.get_charset():
            return message.get_charset()
        return default
 
    def get_body(self, message):
        """Get the body of the email message"""
        if message.is_multipart():
            #get the plain text version only
            text_parts = [part for part in typed_subpart_iterator(message,'text','plain')]
            body = []
            for part in text_parts:
                charset = get_charset(part, get_charset(message))
                body.append(unicode(part.get_payload(decode=True),
                                    charset,
                                    "replace"))

            return u"\n".join(body).strip()

        else: # if it is not multipart, the payload will be a string
              # representing the message body
            body = unicode(message.get_payload(decode=True),
                           get_charset(message),
                           "replace")
            return body.strip()
    
    def parse_attachment(self, message_part):
        content_disposition = message_part.get("Content-Disposition", None)
        if content_disposition:
            print message_part.get_content_type()
            dispositions = content_disposition.strip().split(";")
            if bool(content_disposition and dispositions[0].lower() == "attachment"):
                file_data = message_part.get_payload(decode=True)
                attachment = StringIO(file_data)
                attachment.content_type = message_part.get_content_type()
                attachment.size = len(file_data)
                attachment.name = None
                attachment.create_date = None
                attachment.mod_date = None
                attachment.read_date = None
                for param in dispositions[1:]:
                    name,value = param.split("=")
                    name = name.lower()
                    if name == "filename":
                        attachment.name = value
                    elif name == "create-date":
                        attachment.create_date = value  #TODO: datetime
                    elif name == "modification-date":
                        attachment.mod_date = value #TODO: datetime
                    elif name == "read-date":
                        attachment.read_date = value #TODO: datetime
                return attachment
        return None
    
    def mailProcess(self, dict, mail):
        
        for part in mail.walk():
            content_disposition = part.get("Content-Disposition", None)
            if content_disposition:
                if part.get_param('name') is None:
                    pass
                else:
                    try:
                        h = part.get_param('name')
                        attach_name = ''.join(s.decode(c or 'us-ascii') for s, c in email.header.decode_header(h))
                        #dict['new'].append(dict['_id']+'__'+decode_header(part.get_param('name').decode('utf8','ignore'))[0][0])
                        dict['attachments_list'].append(dict['_id']+'__'+attach_name)
                        if not self.bb_attachments.exists({"_id": dict['_id']+'__'+attach_name}):
                            try:
                                self.bb_attachments.put(base64.b64decode(part.get_payload()), content_type=part.get_content_type(), filename=attach_name, _id=dict['_id']+'__'+attach_name)
                            except Exception, err:
                                self.bb_attachments.put(part.get_payload(), content_type=part.get_content_type(), filename=attach_name, _id=dict['_id']+'__'+attach_name)
                        if not self.bb_attachments1.exists({"_id": dict['_id']+'__'+part.get_param('name')}):
                            try:
                                self.bb_attachments1.put(base64.b64decode(part.get_payload()), content_type=part.get_content_type(), filename=attach_name, _id=dict['_id']+'__'+attach_name)
                            except Exception, err:
                                self.bb_attachments1.put(part.get_payload(), content_type=part.get_content_type(), filename=attach_name, _id=dict['_id']+'__'+attach_name)
                    except:
                        #dict['new'].append(dict['_id']+'__'+decode_header(part.get_param('name').decode('utf8','ignore'))[0][0])
                        dict['attachments_list'].append(dict['_id']+'__'+unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'))
                        if not self.bb_attachments.exists({"_id": dict['_id']+'__'+unicode(decode_header(part.get_param('name'))[0][0], errors='ignore')}):
                            try:
                                self.bb_attachments.put(base64.b64decode(part.get_payload()), content_type=part.get_content_type(), filename=unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'), _id=dict['_id']+'__'+unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'))
                            except Exception, err:
                                self.bb_attachments.put(part.get_payload(), content_type=part.get_content_type(), filename=unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'), _id=dict['_id']+'__'+unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'))
                        if not self.bb_attachments1.exists({"_id": dict['_id']+'__'+part.get_param('name')}):
                            try:
                                self.bb_attachments1.put(base64.b64decode(part.get_payload()), content_type=part.get_content_type(), filename=unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'), _id=dict['_id']+'__'+unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'))
                            except Exception, err:
                                self.bb_attachments1.put(part.get_payload(), content_type=part.get_content_type(), filename=unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'), _id=dict['_id']+'__'+unicode(decode_header(part.get_param('name'))[0][0], errors='ignore'))
                        
        return dict
        
    def insertIntoDB(self, dict, mail):
        conn = MySQLdb.connect( host="",user = "",passwd = "",db="")
        cursor = conn.cursor()
        cursor.execute ("SELECT 1 FROM process_it_mawbdetail WHERE mawbNum='%s'" % (dict['Mawb']))
        row = cursor.fetchone()        
        cursor.close()
        conn.close()
        msg = "SELECT 1 FROM process_it_mawbdetail WHERE mawbNum="+(dict['Mawb'])
        self.writeDBLog(logdata=msg)

        if not row:
            conn = MySQLdb.connect( host="",user = "",passwd = "",db="")
            cursor = conn.cursor()
            cursor.execute(""" INSERT INTO process_it_mawbdetail (papFlag, pamFlag, mawbNum, preAlertReceivedDate, preAlertReceivedTime, lastUpdatedDate, lastUpdatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s) """,(True, False, dict['Mawb'], datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S")))
            cursor.close()
            conn.commit()
            conn.close()
            msg = """ INSERT INTO process_it_mawbdetail (papFlag, pamFlag, mawbNum, preAlertReceivedDate, preAlertReceivedTime, lastUpdatedDate, lastUpdatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s) """,(True, False, dict['Mawb'], datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"))
            self.writeDBLog(logdata=msg)
        else:            
            dict['duplicate'] = '1'
            dict['categories'] = self.dbObj2.ds.find({"Mawb":dict['Mawb']})[0]['categories']
            dict['categories'].append('yellow')            
            
        dict = self.mailProcess(dict,mail)
        dict['attachments_list'] = list(set(dict['attachments_list']))
        self.dbObj2.ds.insert(dict,force_insert=True)
        self.dbObj1.ds.insert(dict,force_insert=True)
            
    def startParsing(self):
        print dir(self)
        #host = "mail.invoize.com"
        host = "pop.gmail.com"
        M = poplib.POP3_SSL('pop.googlemail.com', '995')
        #M = poplib.POP3_SSL(host)
        print M.getwelcome()
        print M.user("lax.bb.air.hcl.ceva@searce.com")
        print M.pass_("Searce@888")
        #print '/////////////////////////////',M.list()[1]
        print '/////////////////////////////',M.uidl()[1]
        numMessages = len(M.list()[1])
        print "total msg",numMessages
        logmsg = "script start and total_mails are "+str(numMessages)
        self.writeLog(logdata=logmsg,DEBUG=1)
        for i in range(0,numMessages):            
            try:
                print M.uidl()[1][i].split(' ')[1]
                msg = M.retr(i+1)            
            except:
                print 'in except'
                logmsg = "MAIL MISSING ERROR and UIDL's LIST "+M.uidl()[1]
                self.writeLog(logdata=logmsg,DEBUG=1)
                continue            
            #msg = M.retr(sys.argv[1])
            str1 = string.join(msg[1], "\n")
            mail = email.message_from_string(str1)
            #to = re.sub('</br>','',mail["To"])
            #############To############
            mailToList = mail.get_all('To', []) #mail.get('To').split(',')
            to = ''          
            print "mailToList=",mailToList  
            for address in mailToList:
                #print "addrfess:", type(parseaddr(address)[1])
                to = to + parseaddr(address)[1] + ','
            to = mail.get('To')#to.rstrip(',')
            #-------------Cc-----------------#
            try:
                mailCcList = mail.get_all('Cc', []) #mail.get('Cc').split(',')
            except:
                mailCcList = []
            cc = ''
            print "mailCcList=",mailCcList
            for address in mailCcList:
                cc = cc + parseaddr(address)[1] + ','
            cc = mail.get('Cc')#cc.rstrip(',')        
            ###########################        
            sender = parseaddr(mail.get('From'))[1]
            date_is = parsedate(mail.get('Date'))[1]
            if mail['Subject'] is not None:
                decodefrag = decode_header(mail['Subject'])
                subj_fragments = []
                for s , enc in decodefrag:
                    if enc:
                        try:
                            s = unicode(s , enc).encode('utf8','replace')
                        except:
                            s = s.decode('utf8','ignore')
                    subj_fragments.append(s)
                subject = ''.join(subj_fragments)
            else:
                subject = None
            mail_str = str(mail)
            date = mail["Date"]
            print "before uidl",subject
            print "and uidl",M.uidl()[1][i].split(' ')[1]
            if self.dbObj1.ds.find({"uidl":M.uidl()[1][i].split(' ')[1]}).count() > 0:
                print "in uidl"
                continue
            dict = {}
            dict1 = {}
            hbl_lst = []
            dict['to'] = to
            dict['uidl'] = M.uidl()[1][i].split(' ')[1]
            dict['from'] = sender
            dict['subject'] = subject
            dict['cc'] = cc
            if len(date) == 37:
                if '+' in date:
                    ind = date.index('+')
                    hrs = 5 - int(date[ind+1:ind+3])
                    dict['date'] = datetime.strptime(date[:-12], "%a, %d %b %Y %H:%M:%S") + timedelta(hours=hrs,minutes=30) #.strftime("%Y%m%d%H%M%S") #.strftime("%m-%d-%Y")
                elif '-' in date:
                    ind = date.index('-')
                    hrs = 5 + int(date[ind+1:ind+3])
                    dict['date'] = datetime.strptime(date[:-12], "%a, %d %b %Y %H:%M:%S") + timedelta(hours=hrs,minutes=30) #.strftime("%Y%m%d%H%M%S") #.strftime("%m-%d-%Y")
                else:
                    dict['date'] = datetime.strptime(date[:-12], "%a, %d %b %Y %H:%M:%S")
            else:
                if '+' in date:
                    ind = date.index('+')
                    hrs = 5 - int(date[ind+1:ind+3])
                    dict['date'] = datetime.strptime(date[:-6], "%a, %d %b %Y %H:%M:%S") + timedelta(hours=hrs,minutes=30) #.strftime("%Y%m%d%H%M%S") #.strftime("%m-%d-%Y")
                elif '-' in date:
                    ind = date.index('-')
                    hrs = 5 + int(date[ind+1:ind+3])
                    dict['date'] = datetime.strptime(date[:-6], "%a, %d %b %Y %H:%M:%S") + timedelta(hours=hrs,minutes=30) #.strftime("%Y%m%d%H%M%S") #.strftime("%m-%d-%Y")
                else:
                    dict['date'] = datetime.strptime(date[:-6], "%a, %d %b %Y %H:%M:%S")
            hrs = 0    
            dict['date'] = dict['date'].strftime("%Y%m%d%H%M%S")
            dict['prealert'] = "1"
            dict['manual'] = "0"
            dict['bb'] = "1"
            dict['attachments_list'] = []
            dict['categories'] = []
            dict["mailbox"] = 'lax_import'
            doc_id = str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
            dict['_id'] = doc_id
            dict['id'] = doc_id
            #print doc_id
            body = None
            html = None
            for part in mail.walk():
                if part.get_content_type() == 'text/plain':
                    if body is None:
                        body = ""
                        try:
                            body += unicode(
                                part.get_payload(decode=True),
                                part.get_content_charset(),
                                'replace'
                            ).encode('utf8','replace')
                        except:
                            body += part.get_payload(decode=True).decode('utf8','ignore')
                elif part.get_content_type() == "text/html":
                    if html is None:
                        html = ""
                        try:
                            html += unicode(
                                part.get_payload(decode=True),
                                part.get_content_charset(),
                                'replace'
                            ).encode('utf8','replace')
                        except:
                            html += part.get_payload(decode=True).decode('utf8','ignore')
            dict['body_text'] = body
            dict['html_text'] = html
            #PRE-ALERT FOR CNEE/ITAUTEC VCP VIA LAX'
            print "before try",subject
            try:
                if subject.find('Air ETA') == 0:
                    print "Live till Air ETA..."
                    #print 'subject ================== ',subject
                    #print 'id is : ============' ,dict['_id']
                    if mail.is_multipart():
                        print "*********************in is multipart*******************"
                        msg = str(i)+"-:-:-"+subject+"*********************in is multipart*******************-:-:-"+M.uidl()[1][i].split(' ')[1]
                        self.writeLog(logdata=msg,DEBUG=1)
                        print 'subject ================== ',subject
                        #print mail.get_payload(1).get_payload()
                    else:
                        #print "in else part"
                        msg = str(i)+"-:-:-"+date+"-:-:-"+subject+"-:-:-"+M.uidl()[1][i].split(' ')[1]
                        self.writeLog(logdata=msg,DEBUG=1)
                        data = mail.get_payload()
                        station = data[data.find('-US')+4:data.find('-US')+7]
                        mawb = data[data.rfind('MAWB')+5:data.rfind('IC:')]
                        ic = data[data.rfind('IC:')+3:data.rfind('PC:')]
                        pc = data[data.rfind('PC:')+3:data.rfind('WGT:')]
                        wgt = data[data.rfind('WGT:')+4:data.rfind('FLIGHT#')]
                        flight_num = data[data.rfind('FLIGHT#')+7:data.rfind('FLIGHT#')+11]
                        etd = data[data.rfind('ETD:')+4:data.rfind('ETA:')]
                        eta = data[data.rfind('ETA:')+4:data.rfind('\n\n----------')]
                        dict['station'] = station
                        dict['Mawb'] = mawb.strip(" ").replace('.','')
                        dict['ic'] = ic.strip(" ")
                        dict['pc'] = pc.strip(" ")
                        dict['weight'] = wgt.strip(" ")
                        dict['flight_num'] = flight_num.strip(" ").strip("\n")
                        if eta.strip(" ") <> "\n\n----------":
                            dict['eta'] = eta.strip(" ")
                        else:
                            dict['eta'] = ""
                        dict['etd'] = etd.strip(" ")
                        data1 = data[data.rfind('ORIGIN'):data.rfind('This e-mail message')]
                        splitted_list = data1.split('|')
                        index = 9
                        count = (len(splitted_list) - 1) / 9
                        while (index < len(splitted_list) - 1):
                            if(index == 9):
                                temp_origin = splitted_list[int(index)].strip(" ")
                                dict1['origin'] = temp_origin[temp_origin.rfind("----\n") + 5:]#splitted_list[int(index)].strip(" ")
                            else:
                                dict1['origin'] = splitted_list[int(index)].strip(" ")[splitted_list[int(index)].strip(" ").rfind("\n\n")+2:]
                            dict1['Hawb'] = splitted_list[int(index) + 1].strip(" ")
                            dict1['shipper'] = splitted_list[int(index) + 2].strip(" ")
                            dict1['destination'] = splitted_list[int(index) + 3].strip(" ")
                            dict1['consignee'] = splitted_list[int(index) + 4].strip(" ")
                            dict1['pcsPerPkg'] = splitted_list[int(index) + 5].strip(" ")
                            dict1['actPerKgs'] = splitted_list[int(index) + 6].strip(" ")
                            dict1['cbm'] = splitted_list[int(index) + 7].strip(" ")
                            dict1['porc'] = splitted_list[int(index) + 8].strip(" ")
                            dict1['references'] = splitted_list[int(index) + 9].strip(" ")[:splitted_list[int(index) + 9].strip(" ").rfind("\n\n")].strip("\n")
                            dict1['id'] = str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
                            hbl_lst.append(dict1)
                            index = index + 9
                            dict1 = {}
                        dict['Hawb_details'] = hbl_lst
                        flg = 1
                        conn = MySQLdb.connect( host="",user = "",passwd = "",db="")
                        cursor = conn.cursor()
                        cursor.execute ("SELECT 1 FROM process_it_mawbdetail WHERE mawbNum='%s'" % (dict['Mawb']))
                        row = cursor.fetchone()                        
                        cursor.close()
                        conn.close()
                        msg = "SELECT 1 FROM process_it_mawbdetail WHERE mawbNum="+(dict['Mawb'])
                        self.writeDBLog(logdata=msg)
                        #print dict
                        if not row:
                            if dict['station'] == 'LAX' or dict['station'] == 'SFO':                                
                                if [ True for hawb in dict['Hawb_details'] if "MEDTRONIC HEART" in hawb['consignee']] :
                                    scope_flag = False
                                else:
                                    scope_flag = True
                            else:
                                scope_flag = False
                            #print dict
                            conn = MySQLdb.connect( host="",user = "",passwd = "",db="")
                            cursor = conn.cursor()
                            cursor.execute(""" INSERT INTO process_it_mawbdetail (papFlag, pamFlag, mawbNum, station, flightNum, preAlertReceivedDate, preAlertReceivedTime, lastUpdatedDate, lastUpdatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,(scope_flag, False, dict['Mawb'], dict['station'], dict['flight_num'], datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S")))
                            cursor.close()
                            conn.commit()
                            conn.close()
                            msg = """ INSERT INTO process_it_mawbdetail (papFlag, pamFlag, mawbNum, station, flightNum, preAlertReceivedDate, preAlertReceivedTime, lastUpdatedDate, lastUpdatedTime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) """,(scope_flag, False, dict['Mawb'], dict['station'], dict['flight_num'], datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"))
                            self.writeDBLog(logdata=msg)
                        else:
                            flg = 0
                            dict['duplicate'] = '1'
                            dict['categories'] = self.dbObj2.ds.find({"Mawb":dict['Mawb']})[0]['categories']
                            dict['categories'].append('yellow')
                            conn = MySQLdb.connect( host="",user = "",passwd = "",db="")
                            cursor = conn.cursor()
                            
                            cursor.execute ("""
                                   UPDATE process_it_mawbdetail 
                                   SET station=%s, flightNum=%s, preAlertReceivedDate=%s, preAlertReceivedTime=%s, lastUpdatedDate=%s, lastUpdatedTime=%s
                                   WHERE mawbNum=%s
                                 """,(dict['station'], dict['flight_num'], datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), dict['Mawb']))
                            '''
                            cursor.execute ("""
                                   UPDATE process_it_mawbdetail 
                                   SET papFlag=%s ,station=%s, flightNum=%s, preAlertReceivedDate=%s, preAlertReceivedTime=%s, lastUpdatedDate=%s, lastUpdatedTime=%s
                                   WHERE mawbNum=%s
                                 """,(True, dict['station'], dict['flight_num'], datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), dict['Mawb']))
                            '''
                            cursor.close()
                            conn.commit()
                            conn.close()
                            msg = """UPDATE process_it_mawbdetail 
                                   SET station=%s, flightNum=%s, preAlertReceivedDate=%s, preAlertReceivedTime=%s, lastUpdatedDate=%s, lastUpdatedTime=%s
                                   WHERE mawbNum=%s""",(dict['station'], dict['flight_num'], datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d"), datetime.strptime(dict['date'], "%Y%m%d%H%M%S").strftime("%H:%M:%S"), dict['Mawb'])
                            self.writeDBLog(logdata=msg)

                        if dict['station'] == 'LAX':
                            dict['categories'].append('green')
                        elif dict['station'] == 'SFO':
                            dict['categories'].append('blue')
                        dict['categories'] = list(set(dict['categories']))
                        self.dbObj2.ds.insert(dict,force_insert=True)
                        self.dbObj1.ds.insert(dict,force_insert=True)
                            
                        dict = {}
                #FW: PRE ALERT SOF-LAX MAWB:057-73696781 HAWB:ARC-10120940 SHI:DIKO\n IVAN DIKOLAKOV CO:ZOBELE MEXICO
                #'Air ETA 22-Oct-2012 ADL 081-79171385'
               # elif re.search('MAWB.*-\d{8}',subject,flags=re.IGNORECASE):
                    #print "Live till MAWB.*-\d{8}..."
                    #msg = str(i)+"-:-:-"+subject+"-:-:-"+M.uidl()[1][i].split(' ')[1]
                    #self.writeLog(logdata=msg,DEBUG=1)
                    #print 'MAIL NO ================== ',i
                    #data = re.search('MAWB.*-\d{8}',subject,flags=re.IGNORECASE)
                    #mawb = data.group(0)
                    #dict['Mawb'] = mawb[mawb.rfind("-")-3:].strip(" ")
                    
                    #self.insertIntoDB(dict,mail)
                   # pass
                elif re.search('\d{3}-\d{8}',subject,flags=re.IGNORECASE):
                    print "Live till \d{3}-\d{8}..."
                    msg = str(i)+"-:-:-"+subject+"-:-:-"+M.uidl()[1][i].split(' ')[1]
                    self.writeLog(logdata=msg,DEBUG=1)
                    #print 'MAIL NO ================== ',i
                    data = re.search('\d{3}-\d{8}',subject,flags=re.IGNORECASE)
                    mawb = data.group(0)
                    dict['Mawb'] = mawb    
                    self.insertIntoDB(dict,mail)
                elif re.search('\d{3}'+'-'+'\d{4}'+' '+'\d{4}',subject):
                    print "Live till \d{3}'+'-'+'\d{4}'+' '+'\d{4}..."
                    msg = str(i)+"-:-:-"+subject+"-:-:-"+M.uidl()[1][i].split(' ')[1]
                    self.writeLog(logdata=msg,DEBUG=1)
                    data = re.search('\d{3}'+'-'+'\d{4}'+' '+'\d{4}',subject)
                    mawb = data.group(0)
                    dict['Mawb'] = mawb.replace(' ','')
                    self.insertIntoDB(dict,mail)
                else:
                    '''These are mails in which we can't find any useful detail not even Mawb number and they might contain attachments'''
                    print "Live till no data..."
                    msg = str(i)+"-:-:-"+subject+"-:-:-"+M.uidl()[1][i].split(' ')[1]
                    self.writeLog(logdata=msg,DEBUG=1)
                    dict = self.mailProcess(dict,mail)
                    dict['categories'].append('red')
                    self.dbObj2.ds.insert(dict,force_insert=True)
                    self.dbObj1.ds.insert(dict,force_insert=True)
                    dict = {}
            except:
                dict['categories'] = []
                print "Live till except..."
                dict['categories'].append('red')
                dict['attachments_list'] = []
                error = str(sys.exc_info()[1])
                msg = str(i)+"-:-:-"+subject+" ERROR="+error+"-:-:-"+M.uidl()[1][i].split(' ')[1]
                self.writeLog(logdata=msg,DEBUG=1)
                self.dbObj1.ds.insert(dict,force_insert=True)
                self.dbObj2.ds.insert(dict,force_insert=True)
                dict = {}
        M.quit()
        
if __name__ == '__main__':
    papObj = Pre_Alert_Parser()
    papObj.startParsing()
