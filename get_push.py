#http://www.ahu.edu.cn/52/list.htm

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request
from bs4 import BeautifulSoup
import os
from Mail import *

link = "http://www.ahu.edu.cn/52/list.htm"
hostlink = "http://www.ahu.edu.cn"
mailtext = ""
req = request.Request(link)
with request.urlopen(req) as f:
    con = f.read()
    soup = BeautifulSoup(con, "html.parser")
    #con = soup.prettify().replace(u'\xf1', u' ').replace(u'\xa0', u' ')
    for wplist in soup.find_all('a'):
        if wplist.has_attr('target') and wplist.has_attr('alt'):
            #print(wplist.get('title'))
            href = wplist.get('href')                              # parsing the page and get the article page address
            with request.urlopen(hostlink + href) as pagefile:
                pagemain = pagefile.read();
                pagesoup = BeautifulSoup(pagemain, "html.parser")
                #print(pagesoup.find('title'))
               # print(pagesoup.prettify().replace(u'\xf1', u' ').replace(u'\xa0', u' '))
                mailtext += '<b>' + pagesoup.find('title').get_text() + '</b>'
                for meta in pagesoup.find_all('meta'):              #get content
                    if  not meta.has_attr('http-equiv'):
                        mailtext += '<p>' + meta.get('content').replace('演讲人：','<p>演讲人：').replace('.', '.<p>').replace('报告人', '<p>报告人').replace('时间', '<p>时间').replace('地点', '</p><p>地点').replace('简介：', '<p>简介：</p>').replace('主持人：', '<p>主持人：') + '</p>'
                        #print(meta.get('content').replace(u'\xa0', u' '))#.replace(u'\xf1', u' ').
cont = ""
try:
    cont = open('total_old.html', 'r').read()
except:
    pass
with open('total_old.html', 'w',) as oldfile:
    if cont != mailtext:
        #print(cont)
        maillist = ['282271296@qq.com','1542804739@qq.com','gemini0617@qq.com', 'm17775301896@163.com'] #,'1542804739@qq.com','gemini0617@qq.com', 'm17775301896@163.com'
        for tar in maillist:
            mail = Mail(target = tar)  #收件邮箱
            mail.sendMail(mailtext)	
    oldfile.write(mailtext)               
                
