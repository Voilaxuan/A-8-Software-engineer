import socket
import threading
import urllib.request
import urllib.error
import re
import sys
from bs4 import BeautifulSoup

import manager
import net_explore
import save_to_mysql
import dirfuzz
from site_port_check import portScan
import time
import os
import importlib
urllist =[]
iplist =[]


importlib.reload(sys)

#sys.setdefaultencoding('utf-8')
def get_url(body_text):

        soup=BeautifulSoup(body_text,"html.parser")
        links=soup.findAll('a')
        for link in links:
            url =link.get('href')
            try:
                if '?' in str(url):
                    urllist.append(url)
            except:
                pass


def get_ip(body_text):
    body_text=body_text.replace(" ","")
    #match all ip address
    ips=re.findall(r"\d+\.\d+\.\d+\.\d+",body_text,re.I)
    for i in ips:
        iplist.append(i)
def get_post(body_text):
    pass
def get(target_url):
    try:
        #i_headers_1 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48','Upgrade-Insecure-Requests':'1','Referer':'http://toutiao.com/m5573658957/'}
        i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48','Upgrade-Insecure-Requests':'1','Referer':'https: // google.com'}


        #print "get_ok1"

        #req = urllib.Request(target_url,headers=i_headers)
        #print "get_ok2"
        #body_text=urllib.urlopen(req).read()
        #print "get_ok3"


        req = urllib.request.Request(target_url, headers=i_headers)
        response = urllib.request.urlopen(req)
        body_text = response.read().decode('utf-8')

    except Exception as e:
        print(e)
        pass
    return body_text

def subdomainapi(target_url):
    if 'www' in target_url:
        try:
            subdomain = []
            target_url = target_url.strip('http:').strip('/').strip('www.')
            api = 'http://i.links.cn/subdomain/'+target_url+'.html'
            i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
            req = urllib.request.Request(api,headers=i_headers)
            response = urllib.request.urlopen(req)
            body_text=response.read.decode("utf-8")
            print("subdomain")
            print(api)
            body_text = get(api)
            print("body_text",body_text)
            soup=BeautifulSoup(body_text)
            links=soup.findAll('a')
            for link in links:
                url =link.get('href')
                if target_url in url:
                    subdomain.append(url)
            return subdomain
        except Exception as e:
            print("出现异常:",e)
            pass
    else:
        return "0"


def netexp(url):
    #url = id
    try:
        addr = socket.getaddrinfo(url, 'http')[0][4][0]
        #netmain(addr)
    except:
        pass

def runscan(target_url):

    try:
        global urllist
        global iplist
        urllist = []
        turllist = []
        iplist =[]
        list1 = []
        list2 = []
        body_text = ""
        print ("runscan1:",target_url)
        body_text = get(target_url)
        #print ("body_text",body_text)
        get_ip(body_text)
        get_url(body_text)
        iplist = list(set(iplist))
        #print "runscan3:",iplist
        for i in urllist:
            if 'http://' not in i:
                i = target_url + i
                list1.append(i)
            else:
                list2.append(i)
        target_urllist = list(set(list1).union(set(list2)))
        collect_dirs = dirfuzz.fuzz_start(target_url)
        collect_dirs= list(set(collect_dirs))
        collect_ports = portScan(target_url)
        try:
            netexplore_t = threading.Thread(target=netexp,args=(target_url,))
            netexplore_t.start()
        except Exception as e:
            print(e)

        #subdomain = subdomainapi(target_url)
        subdomain = ""
        print("target_url",target_url)
        print("target_urllist",target_urllist)
        print("iplist",iplist)
        print("collect_dirs",collect_dirs)
        print("collect_ports",collect_ports)
        print("subdomain",subdomain)
        hashid = save_to_mysql.addurls(str(target_url), str(target_urllist), str(iplist), str(collect_dirs), str(collect_ports), str(subdomain))
    except Exception as e:
        print(e)
    #print target_urllist,iplist,collect_dirs,collect_ports,subdomain
    return target_urllist,iplist,collect_dirs,collect_ports,subdomain,hashid

#runscan('http://127.0.0.1')
