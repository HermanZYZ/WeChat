import requests
import itchat
from itchat.content import *
import json
from pydub import AudioSegment
# from io import BytesIO
from aip import AipSpeech

APP_ID = '秘密'
API_KEY = '秘密'
SECRET_KEY = '秘密'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

#通过图灵机器人获取回复
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '秘密',
        'info': msg,
        'userid': 'Eternal',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return '爱你么么哒'

'''自动回复'''
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, NOTE, SHARING, RECORDING, ATTACHMENT, VIDEO])
def getMSG(msg):
    print(msg['FromUserName'])
    print(msg['Text'])
    print(msg['MsgType'])
    # if msg['FromUserName'] == '@226651aee0951b7cd0d6ca6d6029073e21c39a8616263b50976c035fc1e1f90a':
    if msg['FromUserName'] != None:
        if msg['MsgType'] == 34: #语音消息
            print(msg['Text'](msg['FileName']))
            audio = AudioSegment.from_mp3(msg['FileName'])
            export = audio.export(format="amr", bitrate="12.20k")
            transform = aipSpeech.asr(export.read(), 'amr', 8000, {'lan': 'zh', })
            if transform['err_msg'] == 'success.':
                print(transform['result'][0])
                itchat.send(get_response(transform['result'][0]), toUserName=msg['FromUserName'])

        elif msg['MsgType'] == 1: #文本消息
            itchat.send(get_response(msg['Text']), toUserName=msg['FromUserName'])

##将语音消息转成文本返回
def voiceToText(msg):
    audio = AudioSegment.from_mp3(msg['FileName'])
    export = audio.export(format="amr", bitrate="12.20k")
    transform = aipSpeech.asr(export.read(), 'amr', 8000, {'lan': 'zh', })
    print(transform)
    return transform

# print(get_response('你好'))
if __name__ == '__main__':
    # voiceToText()
    itchat.auto_login(hotReload=True)  # 调试用的，保留登录状态
    itchat.run()  # 启动微信
