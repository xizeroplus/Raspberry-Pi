import sys
import database
from SpeakerRecognition import *
import json
import requests
import access_token

if __name__ == '__main__':

    toUser = sys.argv[1]
    fromUser = sys.argv[2]
    new_filename = sys.argv[3]
    token = access_token.get_access_token()
    subscription_key = '20f920b168a241b9992fd0b1dc1bf664'

    ConvertFileFormat.convert(new_filename)
    new_filename = new_filename.split('.')[0] + '.wav'
    ids = database.get_voice_ids()
    speakerID = IdentifyFile.identify_file(subscription_key, new_filename, 'true', ids)
    speaker_name = database.from_voiceid_to_name(speakerID)

    url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send'
    params = {'access_token': token}

    send_json = {
    "touser":toUser,
    "msgtype":"text",
    "text":
    {
         "content":speaker_name
    }
}
#'''.format(toUser, speaker_name)

    r = requests.post(url, params=params, json=send_json)
    print(r)
