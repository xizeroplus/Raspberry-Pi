# -*- coding: utf-8 -*-
import urllib2
import json
from Weather.city import city
from bs4 import BeautifulSoup
import re


class Weather(object):
    """weather"""

    def __init__(self, cityname):
        #cityname = raw_input('Which city?\n')
        citycode = city.get(cityname)
        if citycode:
            try:
                #print citycode
                request = urllib2.Request('http://www.weather.com.cn/weather/%s.shtml' % citycode)

                #在请求加上头信息，伪装成浏览器访问
                request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')

                opener = urllib2.build_opener()
                resp = opener.open(request)
                resp = resp.read().decode('utf-8')
                
                #resp = urllib2.urlopen(url).read()
                #print citycode
                #resp=urlopen('http://www.weather.com.cn/weather/101010100.shtml')
                soup=BeautifulSoup(resp,'html.parser')
                tagToday=soup.find('p',class_="tem")  #第一个包含class="tem"的p标签即为存放今天天气数据的标签
                
                try:
                    temperatureHigh=tagToday.span.string  #有时候这个最高温度是不显示的，此时利用第二天的最高温度代替。
                except AttributeError as e:
                    temperatureHigh=tagToday.find_next('p',class_="tem").span.string  #获取第二天的最高温度代替

                temperatureLow=tagToday.i.string  #获取最低温度
                weather=soup.find('p',class_="wea").string #获取天气
                tagWind=soup.find('p',class_="win")
                winL=tagWind.i.string

                str_temp = ('%s\n%s ~ %s\n%s') % (
                    weather,
                    temperatureLow,
                    temperatureHigh,
                    winL
                )                                                
                self.result = str_temp
            except:
                self.result = '网络故障'
        else:        
            self.result = '城市有误'
    
    def show_result(self):
        return self.result




