'''
Created on Sep 28, 2012

@author: avinash.keshri
# -*- coding: utf-8 -*-
'''
#import cherrypy
import MySQLdb
#from datetime import date
import telnetlib
#import time
import os
#import re
#import sys


localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)


class Class_wp_automation(object):

    def __init__(self):
        self._db = MySQLdb.connect()
        self._cursor = self._db.cursor()    

    def get_results(self, query):
        # query = "UPDATE process_it_mawbdetail SET createAIDesc='1st page', createAIStatus=1 WHERE mawbNum='" + mawb + "'"
        print "Query-->", query
        #return True
        try:
            # Execute the SQL command
            self._cursor.execute(query)
            self._db.commit()
            #   print row
        except:
            self._db.rollback()
            return False
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

    def consolno_checkpoint_database(self, checkpoint_str, mawb):
        query = "UPDATE process_it_mawbdetail SET getConsoleDesc='Unable to reach checkpoint -" + checkpoint_str + " ', getConsoleStatus=2  WHERE mawbNum IN ('" + mawb + "')"
        return True
        if not self.get_results(query):
            return "some Problem in querying the database..aborting, Unable to create AI file!"
        pass

    def get_console_num(self):
        if True:
            query = "SELECT mawbNum FROM process_it_mawbdetail WHERE consoleNumber IS NULL LIMIT 2;"
            if not self.get_results(query):
                return "some Problem in querying the database..aborting!"
            
            results = self._cursor.fetchall()
            fetched_data = ""
            mawb = ""
            test_update = '0'
            for row in results:
               mawb += "'" + row[0] + "',"
               #print row[0]
            
            #print "---",mawb
            mawb = mawb.rstrip(",")
            for each_mawb in mawb.split(","): 
                print "each_mawb:",each_mawb.strip("'")
                fomatted_mawb = each_mawb.strip("'").replace("-", "")[:11] 
                print "fomatted_mawb:",fomatted_mawb
            '''
            query = "UPDATE process_it_mawbdetaild ds SET getConsoleStatus=1 WHERE mawbNum IN ('" + mawb + "')"
            if not self.get_results(query):
                return "some Problem in querying the database..aborting!"
            '''
            #return "Ai file done"

            #HOST = "57.33.98.226"  # live
            if test_update == '1':
                HOST = ""    # test
            else:
                HOST = ""  # live

            PORT = 23
            data = [""]
            username = ""     # 'IAHAEKZB'
            password = ""     # 'GENERAL5'
            tn = telnetlib.Telnet(HOST)
            tn.open(HOST, PORT)      # get logged in here
            #tn.set_debuglevel(10)
            #print "opening--->",tn.read_untill()
            tn.write(username)
            checkpoint_str = "(C) COPYRIGHT IBM CORP. 1980, 2005"
            if not self.checkpoint(data, checkpoint_str, tn, 5):
                #self.consolno_checkpoint_database(checkpoint_str, mawb)
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
                    #self.consolno_checkpoint_database(checkpoint_str, mawb)
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
                #self.consolno_checkpoint_database(checkpoint_str, mawb)
                return "Unable to reach checkpoint : '" + checkpoint_str + "', please recheck userid and passwd!"
            data[0] += tn.read_until('IBM AT&T Brokerage', 5)
            data[0] += tn.read_until('=Fast Path', 5)
            data[0] += tn.read_until(' Copyright 2001 H & H Technologies', 5)

            tn.write('\x1b2')
            checkpoint_str = "Select an EXTEND Menu"
            if not self.checkpoint(data, checkpoint_str, tn, 5):
                #self.consolno_checkpoint_database(checkpoint_str, mawb)
                return "Unable to reach checkpoint : '" + checkpoint_str + "'"
            data[0] += tn.read_until('=Previous', 5)

            tn.write('bbulk')
            tn.write('\r')
            checkpoint_str = "Open/Update a Breakbulk File"
            if not self.checkpoint(data, checkpoint_str, tn, 5):
                #self.consolno_checkpoint_database(checkpoint_str, mawb)
                return "Unable to reach checkpoint : '" + checkpoint_str + "'"
            data[0] += tn.read_until('=Fast Path', 5)

            tn.write('21')
            tn.write('\r')

            for each_mawb in mawb.split(","):       #mawb will be ['111-2313233','111-2313233','111-2313233']
                checkpoint_str = "House B/Lading"
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    #self.consolno_checkpoint_database(checkpoint_str, each_mawb.strip("'"))   #each mawb will be 111-2313233
                    return "Unable to reach checkpoint : '" + checkpoint_str + "'"
                data[0] += tn.read_until('=House Bill Review', 5)

                fomatted_mawb = each_mawb.strip("'").replace("-", "")[:11]      #each mawb will be 111-2313233->1112313233  or 111-2313233B ->1112313233
                tn.write('\t\t\t\t\t\t')
                tn.write(fomatted_mawb)
                tn.write('\r')
                checkpoint_str = fomatted_mawb
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    #self.consolno_checkpoint_database(checkpoint_str, each_mawb.strip("'"))
                    continue

                checkpoint_str = "Cust. Ref.:\x1b[0m " + fomatted_mawb
                if not self.checkpoint(data, checkpoint_str, tn, 5):
                    #self.consolno_checkpoint_database(checkpoint_str, mawb)
                    #return "Unable to reach checkpoint : 3-'" + checkpoint_str + "'"
                    query = "UPDATE process_it_mawbdetail SET consoleNumber=111111,getConsoleStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                    #if(self.get_results(query) == 0):
                    #    return "Same status in database or Mawb not exist in database!"
                    #continue
                    #return "Console no. Not found"
                #print "--", data[0].rsplit(" ", 21)
                splitted_str = data[0].rsplit(" ", 21)
                consol_num = splitted_str[5]
                branch_code = splitted_str[2]
                #print "==", splitted_str
                #print "===" + each_mawb.strip("'") + "---" + consol_num + "__" + branch_code
                fetched_data += each_mawb.strip("'") + "=" + consol_num + "\n"
                if branch_code == "J2":
                    #return data[0] + "____" + data[0].rsplit(" ", 21)[5]
                    query = "UPDATE process_it_mawbdetail SET consoleNumber=" + consol_num + ", getConsoleStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                    #if not self.get_results(query):
                    #   return "some Problem in querying the database..aborting, Unable to create AI file!"
                else:
                    query = "UPDATE process_it_mawbdetail SET consoleNumber=111111,getConsoleStatus=3 WHERE mawbNum IN ('" + each_mawb.strip("'") + "')"
                    #if not self.get_results(query):
                    #    return "some Problem in querying the database..aborting, Unable to create AI file!"

                tn.write('\x1b[24~')
            print "Total data=",fetched_data
            return "Updated in database!"
        else:
            return "Some problem in server pls contact sys admin!!"
    

if __name__ == '__main__':
    ob = Class_wp_automation()
    print "=>",ob.get_console_num()
'''
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(FileDemo(), config=tutconf)
'''

