# coding:utf-8

import sys
import json
import time
import mysql.connector
from flask import Flask, render_template, Blueprint, g, request, send_from_directory
import site_info_collect
from playsqlmap import start
from save_to_mysql import checkurl
import hashlib
import json

import importlib

importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

app = Blueprint("trace", __name__)
'''
@app.before_request
def before_request():
    g.conn=mysql.connector.connect(user='root',password='123456',host='localhost',database='TDScan')
    g.cur=g.conn.cursor()


@app.teardown_request
def tear_down(response):
    g.conn.close()
    return response
'''


#@app.route("/trace", methods=['GET', 'POST'])
def trace(target):

    try:
        result_infos = {}
        #target = request.form["target"]
        #target = "https://www.google.com/maps"
        print("targe",target)
        target_urllist, iplist, collect_dirs, collect_ports, subdomain ,dns_content, differnet_dsn ,hashid = site_info_collect.runscan(target)
        print("target_urllist",target_urllist)
        # urla = checkurl(target)
        # id = hashlib.md5()
        # id.update(urla)
        # siteid = id.hexdigest()
        # print "sql_hash:" + siteid

        #print hashid

        for url in target_urllist[0:10:1]:
            print ("checksql_url：",url)
            start(hashid, url)
            time.sleep(0.3)
    except:
        pass

    data = {
        "target_urllist":target_urllist,
        "iplist":iplist,
        "collect_dirs":collect_dirs,
        "collect_ports":collect_ports,
        "subdomain":subdomain,
        "dns_content":dns_content,
        "differnet_dsn":differnet_dsn

    }

    #target_urllist, iplist, collect_dirs, collect_ports, subdomain = 'abc', 'abc', 'abc', 'abc', 'abc'

    # return render_template("trace.html", target=target, target_urllist=target_urllist, iplist=iplist,
    #                         collect_dirs=collect_dirs, collect_ports=collect_ports, subdomain=subdomain)
    return json.dumps(data)

# return render_template("trace.html")

