#coding=utf-8

def from_uid_to_name(uid):
    if uid == 'ob0Sx0jrDdT8j91cNEikCZc19Giw':
        return 'Player1'
    elif uid == 'ob0Sx0gUJ6bhM8fvCs5wTfUDuaQU':
        return 'Player2'
    elif uid == 'ob0Sx0nzvESvUVUJAYnhflcaskqA':
        return 'Player3'
    elif uid == 'ob0Sx0mJn2MiIb3LVN-NQAOwCApo':
        return 'Player4'
    else:
        return 'Player5'


def from_abbr_to_name(abbr):
    if abbr == 'mao':
        return "毛威超"
    elif abbr == 'chang':
        return "常瑞恒"
    elif abbr == 'lv':
        return "吕福源"
    elif abbr == 'huang':
        return "黄潮钦"

def from_voiceid_to_name(voiceid):
    voiceid = voiceid.encode('utf-8')
    with open('SpeakerRecognition/voiceid.txt') as file:
        lines = file.readlines()
    for line in lines:
        tmp = line.strip().split('\t')
        if voiceid == tmp[1]:
            return from_abbr_to_name(tmp[0])
    return "未知身份"

def get_voice_ids():
    with open('SpeakerRecognition/voiceid.txt') as file:
        lines = file.readlines()
    tmp = []
    for line in lines:
        tmp.append(line.split('\t')[1])
    return tmp