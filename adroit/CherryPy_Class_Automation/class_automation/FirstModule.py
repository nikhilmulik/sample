
import cherrypy
import MySQLdb
from datetime import date
import datetime
import telnetlib
import os
import datetime
from dateutil.relativedelta import *
import calendar
from datetime import date



localDir = os.path.dirname(__file__)
#localDir = 'C:/Users/nikhil.mulik/Desktop/class_automation'
absDir = os.path.join(os.getcwd(), localDir)


class FileDemo(object):
    # Open database connection
    # cherrypy.config.get(key, defaultValue = None)
    # _db = MySQLdb.connect(cherrypy.config.get('host'), cherrypy.config.get('user'), cherrypy.config.get('passwd'), "ADROIT")
    # _db = ""
    # _cursor = ""

    #def __init__(self):
    #    self._db = MySQLdb.connect(cherrypy.config['host'], cherrypy.config['user'], cherrypy.config['passwd'], "ADROIT")
    #    self._cursor = self._db.cursor()

    def renderScreen(self, data, pagedown):
        """ rendering screen of worldport into output screen"""
        dataA = data.split('\x1b')
        print dataA
        if pagedown != 1:
            self.ScreenString = " " * 80 * 27
        startPos = 0
        flag = 0
        theData = ''
        for x in dataA:
            i = 0
            if flag == 1:
                if x[0] == '[' and len(x) > 4:
                    if x[2] == ';':
                        if x[4] == 'H':
                            i = 5
                            startPos = int(x[1]) * 80 + int(x[3]) - 1
                        elif x[4] == 'm':
                            i = 5
                        elif x[5] == 'H':
                            i = 6
                            startPos = int(x[1]) * 80 + int(x[3:5]) - 1
                    if x[3] == ';':
                        if x[5] == 'H':
                            i = 6
                            startPos = int(x[1:3]) * 80 + int(x[4]) - 1
                        elif x[5] == 'm':
                            i = 6
                        elif x[6] == 'H':
                            i = 7
                            startPos = int(x[1:3]) * 80 + int(x[4:6]) - 1
                if len(x) > 2 and (x[2] == 'm' or x[2] == 'J'):
                    i = 3
                    theData = theData + x[i::]
                elif len(x) > 4 and (x[4] == 'm'):
                    i = 5
                    theData = theData + x[i::]
                elif len(x) < 4:
                    i = 4
                    theData = theData + x[i::]
                else:
                    theData = x[i::]
                self.ScreenString = self.ScreenString[0:startPos] + theData + self.ScreenString[startPos + len(theData)::]

            if x == '[?7h' or x == '[2J' or pagedown == 1:
                flag = 1
        return self.ScreenString[1::]

    def get_results(self, query):
        self._db = MySQLdb.connect(cherrypy.config['host'], cherrypy.config['user'], cherrypy.config['passwd'], "ADROIT")
        self._cursor = self._db.cursor()
        # query = "UPDATE process_it_mawbdetail SET createAIDesc='1st page', createAIStatus=1 WHERE mawbNum='" + mawb + "'"
        print "Query-->", query
        #return True
        try:
            # Execute the SQL command
            self._cursor.execute(query)
            self._db.commit()

            #print "ur====>", self._db.use_result()
            #print "sr====>", self._db.store_result()
            #print "ar====>", self._db.affected_rows()

            # Fetch all the rows in a list of lists.
            #results = cursor.fetchall()
            #for row in results:
            #   print row
        except:
            self._db.rollback()
            return False
        self._db.close()
        return True
        pass

    def checkpoint(self, data, checkpoint_str, tn, checkpoint_timeout):
        if checkpoint_str:
            response_str = tn.read_until(checkpoint_str, checkpoint_timeout)
            if checkpoint_str in response_str:
                data[0] += "<br><br>" + response_str
                return True
            else:
                return False
        pass

    def check_access(self):

        # print "connection from: ",remote_addr
        # cherrypy.response.headers['content-type']="text/json"
        # cherrypy.response.headers['Retry-After'] = 60
        # cherrypy.response.status = 503
        # cherrypy.response.headers['Access-Control-Allow-Origin'] = "http://122.248.234.221:9011"
        # return "<p>pp</p>"
        #print "base:", cherrypy.request.base

        #print "addr:", remote_addr
        cherrypy.response.headers['Access-Control-Allow-Origin'] = "*"
        return True
        '''
        remote_addr = cherrypy.request.headers['Remote-Addr'].strip()
        if remote_addr not in ["127.0.0.1", "122.248.234.221", "172.16.0.89", "172.16.5.91", "172.16.9.104"]:
            return False
        else:
            cherrypy.response.headers['Access-Control-Allow-Origin'] = "*"
                # "http://" + remote_addr + ":9999"  # cherrypy.request.base
            return True
        '''
        pass

    def ai_create_checkpoint(self, checkpoint_str, mawb):
        query = "UPDATE ADROIT.process_it_mawbdetail SET createAIDesc='Unable to reach checkpoint -" + checkpoint_str + " ', createAIStatus=2  WHERE mawbNum IN ('" + mawb + "')"
        if not self.get_results(query):
            return "some Problem in querying the database..aborting, Unable to create AI file!"
        pass

    def consolno_checkpoint_database(self, checkpoint_str, mawb):
        query = "UPDATE process_it_mawbdetail SET getConsoleDesc='Unable to reach checkpoint -" + checkpoint_str + " ', getConsoleStatus=2  WHERE mawbNum IN ('" + mawb + "')"
        if not self.get_results(query):
            return "some Problem in querying the database..aborting, Unable to create AI file!"
        pass

    def remarks_checkpoint_database(self, checkpoint_str, mawb):
        query = "UPDATE process_it_mawbdetail SET updateRemarksDesc='Unable to reach checkpoint -" + checkpoint_str + " ', updateRemarkStatus=2  WHERE mawbNum IN ('" + mawb + "')"
        if not self.get_results(query):
            return "some Problem in querying the database..aborting, Unable to create AI file!"
        pass

        
        
    def create_ai_file(self, username="", password="", mawb="", station_list="", test_update=0):
        try:
            #self._db = MySQLdb.connect(cherrypy.config['host'], cherrypy.config['user'], cherrypy.config['passwd'], "ADROIT")
            #self._cursor = self._db.cursor()
            if not self.check_access():
                return "Not authorized IP"
                #sys.exit(0)

            # mawb = str(cherrypy.request.body.params['mawb']).strip()
            mawb = str(cherrypy.request.body.params['mawb']).rstrip(",").replace(',', "','")
            username = str(cherrypy.request.body.params['username']).strip()
            password = str(cherrypy.request.body.params['password']).strip()
            test_update = str(cherrypy.request.body.params['test_update']).strip()
            #station_list = str(cherrypy.request.body.params['station_list']).strip()
       
            print "-----------------------------------------------------------------------------------"
            print 'username: ',username
            print 'password: ',password
            print 'mawb: ',mawb
            #print 'station_list: ',station_list
            print 'test_update: ',test_update
            print "-----------------------------------------------------------------------------------"

			
            if username == "" or password == "" or mawb == "":
                return "Not enough data! contact the admin"
                pass
            else:
                #print cherrypy.request.body.params
                #return "not live"
                # createAIStatus = 1  started
                # createAIStatus = 2  done
                # createAIStatus = 3  error

                query = "UPDATE ADROIT.process_it_mawbdetail SET createAIDesc='AI file creation in progress', createAIStatus=1 WHERE mawbNum IN ('" + mawb + "')"
                if not self.get_results(query):
                    return "some Problem in querying the database..aborting, Unable to create AI file!"
                #if self._cursor.rowcount != 1:
                #    return "Mawb does not exist in database or its in progress, wont spawn a new process for AI file!"
                '''
                if(self.get_results(query) == 0):
                    return "Same status in database or Mawb not exist in database, Unable to create AI file!"
                '''
                #HOST = "57.33.98.226"  # live
                #return mawb + "ai done.."

                if test_update == '1':
                    HOST = ""    # test
                else:
                    HOST = ""  # live

                PORT = 23
                data = [""]   # <a onclick='history.back();'>Go back and create another AI file</a></script>"
                username = username     # 'IAHAEKZB'
                password = password     # 'GENERAL5'
                tn = telnetlib.Telnet(HOST)
                tn.open(HOST, PORT)      # get logged in here
                # tn.set_debuglevel(10)
                #print "opening--->",tn.read_untill()
                tn.write(username)
                checkpoint_str = "(C) COPYRIGHT IBM CORP. 1980, 2005"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.ai_create_checkpoint(checkpoint_str, mawb)
                    return "Unable to reach checkpoint :(Login Screen) '" + checkpoint_str + "'"

                tn.write('\t')
                tn.write(password)
                tn.write('\r')

                checkpoint_str = 'is allocated to another job'
                if self.checkpoint(data, checkpoint_str, tn, 2):
                    tn.write('\r')
                    #return data

                if test_update == '1':
                    checkpoint_str = "90. Signoff"
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.ai_create_checkpoint(checkpoint_str, mawb)
                        return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    data[0] += tn.read_until("F12=Cancel", 5)
                    tn.write('17')      # only in test###
                    tn.write('\r')  # this will continue till the below keyword is found
                #checkpoint_str = "This is a production environment signon using live data"
                #if not self.checkpoint(data, checkpoint_str, tn, 5):
                #    self.ai_create_checkpoint(checkpoint_str, mawb)
                #    return "Unable to reach checkpoint : '" + checkpoint_str + "'"

                tn.write('\r')
                checkpoint_str = "Master Applications Menu"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.ai_create_checkpoint(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "', please recheck userid and passwd!"
                data[0] += tn.read_until('IBM AT&T Brokerage', 5)
                data[0] += tn.read_until('=Fast Path', 5)
                data[0] += tn.read_until(' Copyright 2001 H & H Technologies', 5)

                tn.write('\x1b2')
                checkpoint_str = "Select an EXTEND Menu"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.ai_create_checkpoint(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                data[0] += tn.read_until('=Previous', 5)

                tn.write('GMSBB')
                tn.write('\r')
                checkpoint_str = "GATEWAY IMPORT PROCESS MENU"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.ai_create_checkpoint(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                data[0] += tn.read_until('Work with Ready Shipments', 5)
                data[0] += tn.read_until('=Fast Path', 5)

                tn.write('1')
                tn.write('\r')
                checkpoint_str = "Station..............:"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.ai_create_checkpoint(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                data[0] += tn.read_until('Mode.................:', 5)
                data[0] += tn.read_until('Specfic House Bill#..:', 5)
                # data[0] += tn.read_until('=prompt', 5)

                #tn.write(station_list)
                tn.write("   ")
                tn.write('\r')

                for each_mawb in mawb.split(","):
                    checkpoint_str = "RDY Ready Shipments"
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.ai_create_checkpoint(checkpoint_str, mawb)
                        return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    data[0] += tn.read_until('=Container', 5)

                    fomatted_mawb = each_mawb.strip("'").replace("-", "")[:11]
                    tn.write('\t')
                    tn.write(fomatted_mawb)
                    tn.write('\r')
                    mawb_chk_str = tn.read_until(fomatted_mawb, 5)
                    #print "----",mawb_chk_str
                    mawb_chk_str = tn.read_until("F10=View House", 5)

                    if fomatted_mawb in mawb_chk_str:
                        data[0] += "<br>Valid Mawb exists in GMSBB"
                        data[0] += "<br><br>" + "8th page--<br><br>" + mawb_chk_str

                        tn.write('\t')
                        tn.write('\t')
                        tn.write('\t')
                        tn.write('\t')
                        tn.write('\t')
                        tn.write('x')
                        tn.write('\x1b2')
                        checkpoint_str = "Send To Operations Window"
                        if not self.checkpoint(data, checkpoint_str, tn, 5):
                            self.ai_create_checkpoint(checkpoint_str, each_mawb.strip("'"))
                            #return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                        data[0] += tn.read_until('=Send To Ops', 5)
                        tn.write('\x1b2')
                        '''
                        cross_verify_str = tn.read_until('F10=View House', 5)
                        data[0] += "<br><br>" + "9th page--<br><br>" + cross_verify_str

                        if mawb in cross_verify_str:
                            data[0] += "<br>Some problem in creating AI file, Mawb still exist in GMSBB after all steps!<br>"
                            query = "UPDATE process_it_mawbdetail SET createAIDesc='Mawb still exist in GMSBB after all steps!', createAIStatus=2 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                            if(not self.get_results(query)):
                                return "some Problem in querying the database..aborting, Unable to create AI file!"
                            #return data  # "prob"
                        else:
                            data[0] += "<br><br>---AI File Created successfully--"
                            query = "UPDATE process_it_mawbdetail SET createAIDesc='Done', createAIStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                            if(not self.get_results(query)):
                                return "some Problem in querying the database..aborting, but AI file created"
                            #return "AI File Created successfully"  # data[0]  # "done!"
                        '''
                        query = "UPDATE ADROIT.process_it_mawbdetail SET createAIDesc='AI file created', createAIStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                        if(not self.get_results(query)):
                            return "some Problem in querying the database..aborting, Unable to create AI file!"
                        #return self.renderScreen(data,0)
                    else:
                        data[0] += "Mawb not in GMSBB!"
                        tn.write('\x1b2')
                        query = "UPDATE ADROIT.process_it_mawbdetail SET createAIDesc='Mawb does not exists in GMSBB!', createAIStatus=4 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                        if(not self.get_results(query)):
                            return "some Problem in querying the database..aborting, but AI file created"
                        #return "Mawb not in GMSBB!"  # data[0]  #  "Mawb not in GMSBB"                
                tn.close               
            #self._db.close()
            return "Status updated in database, refresh the screen to see the changes!"
            pass
        except:
            return "Some problem in creatung AI file at server..pls try: after some time!! ( Notify sys admin if this persist for a long)"
 
 
    def update_remarks(self, username="", password="", remark="", console_no="", test_update="", mawb=""):
        if True:
            #self._db = MySQLdb.connect(cherrypy.config['host'], cherrypy.config['user'], cherrypy.config['passwd'], "ADROIT")
            #self._cursor = self._db.cursor()
            if not self.check_access():
                return "Not authorized IP"
                #sys.exit(0)

  
            #itinfo = str(cherrypy.request.body.params['itinfo'])#.rstrip(",")
            remark = str(cherrypy.request.body.params['remark']).rstrip(",").replace("','", ",")
            username = str(cherrypy.request.body.params['username']).strip()
            password = str(cherrypy.request.body.params['password']).strip()
            mawb = str(cherrypy.request.body.params['mawb']).rstrip(",").replace(',', "','")
            console_no = str(cherrypy.request.body.params['console_no']).rstrip(",").replace("','", ",")
            test_update = str(cherrypy.request.body.params['test_update']).strip()
            
       
            print "-----------------------------------------------------------------------------------"
            #print 'itinfo: ',itinfo
            print 'remark: ',remark
            print 'username: ',username
            print 'password: ',password
            print 'mawb: ',mawb
            print 'console_n: ',console_no
            print 'test_update: ',test_update
            print "-----------------------------------------------------------------------------------"


            #return mawb + " ---" + console_no + " ---" + remark

            if username == "" or password == "" or remark == "" or console_no == "" or mawb == "":
                return "Not enough data! contact the admin"
                pass
            else:
                #return "udate rematrks"
                query = "UPDATE process_it_mawbdetail SET updateRemarksDesc='Started', updateRemarkStatus=1 WHERE mawbNum IN ('" + mawb + "')"
                if not self.get_results(query):
                    return "some Problem in querying the database..aborting, Unable to create AI file!"
                #if self._cursor.rowcount != 1:
                #    return "Mawb does not exist in database or its in progress, wont spawn a new process for AI file!"
                # print "ur====>", self._db.use_result()
                # print "sr====>", self._db.store_result()
                #print "ar====>", self._db.affected_rows()
                #print "ar====>", self._cursor.rowcount
                '''
                if(self.get_results(query) == 0):
                    return "Same status in database or Mawb not exist in database, Unable to create AI file!"
                '''
                #return "Ai file done"

                #HOST = "57.33.98.226"  # live
                if test_update == '1':
                    HOST = ""    # test
                else:
                    HOST = ""  # live

                PORT = 23
                data = [""]   # <a onclick='history.back();'>Go back and create another AI file</a></script>"
                username = username     # 'IAHAEKZB'
                password = password     # 'GENERAL5'
                tn = telnetlib.Telnet(HOST)
                tn.open(HOST, PORT)      # get logged in here
                tn.set_debuglevel(10)
                #print "opening--->",tn.read_untill()
                tn.write(username)
                checkpoint_str = "(C) COPYRIGHT IBM CORP. 1980, 2005"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.remarks_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"

                tn.write('\t')
                tn.write(password)
                tn.write('\r')

                checkpoint_str = 'is allocated to another job'
                if self.checkpoint(data, checkpoint_str, tn, 2):
                    tn.write('\r')
                    #return data

                if test_update == '1':
                    checkpoint_str = "90. Signoff"
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.remarks_checkpoint_database(checkpoint_str, mawb)
                        return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    data[0] += tn.read_until("F12=Cancel", 5)
                    tn.write('17')      # only in test###
                    tn.write('\r')  # this will continue till the below keyword is found
                #checkpoint_str = "This is a production environment signon using live data"
                #if not self.checkpoint(data, checkpoint_str, tn, 5):
                #    self.update_checkpoint_database(checkpoint_str, mawb)
                #    return "Unable to reach checkpoint : '" + checkpoint_str + "'"

                tn.write('\r')
                checkpoint_str = "Master Applications Menu"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.remarks_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "', please recheck userid and passwd!"
                data[0] += tn.read_until('IBM AT&T Brokerage', 5)
                data[0] += tn.read_until('=Fast Path', 5)
                data[0] += tn.read_until(' Copyright 2001 H & H Technologies', 5)

                tn.write('\x1b2')
                checkpoint_str = "Select an EXTEND Menu"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.remarks_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                data[0] += tn.read_until('=Previous', 5)

                tn.write('bbulk')
                tn.write('\r')
                checkpoint_str = "Open/Update a Breakbulk File"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.remarks_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                data[0] += tn.read_until('=Fast Path', 5)

                tn.write('1')
                tn.write('\r')
                mawbs = mawb.split(",")
                remarks = remark.split(",")
                consoles = console_no.split(",")
#                itinfo = itinfo.split(",")
                for i in xrange(len(mawbs)):
                    each_mawb = mawbs[i]
                    each_remark = remarks[i]
                    each_consol = consoles[i]
#                    each_itinfo = itinfo[i]
                    #fomatted_mawb = each_mawb.strip("'").replace("-", "")[:11]

                    checkpoint_str = "Enter Consolidation No.:"
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.remarks_checkpoint_database(checkpoint_str, mawb)
                        return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    data[0] += tn.read_until('=House Bill Review', 5)

                    tn.write(each_consol)
                    tn.write('\r')
                    checkpoint_str = each_consol
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.remarks_checkpoint_database(checkpoint_str, each_mawb.strip("'"))
                        return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    data[0] += tn.read_until('=Check Now', 5)

                    tn.write('\x1b5')
                    checkpoint_str = "-- R E M A R K S --"
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.remarks_checkpoint_database(checkpoint_str, each_mawb.strip("'"))
                        return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    data[0] += tn.read_until('Line commands:', 5)
                    data[0] += tn.read_until('=Delete all', 5)

                    tn.write('\x04')
                    temp=tn.read_some()
                    while len(temp)>0:
                        data[0]+=temp
                        temp=tn.read_very_eager()
                    tn.write('\x04')
                    temp=tn.read_some()
                    while len(temp)>0:
                        data[0]+=temp
                        temp=tn.read_very_eager()
                    tn.write('\x04')
                    temp=tn.read_some()
                    while len(temp)>0:
                        data[0]+=temp
                        temp=tn.read_very_eager()


                    #tn.write('\t\t\t\t\t\t\t\t\t\t\t\t\t\t')  #14 earlier ut was working
                    tn.write('\t\t\t\t\t\t\t\t\t\t\t\t')  # 12 TAB

#                    tn.write(each_itinfo)
#                    tn.write('\t\t')

                    tn.write(each_remark)
                    tn.write('\x1b2')
                    '''
                    checkpoint_str = each_remark
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.remarks_checkpoint_database(checkpoint_str, each_mawb.strip("'"))
                        #return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    if not self.checkpoint(data, checkpoint_str, tn, 3):
                        tn.write('\x04')
                        if not self.checkpoint(data, checkpoint_str, tn, 5):
                            self.remarks_checkpoint_database(checkpoint_str, each_mawb.strip("'"))
                        #return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    else:
                        #return "Remarks updated successfully"
                        query = "UPDATE process_it_mawbdetail \
                            SET remarksInClass=(CASE WHEN remarksInClass IS NULL THEN '" + each_remark + "' ELSE CONCAT('" + each_remark + "',',',remarksInClass) END), \
                            updateRemarkStatus=3, updateRemarksDesc='Done' WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                        if not self.get_results(query):
                            return "some Problem in querying the database..aborting, Unable to update remarks!"
                        pass
                    '''
                    query = "UPDATE process_it_mawbdetail \
                        SET remarksInClass=(CASE WHEN remarksInClass IS NULL THEN '" + each_remark + "' ELSE CONCAT('" + each_remark + "',',',remarksInClass) END), \
                        updateRemarkStatus=3, updateRemarksDesc='Done' WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                    if not self.get_results(query):
                        return "some Problem in querying the database..aborting, Unable to update remarks!"
                    tn.write('\x1b[24~')
                    tn.write('\x1b[24~')
                tn.close            
            #self._db.close()

            return "Done, Updated in database!"
        else:
            return "Some problem in updating remarks at server..pls try after some time!! ( Notify sys admin if this persist for a long)"
            
              
            
           
    def get_console_num(self, username="", password="", test_update="", mawb=""):
        try:
            #self._db = MySQLdb.connect(cherrypy.config['host'], cherrypy.config['user'], cherrypy.config['passwd'], "ADROIT")
            #self._cursor = self._db.cursor()
            if not self.check_access():
                return "Not authorized IP"
                #sys.exit(0)

            username = str(cherrypy.request.body.params['username']).strip()
            password = str(cherrypy.request.body.params['password']).strip()
            # mawb = str(cherrypy.request.body.params['mawb']).strip(",").replace('-', '')
            mawb = str(cherrypy.request.body.params['mawb']).rstrip(",").replace(',', "','")
            test_update = str(cherrypy.request.body.params['test_update']).strip()

            # return "SELECT * FROM process_it_mawbdetail WHERE mawbNum IN ('" + mawb + "')"

            if username == "" or password == "" or mawb == "":
                return "Not enough data! contact the admin"
                pass
            else:
                #return "update remarks"
                query = "UPDATE ADROIT.process_it_mawbdetail SET getConsoleStatus=1 WHERE mawbNum IN ('" + mawb + "')"
                if not self.get_results(query):
                    return "some Problem in querying the database..aborting!" 

                '''
                if(self.get_results(query) == 0):
                    return "Same status in database or Mawb not exist in database!"
                '''



                PORT = 23
                data = [""]
                username = username     # ''
                password = password     # ''
                tn = telnetlib.Telnet(HOST)
                tn.open(HOST, PORT)      # get logged in here
                # tn.set_debuglevel(10)
                #print "opening--->",tn.read_untill()
                tn.write(username)
                checkpoint_str = "(C) COPYRIGHT IBM CORP. 1980, 2005"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.consolno_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint :(Login Screen) '" + checkpoint_str + "'"

                tn.write('\t')
                tn.write(password)
                tn.write('\r')

                checkpoint_str = 'is allocated to another job'
                if self.checkpoint(data, checkpoint_str, tn, 2):
                    tn.write('\r')
                    #return data

                if test_update == '1':
                    checkpoint_str = "90. Signoff"
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.consolno_checkpoint_database(checkpoint_str, mawb)
                        return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    data[0] += tn.read_until("F12=Cancel", 5)
                    tn.write('17')      # only in test###
                    tn.write('\r')  # this will continue till the below keyword is found

                #checkpoint_str = "This is a production environment signon using live data"
                #if not self.checkpoint(data, checkpoint_str, tn, 5):
                #    self.consolno_checkpoint_database(checkpoint_str, mawb)
                #    return "Unable to reach checkpoint : '" + checkpoint_str + "'"

                tn.write('\r')
                checkpoint_str = "Master Applications Menu"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.consolno_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "', please recheck userid and passwd!"
                data[0] += tn.read_until('IBM AT&T Brokerage', 5)
                data[0] += tn.read_until('=Fast Path', 5)
                data[0] += tn.read_until(' Copyright 2001 H & H Technologies', 5)

                tn.write('\x1b2')
                checkpoint_str = "Select an EXTEND Menu"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.consolno_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                data[0] += tn.read_until('=Previous', 5)

                tn.write('bbulk')
                tn.write('\r')
                checkpoint_str = "Open/Update a Breakbulk File"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.consolno_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                data[0] += tn.read_until('=Fast Path', 5)

                tn.write('21')
                tn.write('\r')

                for each_mawb in mawb.split(","):
                    checkpoint_str = "House B/Lading"
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.consolno_checkpoint_database(checkpoint_str, each_mawb.strip("'"))
                        return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                    data[0] += tn.read_until('=House Bill Review', 5)

                    fomatted_mawb = each_mawb.strip("'").replace("-", "")[:11]
                    tn.write('\t\t\t\t\t\t')
                    tn.write(fomatted_mawb)
                    tn.write('\r')
                    checkpoint_str = fomatted_mawb
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        self.consolno_checkpoint_database(checkpoint_str, each_mawb.strip("'"))
                        continue

                    checkpoint_str = "Cust. Ref.:\x1b[0m " + fomatted_mawb
                    if not self.checkpoint(data, checkpoint_str, tn, 5):
                        #self.consolno_checkpoint_database(checkpoint_str, mawb)
                        #return "Unable to reach checkpoint : 3-'" + checkpoint_str + "'"
                        query = "UPDATE ADROIT.process_it_mawbdetail SET consoleNumber=111111,getConsoleStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                        #if(self.get_results(query) == 0):
                        #    return "Same status in database or Mawb not exist in database!"
                        #continue
                        #return "Console no. Not found"
                    #print "--", data[0].rsplit(" ", 21)
                    splitted_str = data[0].rsplit(" ", 21)
                    consol_num = splitted_str[5]
                    branch_code = splitted_str[2]
                    #print "==", splitted_str
                    #print "---" + consol_num + "__" + branch_code
                    if branch_code == "J2":
                        #return data[0] + "____" + data[0].rsplit(" ", 21)[5]
                        query = "UPDATE ADROIT.process_it_mawbdetail SET consoleNumber=" + consol_num + ", getConsoleStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                        if not self.get_results(query):
                            return "some Problem in querying the database..aborting, Unable to retch Branch: J2 !"
                            
                    elif branch_code == "J6":
                        query = "UPDATE ADROIT.process_it_mawbdetail SET consoleNumber=" + consol_num + ", getConsoleStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                        if not self.get_results(query):
                            return "some Problem in querying the database..aborting, Unable to retch Branch: J6 !"
                            
                    else:
                        query = "UPDATE ADROIT.process_it_mawbdetail SET consoleNumber=111111,getConsoleStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                        if not self.get_results(query):
                            return "some Problem in querying the database..aborting, Unable to create AI file!"

                    tn.write('\x1b[24~')
                tn.close();
            #self._db.close()
            return "Updated in database!"
        except:
            return "Some: problem at fetching console # server..pls try after some time!! ( Notify sys admin if this persist for a long)"

        
        
        
    def hawb_count(self, username="", password="", remark="", console_no="", test_update="", mawb="", itinfo=""):
        try:
            if not self.check_access():
                return "Not authorized IP"


            username = str(cherrypy.request.body.params['username']).strip()
            password = str(cherrypy.request.body.params['password']).strip()
            mawb = str(cherrypy.request.body.params['mawb']).rstrip(",").replace(',', "','")
            console_no = str(cherrypy.request.body.params['console_no']).rstrip(",").replace("','", ",")
            test_update = str(cherrypy.request.body.params['test_update']).strip()

       
            print "-----------------------------------------------------------------------------------"
            print 'username: ',username
            print 'password: ',password
            print 'mawb: ',mawb
            print 'console_n: ',console_no
            print 'test_update: ',test_update
            print "-----------------------------------------------------------------------------------"

#            import pdb;
#            pdb.set_trace()
            
            if username == "" or password == "" or console_no == "" or mawb == "":
                return "Not enough data! contact the admin"
                pass
            else:
                #return "udate rematrks"
                query = "UPDATE process_it_mawbdetail SET updateRemarksDesc='Started', updateRemarkStatus=1 WHERE mawbNum IN ('" + mawb + "')"
                if not self.get_results(query):
                    return "some Problem in querying the database..aborting, Unable to fetch HBL count !"

                if test_update == '1':
                    HOST = "10.1.16.105"    # test
                else:
                    HOST = "57.33.98.226"  # live

                PORT = 23
                data = [""]   # <a onclick='history.back();'>Go back and create another AI file</a></script>"
                username = username     # ''
                password = password     # ''
                tn = telnetlib.Telnet(HOST)
                tn.open(HOST, PORT)      # get logged in here
                tn.set_debuglevel(10)
                #print "opening--->",tn.read_untill()
                tn.write(username)
                checkpoint_str = "(C) COPYRIGHT IBM CORP. 1980, 2005"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.remarks_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint :(Login Screen) '" + checkpoint_str + "'"
                    
                tn.write('\t')
                tn.write(password)
                
                tn.write('\r')
                testData = tn.read_until("F12=Cancel", 5)
                testData = self.renderScreen(testData,0)
                print testData
                if testData.find('Display Program Messages')==-1:      #False
                    return "Unable to reach checkpoint 1."
                   
                tn.write('\r')
                
                testData = tn.read_until("F12=Cancel", 5)
                testData = self.renderScreen(testData,0)
                print testData
                
                tn.write('\r')
                testData = tn.read_until("Technologies", 5)
                testData = self.renderScreen(testData,0)
                print testData

                if testData.find('Master Applications Menu')==-1:      #False
                    self.remarks_checkpoint_database("Master Applications Menu", mawb)
                    return "Unable to reach checkpoint : Master Applications Menu"

                tn.write('\x1b2')# F2
                testData = tn.read_until("F3=Exit", 5)
                testData = self.renderScreen(testData,0)
                #print testData

                tn.write('bbulk')
                tn.write('\r')
                testData = tn.read_until("F3=Exit", 5)
                testData = self.renderScreen(testData,0)
                print testData
                if testData.find('BREAKBULK MASTER MENU')==-1:      #False
                    return "Unable to reach checkpoint : BREAKBULK MASTER MENU"                

                tn.write('1')
                tn.write('\r')
                testData = tn.read_until("F11=Pull From CSI", 5)
                testData = self.renderScreen(testData,0)
                print testData
                branch_code=testData[testData.find('Branch:')+8:testData.find('Branch:')+10]
                #print '>>>>>>>>>',branch_code,"<<<<<<<<<<"
                if testData.find('Break Bulk Master')==-1:      #False
                    return "Unable to reach checkpoint : Enter Consolidation No:______ \n\t Branch: '" + branch_code + "'"               

                mawbs = mawb.split(",")
                consoles = console_no.split(",")
                for i in xrange(len(mawbs)):
                    each_mawb = mawbs[i]
                    each_consol = consoles[i]
                    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",each_consol
                             
                    tn.write(each_consol)
                    tn.write('\r')
                    testData = tn.read_until("F20=Check Now", 5)
                    testData = self.renderScreen(testData,0)
                    print testData                    
                    
                    if testData.find('Break Bulk Master')==-1:      #False
                        return "Unable to reach checkpoint : Master Main Screen"     
                        
                    hawbNum=testData[testData.find('House Bills:')+12:testData.find('House Bills:')+18]
                    hawbNum=hawbNum.strip(' ')
                    print testData
                    #print '>>>>>>>>>',hawbNum,"<<<<<<<<<<"
                    
                    query = "UPDATE ADROIT.process_it_mawbdetail SET oneFStatus=" + hawbNum + " WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                    if not self.get_results(query):
                        return "some Problem in querying the database..aborting, Unable to create AI file!"

                    tn.write('\x1b[24~')
                tn.close            
            return "Done, Updated in database!"
        except:
            return "Some problem in updating remarks at server..pls try after some time!! ( Notify sys admin if this persist for a long)"      

            
            
        
    def fnb_process(self, username="", password="", console_no="", test_update="", mawb="", sendStation=""):
        if True:
            if not self.check_access():
                return "Not authorized IP"

            username = str(cherrypy.request.body.params['username']).strip()
            password = str(cherrypy.request.body.params['password']).strip()
            mawb = str(cherrypy.request.body.params['mawb']).rstrip(",").replace(',', "','")
            console_no = str(cherrypy.request.body.params['console_no']).rstrip(",").replace("','", ",")
            test_update = str(cherrypy.request.body.params['test_update']).strip()
            station = str(cherrypy.request.body.params['sendStation']).strip()

            print "-----------------------------------------------------------------------------------"
            print 'username: ',username
            print 'password: ',password
            print 'mawb: ',mawb
            print 'console_n: ',console_no
            print 'test_update: ',test_update
            print "station: ",station
            print "-----------------------------------------------------------------------------------"

#            import pdb;
#            pdb.set_trace()
            
            if username == "" or password == "" or console_no == "" or mawb == "":
                return "Not enough data! contact the admin"
                pass
            else:
                #return "udate rematrks"
                query = "UPDATE process_it_mawbdetail SET updateRemarksDesc='Started', updateRemarkStatus=1 WHERE mawbNum IN ('" + mawb + "')"
                if not self.get_results(query):
                    return "some Problem in querying the database..aborting, Unable to fetch FNB file!"


                PORT = 23
                data = [""]   # <a onclick='history.back();'>Go back and create another AI file</a></script>"
                username = username     # 
                password = password     # 
                tn = telnetlib.Telnet(HOST)
                tn.open(HOST, PORT)      # get logged in here
                tn.set_debuglevel(10)
                #print "opening--->",tn.read_untill()
                tn.write(username)
                checkpoint_str = "(C) COPYRIGHT IBM CORP. 1980, 2005"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.remarks_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint :(Login Screen) '" + checkpoint_str + "'"
                    
                tn.write('\t')
                tn.write(password)
                
                tn.write('\r')
                testData = tn.read_until("F12=Cancel", 5)
                testData = self.renderScreen(testData,0)
                print testData
                if testData.find('Display Program Messages')==-1:      #False
                    return "Unable to reach checkpoint 1."
                   
                tn.write('\r')
                
                testData = tn.read_until("F12=Cancel", 5)
                testData = self.renderScreen(testData,0)
                print testData
                
                tn.write('\r')
                testData = tn.read_until("Technologies", 5)
                testData = self.renderScreen(testData,0)
                print testData

                if testData.find('Master Applications Menu')==-1:      #False
                    self.remarks_checkpoint_database("Master Applications Menu", mawb)
                    return "Unable to reach checkpoint : Master Applications Menu"

                tn.write('\x1b2')# F2
                testData = tn.read_until("F3=Exit", 5)
                testData = self.renderScreen(testData,0)
                #print testData

                tn.write('bbulk')
                tn.write('\r')
                testData = tn.read_until("F3=Exit", 5)
                testData = self.renderScreen(testData,0)
                print testData
                if testData.find('BREAKBULK MASTER MENU')==-1:      #False
                    return "Unable to reach checkpoint : BREAKBULK MASTER MENU"                

                tn.write('1')
                tn.write('\r')
                testData = tn.read_until("F11=Pull From CSI", 5)
                testData = self.renderScreen(testData,0)
                print testData
                branch_code=testData[testData.find('Branch:')+8:testData.find('Branch:')+10]
                #print '>>>>>>>>>',branch_code,"<<<<<<<<<<"
                if testData.find('Break Bulk Master')==-1:      #False
                    return "Unable to reach checkpoint : Enter Consolidation No:______ \n\t Branch: '" + branch_code + "'"               

                mawbs = mawb.split(",")
                consoles = console_no.split(",")
                for i in xrange(len(mawbs)):
                    each_mawb = mawbs[i]
                    each_consol = consoles[i]
                    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",each_consol
                             
                    tn.write(each_consol)
                    tn.write('\r')
                    testData = tn.read_until("F20=Check Now", 5)
                    testData = self.renderScreen(testData,0)
                    print testData                    

                    
                    if testData.find('Break Bulk Master')==-1:      #False
                        return "Unable to reach checkpoint : Master Main Screen"     
                        

                    fnb=testData[testData.find('Invoice:')+8:testData.find('Invoice:')+80]
                    fnb=fnb.strip(' ')

#                    print '>>>>>>>>>',fnb,"<<<<<<<<<<"


                    if (station=="DFW"):
                        if fnb.find("AGD")!=-1:
                            print "Processed"
                            fnbStatus = "Processed"
                        else:
                            print "Not Processed"
                            fnbStatus = "Not Processed"
                    else:
                        if fnb.find("AGX")!=-1:
                            print "Processed"
                            fnbStatus="Processed"
                        else:
                            print "Not Processed"
                            fnbStatus="Not Processed"


                    query = "UPDATE ADROIT.process_it_mawbdetail SET spProStatus='" + fnbStatus + "' WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                    if not self.get_results(query):
                        return "ABORT: Some Problem in querying the database, Unable to Fetch FBN Process Status!"
                    
                    tn.write('\x1b[24~')
                tn.close            
            return "Done, Updated in database!"
        else:
            return "Some problem in updating remarks at server..pls try after some time!! ( Notify sys admin if this persist for a long)"      
	  
        
        
        
        
    def fetch_flightEta(self, username="", password="", console_no="", test_update="", mawb=""):
        if True:
            if not self.check_access():
                return "Not authorized IP"

            username = str(cherrypy.request.body.params['username']).strip()
            password = str(cherrypy.request.body.params['password']).strip()
            mawb = str(cherrypy.request.body.params['mawb']).rstrip(",").replace(',', "','")
            console_no = str(cherrypy.request.body.params['console_no']).rstrip(",").replace("','", ",")
            test_update = str(cherrypy.request.body.params['test_update']).strip()
 #           station = str(cherrypy.request.body.params['sendStation']).strip()
            
            print "-----------------------------------------------------------------------------------"
            print 'username: ',username
            print 'password: ',password
            print 'mawb: ',mawb
            print 'console_n: ',console_no
            print 'test_update: ',test_update
 #           print "station: ",station
            print "-----------------------------------------------------------------------------------"

#            import pdb;
#            pdb.set_trace()
            
            if username == "" or password == "" or console_no == "" or mawb == "":
                return "Not enough data! contact the admin"
                pass
            else:
                #return "udate rematrks"
                query = "UPDATE process_it_mawbdetail SET updateRemarksDesc='Started', updateRemarkStatus=1 WHERE mawbNum IN ('" + mawb + "')"
                if not self.get_results(query):
                    return "some Problem in querying the database..aborting, Unable to fetch FNB file!"

                if test_update == '1':
                    HOST = "10.1.16.105"    # test
                else:
                    HOST = "57.33.98.226"  # live

                PORT = 23
                data = [""]   # <a onclick='history.back();'>Go back and create another AI file</a></script>"
                username = username     # 'IAHAEKZB'
                password = password     # 'GENERAL5'
                tn = telnetlib.Telnet(HOST)
                tn.open(HOST, PORT)      # get logged in here
                tn.set_debuglevel(10)
                #print "opening--->",tn.read_untill()
                tn.write(username)
                checkpoint_str = "(C) COPYRIGHT IBM CORP. 1980, 2005"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.remarks_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint :(Login Screen) '" + checkpoint_str + "'"
                    
                tn.write('\t')
                tn.write(password)
                
                tn.write('\r')
                testData = tn.read_until("F12=Cancel", 5)
                testData = self.renderScreen(testData,0)
                print testData
                if testData.find('Display Program Messages')==-1:      #False
                    return "Unable to reach checkpoint 1."
                   
                tn.write('\r')
                
                testData = tn.read_until("F12=Cancel", 5)
                testData = self.renderScreen(testData,0)
                print testData
                
                tn.write('\r')
                testData = tn.read_until("Technologies", 5)
                testData = self.renderScreen(testData,0)
                print testData

                if testData.find('Master Applications Menu')==-1:      #False
                    self.remarks_checkpoint_database("Master Applications Menu", mawb)
                    return "Unable to reach checkpoint : Master Applications Menu"

                tn.write('\x1b2')# F2
                testData = tn.read_until("F3=Exit", 5)
                testData = self.renderScreen(testData,0)
                #print testData

                tn.write('bbulk')
                tn.write('\r')
                testData = tn.read_until("F3=Exit", 5)
                testData = self.renderScreen(testData,0)
                print testData
                if testData.find('BREAKBULK MASTER MENU')==-1:      #False
                    return "Unable to reach checkpoint : BREAKBULK MASTER MENU"                

                tn.write('1')
                tn.write('\r')
                testData = tn.read_until("F11=Pull From CSI", 5)
                testData = self.renderScreen(testData,0)
                print testData
                branch_code=testData[testData.find('Branch:')+8:testData.find('Branch:')+10]
                #print '>>>>>>>>>',branch_code,"<<<<<<<<<<"
                if testData.find('Break Bulk Master')==-1:      #False
                    return "Unable to reach checkpoint : Enter Consolidation No:______ \n\t Branch: '" + branch_code + "'"               

                mawbs = mawb.split(",")
                consoles = console_no.split(",")
                for i in xrange(len(mawbs)):
                    each_mawb = mawbs[i]
                    each_consol = consoles[i]
                    #print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",each_consol
                             
                    tn.write(each_consol)
                    tn.write('\r')
                    testData = tn.read_until("F20=Check Now", 5)
                    testData = self.renderScreen(testData,0)
                    
                    print "========================================="
                    print testData      
                    print "=========================================="
                                        
                    if testData.find('Break Bulk Master')==-1:      #False
                        return "Unable to reach checkpoint : Master Main Screen"     

                    flightCode=testData[testData.find('Carrier:')+9:testData.find('Carrier:')+11]
                    flightNum=testData[testData.find('Plane#:')+12:testData.find('Plane#:')+16]
                    try:
                        etaDate=testData[testData.find("Arr Dte/Tm:")+14:testData.find("Arr Dte/Tm:")+22]
                        etaDate=etaDate.replace('/','-').strip(' ')
                        etaDate= datetime.datetime.strptime(etaDate.strip(' '), '%m-%d-%y')
                        etaDate=etaDate.strftime('%Y-%m-%d')
                    except:
                        etaDate=" "
                    try:
                        etaTime=testData[testData.find("Arr Dte/Tm:")+23:testData.find("Arr Dte/Tm:")+27]
                        etaTime=etaTime.strip(' ')
                        etaTime=datetime.datetime.strptime(etaTime.strip(' '), "%H%M")
                        etaTime=etaTime.strftime("%H:%M:00")
                    except:
                        etaTime=" "

                  
                    query = "UPDATE ADROIT.process_it_mawbdetail SET flightCode='" + flightCode + "' ,flightNum='"+flightNum+"',etaDate='"+etaDate+"',etaTime='"+etaTime+"'  WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                    print ">>>>>>>",query
                    if not self.get_results(query):
                        return "ABORT: Some Problem in querying the database, Unable to Fetch FBN Process Status!"
                    
                    tn.write('\x1b[24~')
                tn.close            
            return "Done, Updated in database!"
        else:
            return "Some problem in updating remarks at server..pls try after some time!! ( Notify sys admin if this persist for a long)"      
	      
          
          
         
    
        
    def master_wright(self, username="", password="", console_no="", test_update="", mawb="", flightCode="", flightNum="", etaDate="", etaTime="", des_station=""):
        if True:
            if not self.check_access():
                return "Not authorized IP"

            username = str(cherrypy.request.body.params['username']).strip()
            password = str(cherrypy.request.body.params['password']).strip()
            mawb = str(cherrypy.request.body.params['mawb']).rstrip(",").replace(',', "','")
            console_no = str(cherrypy.request.body.params['console_no']).rstrip(",").replace("','", ",")
            test_update = str(cherrypy.request.body.params['test_update']).strip()
            
            flightCode = str(cherrypy.request.body.params['flightCode']).strip()
            flightNum = str(cherrypy.request.body.params['flightNum']).strip()
            etaDate = str(cherrypy.request.body.params['etaDate']).strip()
            etaTime = str(cherrypy.request.body.params['etaTime']).strip()
            des_station = str(cherrypy.request.body.params['des_station']).strip()
            
            
            print "-----------------------------------------------------------------------------------"
            print 'username: ',username
            print 'password: ',password
            print 'mawb: ',mawb
            print 'console_n: ',console_no
            print 'test_update: ',test_update
            
            print "flightCode: ",flightCode
            print "flightNum: ",flightNum
            print "etaDate: ",etaDate
            print "etaTime: ",etaTime
            print "des_station: ",des_station

            print "-----------------------------------------------------------------------------------"


            
            if username == "" or password == "" or console_no == "" or mawb == "" or flightCode == "" or flightNum == "" or etaDate =="" or etaTime == "" or des_station == "":
                return "Not enough data! "
                pass
            else:
                #return "udate rematrks"
                query = "UPDATE process_it_mawbdetail SET updateRemarksDesc='Started', updateRemarkStatus=1 WHERE mawbNum IN ('" + mawb + "')"
                if not self.get_results(query):
                    return "some Problem in querying the database..aborting, Unable to fetch FNB file!"

                if test_update == '1':
                    HOST = "10.1.16.105"    # test
                else:
                    HOST = "57.33.98.226"  # live

                PORT = 23
                data = [""]   # <a onclick='history.back();'>Go back and create another AI file</a></script>"
                username = username     # 'IAHAEKZB'
                password = password     # 'GENERAL5'
                tn = telnetlib.Telnet(HOST)
                tn.open(HOST, PORT)      # get logged in here
                tn.set_debuglevel(10)
                #print "opening--->",tn.read_untill()
                tn.write(username)
                checkpoint_str = "(C) COPYRIGHT IBM CORP. 1980, 2005"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    self.remarks_checkpoint_database(checkpoint_str, mawb)
                    return "Unable to reach checkpoint :(Login Screen) '" + checkpoint_str + "'"
                    
                tn.write('\t')
                tn.write(password)
                
                tn.write('\r')
                testData = tn.read_until("F12=Cancel", 5)
                testData = self.renderScreen(testData,0)
                print testData
                if testData.find('Display Program Messages')==-1:      #False
                    return "Unable to reach checkpoint 1."
                   
                tn.write('\r')
                
                testData = tn.read_until("F12=Cancel", 5)
                testData = self.renderScreen(testData,0)
                print testData
                
                tn.write('\r')
                testData = tn.read_until("Technologies", 5)
                testData = self.renderScreen(testData,0)
                print testData

                if testData.find('Master Applications Menu')==-1:      #False
                    self.remarks_checkpoint_database("Master Applications Menu", mawb)
                    return "Unable to reach checkpoint : Master Applications Menu"

                tn.write('\x1b2')# F2
                testData = tn.read_until("F3=Exit", 5)
                testData = self.renderScreen(testData,0)
                #print testData

                tn.write('bbulk')
                tn.write('\r')
                testData = tn.read_until("F3=Exit", 5)
                testData = self.renderScreen(testData,0)
                print testData
                if testData.find('BREAKBULK MASTER MENU')==-1:      #False
                    return "Unable to reach checkpoint : BREAKBULK MASTER MENU"                

                tn.write('1')
                tn.write('\r')
                testData = tn.read_until("F11=Pull From CSI", 5)
                testData = self.renderScreen(testData,0)
                print testData
                
                branch_code=testData[testData.find('Branch:')+8:testData.find('Branch:')+10]
                if testData.find('Break Bulk Master')==-1:      #False
                    return "Unable to reach checkpoint : Enter Consolidation No:______ \n\t Branch: '" + branch_code + "'"               

                mawbs = mawb.split(",")
                consoles = console_no.split(",")
                flightC= flightCode.split(",")
                flightN= flightNum.split(",")
                etaD= etaDate.split(",")
                etaT= etaTime.split(",")
                
 
                    
                for i in xrange(len(mawbs)):
                    each_mawb = mawbs[i]
                    each_consol = consoles[i]
                    each_flightC = flightC[i]
                    each_flightN = flightN[i]
                    
                    if len(each_flightN) == 3:
                        each_flightN=each_flightN+" "
                    
                    
                    each_etaD = etaD[i]
                    each_etaD = each_etaD.replace("-","/")
                    each_etaD15 = (datetime.datetime.strptime(each_etaD.replace("/",""), "%m%d%y").date()+relativedelta(days=+15)).strftime('%m/%d/%y')
                    each_etaD3 = (datetime.datetime.strptime(each_etaD.replace("/",""), "%m%d%y").date()+relativedelta(days=+3)).strftime('%m/%d/%y')
                    each_etaD1 = (datetime.datetime.strptime(each_etaD.replace("/",""), "%m%d%y").date()+relativedelta(days=+1)).strftime('%m/%d/%y')
                    each_etaD_1 = (datetime.datetime.strptime(each_etaD.replace("/",""), "%m%d%y").date()+relativedelta(days=-1)).strftime('%m/%d/%y')
                    
                    #each_etaD_List = (datetime.datetime.strptime(each_etaD.replace("/",""), "%m%d%y").date()+relativedelta(days=+2)).strftime('%m/%d/%y')
                    each_etaD_P2 = datetime.datetime.strptime(each_etaD.replace("/",""), "%m%d%y").date()
                    #today=datetime.datetime.today()
                    freeExpDay= each_etaD_P2.isoweekday()
                    
                    if freeExpDay == 5 :
                        #print "sat/sun","[",freeExpDay,"]"
                        each_etaD_List= each_etaD_P2+relativedelta(days=+4)
                        each_etaD_List=each_etaD_List.strftime('%m/%d/%y')                        
                        #print "[",each_etaD_List,"]"," [",freeExpDay,"]","::--",each_etaD_List.isoweekday()    
                    elif freeExpDay == 6 :
                        #print "sat/sun","[",freeExpDay,"]"
                        each_etaD_List= each_etaD_P2+relativedelta(days=+3)
                        each_etaD_List=each_etaD_List.strftime('%m/%d/%y')                        
                        #print "[",each_etaD_List,"]"," [",freeExpDay,"]","::--",each_etaD_List.isoweekday()
                    elif freeExpDay == 7 :
                        #print "sat/sun","[",freeExpDay,"]"
                        each_etaD_List= each_etaD_P2+relativedelta(days=+2)
                        each_etaD_List=each_etaD_List.strftime('%m/%d/%y')                        
                        #print "[",each_etaD_List,"]"," [",freeExpDay,"]","::--",each_etaD_List.isoweekday()
                    elif freeExpDay == 4:
                        each_etaD_List = each_etaD_P2+relativedelta(days=+4)
                        each_etaD_List=each_etaD_List.strftime('%m/%d/%y')                        
                        #print "[",each_etaD_List,"]"," [",freeExpDay,"]","::--",each_etaD_List.isoweekday()
                    else:
                        #print 'working days',"[",freeExpDay,"]"
                        each_etaD_List= each_etaD_P2+relativedelta(days=+2)
                        each_etaD_List=each_etaD_List.strftime('%m/%d/%y')
                        #print "[",each_etaD_List,"]"," [",freeExpDay,"]","::--"
                     
                    
                    each_etaT = etaT[i] 
                    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",each_consol
                    



                    
                    tn.write(each_consol)
                    testData = tn.read_until("F20=Check Now", 1)
                    testData = self.renderScreen(testData,0)
                    print testData 
                    
                    tn.write('\r')
                    
                    '''
                    testData = tn.read_until("F20=Check Now", 5)
                    testData = self.renderScreen(testData,0)
                    
                    print "========================================="
                    print testData      
                    print "=========================================="

                    if testData.find('Break Bulk Master')==-1:      #False
                        return "Unable to reach checkpoint : Master Main Screen for Consol: '" + each_consol + "'"  

                    '''    
                       
                   
                    if des_station == "LAX":
                        
                        testData = tn.read_until("F20=Check Now", 5)
                        testData = self.renderScreen(testData,1)
                        print '|'*50
                        print testData                    
                        print '|'*50   
                        if testData.find('Break Bulk Master')==-1:      #False
                            return "Unable to reach checkpoint : Master Main Screen for Consol: '" + each_consol + "'"  
                        
                        consolidator=(testData[testData.find('Consolidator:')+13:testData.find('Consolidator:')+20]).replace(" ","")
                        print ">>>>>>>>>>>>>>",consolidator,"<<<<<<<<<<<<<<<<<<<",each_consol
                        
                        
                        if consolidator == 'CNPVG':
                            tn.write('\t')             # 1 TAB
                            tn.write(each_flightC)                
                            tn.write('\t\t\t')        # 3 TAB
                            tn.write('CNSHA')                            
                            tn.write('\t')
                            tn.write(each_flightN) 
                            tn.write('\t\t\t\t\t')         # 8 TAB
                            tn.write('SHA')
                            tn.write('\t')                            
                            tn.write('SHA')                            
                            tn.write('\t')
                            tn.write('2720') 
                            tn.write('\t\t\t')           # 3 TAB
                            tn.write('2720') 
                            tn.write('\t\t')        # 2 TAB
                            tn.write('Z493')    
                            tn.write('\t\t\t\t\t\t')        # 6 TAB
                            tn.write('          0.01')   
                            tn.write('\t')
                            tn.write('P')                    
                            tn.write('\t\t\t')       # 5 TAB
                            tn.write("  "+each_etaD)   
                            tn.write('\t')            # 2 TAB   7/12/13  |   71213|
                            tn.write("  "+each_etaD)       
                            tn.write(each_etaT) 
                            tn.write("  "+each_etaD)       
                            tn.write("  "+each_etaD)    
                            tn.write("  "+each_etaD15)              # 15 days ++
                            tn.write("  "+each_etaD3)        # 3 days ++
                            
                        else:
                            tn.write('\t')             # 1 TAB
                            tn.write(each_flightC)                
                            tn.write('\t\t\t\t')        # 4 TAB
                            tn.write(each_flightN) 
                            tn.write('\t\t\t\t\t\t\t\t')         # 8 TAB
                            tn.write('2720') 
                            tn.write('\t\t\t')           # 3 TAB
                            tn.write('2720') 
                            tn.write('\t\t')        # 2 TAB
                            tn.write('Z493')    
                            tn.write('\t\t\t\t\t\t')        # 6 TAB
                            tn.write('          0.01')   
                            tn.write('\t')
                            tn.write('P')                    
                            tn.write('\t\t\t')       # 5 TAB
                            tn.write("  "+each_etaD)   
                            tn.write('\t')            # 2 TAB   7/12/13  |   71213|
                            tn.write("  "+each_etaD)       
                            tn.write(each_etaT) 
                            tn.write("  "+each_etaD)       
                            tn.write("  "+each_etaD)    
                            tn.write("  "+each_etaD15)              # 15 days ++
                            tn.write("  "+each_etaD3)        # 3 days ++
                            
                   
                        
                    elif des_station == "DFW":
                        tn.write('\t')             # 1 TAB
                        tn.write(each_flightC)                
                        tn.write('\t\t\t\t')        # 4 TAB
                        tn.write(each_flightN) 
                        tn.write('\t') 
                        tn.write(each_flightN) 
                        tn.write('\t\t\t\t\t\t\t')         # 8 TAB
                        tn.write('5501') 
                        
                        tn.write('\t') 
                        tn.write('DFW') 
                        
                        tn.write('\t')           # 1 TAB
                        tn.write('5501') 
                        tn.write('\t\t')        # 2 TAB
                        tn.write('V484')    
                        tn.write('\t\t\t\t\t\t')        # 6 TAB
                        tn.write('          0.01')   
                        tn.write('\t')
                        tn.write('P')                    
                        tn.write('\t\t\t')       # 5 TAB
                        tn.write("  "+each_etaD_1)   
                        tn.write('\t')            # 2 TAB   7/12/13  |   71213|
                        tn.write("  "+each_etaD)       
                        tn.write(each_etaT) 
                        tn.write("  "+each_etaD)       
                        tn.write("  "+each_etaD1)    
                        tn.write("\t")              # 15 days ++
                        tn.write("  "+str(each_etaD_List))        # 3 days ++
                     
                        
                    elif des_station == "IAH":
                        print "**********************",each_mawb;
                        selected_mawb = (each_mawb.replace(" ",""))[0:3]
                        if selected_mawb == '114' or selected_mawb == '117':
                            firm_code = 'V767'
                        elif selected_mawb == '125' or selected_mawb == '157':
                            firm_code = 'T694'
                        elif selected_mawb == '129':
                            firm_code = 'T018'
                        elif selected_mawb == '160' or selected_mawb == '172' or selected_mawb == '176' or selected_mawb == '043' or selected_mawb == '045' or selected_mawb == '065':
                            firm_code = 'V758'
                        elif selected_mawb == '180':
                            firm_code = 'V457'                            
                        elif selected_mawb == '275' or selected_mawb == '369' or selected_mawb == '549' or selected_mawb == '999' or selected_mawb == '053':
                            firm_code = 'U979'
                        elif selected_mawb == '297':
                            firm_code = 'V967'   
                        elif selected_mawb == '403' or selected_mawb == '020':
                            firm_code = 'S973'
                        elif selected_mawb == '406':
                            firm_code = 'S986'   
                        elif selected_mawb == '615':
                            firm_code = 'S678'   
                        elif selected_mawb == '618' or selected_mawb == '695':
                            firm_code = 'S146'   
                        elif selected_mawb == '988':
                            firm_code = 'V767'   
                        elif selected_mawb == '001':
                            firm_code = 'S983'   
                        elif selected_mawb == '002':
                            firm_code = 'U236'  
                        elif selected_mawb == '005':
                            firm_code = 'S984'   
                        elif selected_mawb == '006':
                            firm_code = 'S975'   
                        elif selected_mawb == '016':
                            firm_code = 'S984'   
                        elif selected_mawb == '023':
                            firm_code = 'U020'   
                        elif selected_mawb == '057':
                            firm_code = 'S987'   
                        elif selected_mawb == '074':
                            firm_code = 'S991'  
                              
                        tn.write('\t')             # 1 TAB
                        tn.write(each_flightC)                
                        tn.write('\t\t\t\t')        # 4 TAB
                        tn.write(each_flightN) 
                        tn.write('\t\t\t\t\t\t\t\t')         # 8 TAB
                        tn.write('5309') 
                        tn.write('\t') 
                        tn.write('IAH') 
                        tn.write('\t')           # 1 TAB
                        tn.write('5309') 
                        tn.write('\t\t')        # 2 TAB
                        
                        tn.write(firm_code)    
                        
                        tn.write('\t\t\t\t\t\t')        # 6 TAB
                        tn.write('          0.01')   
                        tn.write('\t')
                        tn.write('P')                    
                        tn.write('\t\t\t')       # 5 TAB
                        tn.write("  "+each_etaD_1)   
                        tn.write('\t')            # 2 TAB   7/12/13  |   71213|
                        tn.write("  "+each_etaD)       
                        tn.write(each_etaT) 
                        tn.write("  "+each_etaD)       
                        tn.write("  "+each_etaD1)    
                        tn.write("\t")              # 15 days ++
                        tn.write("  "+str(each_etaD_List))         # 3 days ++
      
      
      
 
                    tn.write('\r') 

                    
                    testData = tn.read_until("F9=File Lookup           F11=Pull From CSI", 5)
                    testData = self.renderScreen(testData,0)
                    print '*'*50
                    print testData                    
                    print '*'*50    
                    
                    error=(testData[testData.find("F20=Check Now")+15:-1]).strip(" ")
                    
                    if len(error)!=0:
                        if testData.find('Agent Country Code and Port Country Code do not agree')!=-1:      #False  
                            tn.write('\r') 
                        else:
                            return "Cannot Wright Console:"+each_consol+" \nError Message : "+error
                    
                    '''
                    if testData.find('Agent Country Code and Port Country Code do not agree')!=-1:      #False  
                        tn.write('\r') 
                    '''    
                    tn.write('\x1b[24~')                   
                   
                   
                   
                   
                tn.close            
            return "Done !!! \nData Successfully written on Break Bulk Master Screen"
        else:
            return "Some problem in updating remarks at server..pls try after some time!! ( Notify sys admin if this persist for a long)"      
	      
                
          
      
      
      
      
    create_ai_file.exposed = True
    update_remarks.exposed = True
    get_console_num.exposed = True
    hawb_count.exposed = True
    fnb_process.exposed = True
    fetch_flightEta.exposed = True
    master_wright.exposed = True

#tutconf = os.path.join('C:/Users/nikhil.mulik/Desktop/class_automation/tutorial2.conf')
tutconf = os.path.join(os.path.dirname(__file__), 'tutorial2.conf')



if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.config.update(tutconf)
    cherrypy.quickstart(FileDemo(), config=tutconf)

