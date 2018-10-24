# -*- coding: utf-8 -*-
# filename: receive.py
import xml.etree.ElementTree as ET
import requests
import access_token

def parse_xml(web_data):
    if len(web_data) == 0:
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)
    elif msg_type == 'voice':
        return VoiceMsg(xmlData)

def download_voice(VoiceMsg, filename):
    url = 'https://api.weixin.qq.com/cgi-bin/media/get'
    token = access_token.get_access_token()
    print('MediaId:' + VoiceMsg.MediaId)
    params = {'access_token': token, 'media_id': VoiceMsg.MediaId}
    r = requests.get(url, params=params)
    new_filename = 'SpeakerRecognition/audio/tmp/' + filename + '.amr'
    with open(new_filename, 'wb') as file:
        file.write(r.content)
    return new_filename


class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text

class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")

class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text

class VoiceMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.MediaId = xmlData.find('MediaId').text
        self.Format = xmlData.find('Format').text

