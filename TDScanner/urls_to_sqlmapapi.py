# -*- coding: utf-8 -*-
# @Site    : www.TDScan.org


import urllib
import urllib.request
import json
import time
import os
def run_server():
    os.system('python /Users/xysoul/Tools/sqlmap/sqlmapapi.py -s -p 8080' )
    pass

def creat_task():
    try:
        url = 'http://127.0.0.1:8080/task/new'
        response = urllib.request.urlopen(url)
        jdata = json.loads(response.read())
        taskid = str(jdata['taskid'])
        print ("taskid:", taskid)

    except:
        pass
    return taskid

def viewtask(taskid):
        url='http://127.0.0.1:8080/scan/'+taskid+'/log'
        response = urllib.request.urlopen(url)
        return response.read()
def viewdata(taskid):
        url='http://127.0.0.1:8080/scan/'+taskid+'/data'
        response = urllib.request.urlopen(url)
        return response.read()
def task_start(taskid,url):
    try:
        url1='http://127.0.0.1:8080/scan/'+taskid+'/start'
        value ={'url':url}
        i_headers = {'Content-Type':'application/json'}
        jdata = json.dumps(value)
        req = urllib.request.Request(url1, jdata)
        response = urllib.request.Request(req)
        #print "response:",response.read()
    except:
        pass
        return response.read()
def get_status(taskid):
        url='http://127.0.0.1:8080/scan/'+taskid+'/status'
        response = urllib.request.urlopen(url)
        return response.read()

#print task_start(taskid,'http://www.hrbgtj.gov.cn/vote_result.jspx?voteId=20')




