import requests
import json

def get_access_token():

    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {'grant_type': 'client_credential', 'appid': 'wx7468bb7421a4a9be', 'secret': 'd1bbaca4afc0cf3927026f07ff11cc85'}

    r = requests.get(url, params=params)
    # print(r.text)

    data = json.loads(r.text)
    print('Get New Access Token: ' + data['access_token'])
    return data['access_token']
