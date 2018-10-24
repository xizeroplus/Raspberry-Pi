# -*- coding: utf-8 -*-
# filename: reply.py
import time
import json
import requests
import access_token

def reply_text(toUser, fromUser, content):
    replyMsg = TextMsg(toUser, fromUser, content)
    return replyMsg.send()

def reply_image(toUser, fromUser, filename):

    mediaId = upload_temp_image(filename)

    # mediaId = recMsg.MediaId
    replyMsg = ImageMsg(toUser, fromUser, mediaId)
    return replyMsg.send()


# 新增临时素材，返回新素材的 media_id
def upload_temp_image(filename):
    token = access_token.get_access_token()
    url = 'https://api.weixin.qq.com/cgi-bin/media/upload'

    file = open(filename, 'rb')
    params = {'access_token': token, 'type': 'image'}
    files = {'media': file}

    r = requests.post(url, params=params, files=files)
    #print(r.text)
    mediaId = json.loads(r.text)['media_id']

    return mediaId


class Msg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)
    
class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)
