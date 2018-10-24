# coding:utf-8

import json 
import requests
from bs4 import BeautifulSoup

class News:
	'新闻的类'

	def __init__(self,number=10):
		info = []

		#titles = []
		#links = []

		url = "http://news.qq.com/"

		# 请求腾讯新闻的URL，获取其text文本
		wbdata = requests.get(url).text

		# 对获取到的文本进行解析
		soup = BeautifulSoup(wbdata,'lxml')

		# 从解析文件中通过select选择器定位指定的元素，返回一个列表
		news_titles = soup.select("div.text > em.f14 > a.linkto")

		

		# 对返回的列表进行遍历
		for n in news_titles:
			title = n.get_text()
			link = n.get("href")
			#titles.append(title)
			#links.append(link)
			#print title
			info.append(title)
			info.append(link)

			if len(info) >= number*2:
				break

		self.dict = info;


		#self.new_dict = dict(zip(titles,links))

		#for n in self.new_dict:
		#	print json.dumps(n, ensure_ascii=False, encoding='UTF-8')


	def show_result(self):
		return self.dict


