# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import reply
import receive
import web
from SpeakerRecognition import *
import database
from Weather.weather import Weather
from News import mynews
import json
import time
from Camera.our_face.myfacerec import Myface

class Handle(object):
    def __init__(self):
        self.subscription_key = '20f920b168a241b9992fd0b1dc1bf664'
        self.flag = 0
        self.face_name = 'Not Identified'


    def POST(self):
        try: 
            webData = web.data()
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                user_name = database.from_uid_to_name(toUser)
                if recMsg.MsgType == 'text':
                    print('Content Received: ' + recMsg.Content)
                    print('User ID: ' + toUser)
                    print('User Name: ' + user_name)
                    if recMsg.Content == '五子棋':
                        return reply.reply_text(toUser, fromUser, 'orzmaodalao.ml:5901/' + user_name)
                    elif recMsg.Content == '排行榜':
                        return reply.reply_text(toUser, fromUser, 'orzmaodalao.ml:5901/scoreboard')
                    elif recMsg.Content == '新闻':
                        news = mynews.News(5)
                        news_content = ''
                        for n in news.dict:
                            news_content += json.dumps(n, ensure_ascii=False, encoding='UTF-8').encode('utf-8') + '\n'
                        return reply.reply_text(toUser, fromUser, news_content)
                    elif "天气" in recMsg.Content:
                        city_name = recMsg.Content.strip().split('天气')[0]
                        print('city_name = ' + city_name)
                        city_weather = Weather(city_name)
                        return reply.reply_text(toUser, fromUser, city_weather.show_result().encode('utf-8'))
                    elif "拍照" in recMsg.Content:
                        tmp = Myface()
                        self.face_name = tmp.show_result()
                        filename = 'temp.jpg'
                        return reply.reply_image(toUser, fromUser, filename)
                    elif "识别" in recMsg.Content:
                    	name = Myface.show_result()
                    	return reply.reply_text(toUser, fromUser, name)

                    return reply.reply_text(toUser, fromUser, "hello")

                    # filename = '0.jpg'
                    # return reply.reply_image(toUser, fromUser, filename)

                elif recMsg.MsgType == 'image':   
                    content = "你好"
                    return reply.reply_text(toUser, fromUser, content)

                elif recMsg.MsgType == 'voice':
                    print("Voice Received.")
                    filename = 'file'
                    new_filename = receive.download_voice(recMsg, filename)
                    
                    ConvertFileFormat.convert(new_filename)
                    new_filename = new_filename.split('.')[0] + '.wav'
                    ids = database.get_voice_ids()

                    speakerID = IdentifyFile.identify_file(self.subscription_key, new_filename, 'true', ids)
                    speaker_name = database.from_voiceid_to_name(speakerID)
                    
                    return reply.reply_text(toUser, fromUser, speaker_name)

                else:
                    return reply.Msg().send()
            else:
                print "暂且不处理"
                return reply.Msg().send()
        except Exception, Argment:
            return Argment

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "orzchangdalao" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument


