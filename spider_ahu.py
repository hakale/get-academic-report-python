#!/usr/bin/env python
# -*- coding: utf-8 -*-


from urllib import request
from bs4 import BeautifulSoup
import os
from Mail import *

class spider_ahu(object):
	def __init__(self):
		self.sourcelink = 'http://www.ahu.edu.cn/c/24554/index.shtml'
		self.hosturl = "http://cms.ahu.edu.cn"
		self.pageSize = "30"
		self.page = "1"
		self.categoryId = "24554" 
		self.randomNum = "0.847591380821541"
	
	'''def getsoucepage(self):
		self.req = request.Request(self.sourcelink)
		self.req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')
		with request.urlopen(self.req) as f:
			if f.status != 200:
				return status
			self.r = f.read()
			with open('ahu.html', 'wb') as file:
				file.write(self.r)
			return self.r'''
	
		
	def getcatalogue(self):								#获取目录文件
		url = self.hosturl + "/admin/push.jhtml?method=pushItemArticleList&type=xml&categoryId=" + self.categoryId + "&pageNo=" + self.page + "&num=" + self.pageSize + "&att=pageObject.docString&r=" + self.randomNum
		self.req = request.Request(url)
		with request.urlopen(self.req) as f:
			if (f.status != 200):
				print("Can't getcatalogue!")
				exit()
			else:
				r = f.read()
				return r

	def getpage(self, catalogue):
		soup = BeautifulSoup(catalogue, "html.parser")
		total = ""
		count = 0
		for mess in soup.find_all("item"):				#遍历目录，读取每篇通知
			count += 1
			if count > 6:
				break
			titleName = mess['title']
			conlink = "http://www.ahu.edu.cn" + mess['link']
			creaTime = mess['createtime']
			print(conlink)
			req = request.Request(conlink)
			with request.urlopen(req) as con:			#读取通知内容
				r = con.read()
				soupconent = BeautifulSoup(r, 'html.parser')
				filte = 0
				for mess in soupconent.find_all('div'):
					if mess.get('id') == 'university27':		
						for para in mess.find_all('p'):
							contents = (para.get_text().replace(u'\xa0', u' '))  #replace是因为在windows gbk终端下某些字符无法输出，不输出的话就不存在问题
							if filte == 0:
								total = total  + '<b>' + contents + '</b>'
							elif filte == 1 or filte == 8 or filte == 9 or filte == 10: #过滤掉通知里的无关信息"欢迎之类
								pass
							else:
								total = total  + '<p>' + contents + '</p>' 
							filte += 1
		cont = ""
		try:
			cont = open('total_old.html', 'r').read()
		except:
			pass
		with open('total_old.html', 'w',) as oldfile:
			if cont != total:
				print(cont)
				maillist = ['xxx@qq.com','xxx@qq.com','xx7@qq.com', 'xxxxxx96@163.com'] 
				for tar in maillist:
					mail = Mail(target = tar)  #收件邮箱
					mail.sendMail(total)	
			oldfile.write(total)
				


if __name__ == '__main__':
	process = spider_ahu()
	#status = process.getsoucepage()
	r = process.getcatalogue()
	process.getpage(r)
		
		