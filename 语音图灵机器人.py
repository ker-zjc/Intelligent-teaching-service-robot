import time
import speech_recognition as sr
import logging
import requests
import json
logging.basicConfig(level=logging.DEBUG)
from aip import AipSpeech
from aip import AipSpeech
import re
from playsound import playsound
app_id = "17991059"
api_key = "p9bitGtcyv0OcgQ2o6cbGBe0"
secret_key = "fPmpMxVNLi0P2KNheibRYUKfGYQMkX0i"
client = AipSpeech(app_id,api_key,secret_key)
aip_speech = AipSpeech(app_id,api_key,secret_key)
url = "http://openapi.tuling123.com/openapi/api/v2"
headers = {
    'User-Agent': '....' #请求头信息，这里就不列出来了，可以搜搜怎么得到自己的请求头信息，然后把User-Agent这一行的列出来
}

r = sr.Recognizer()
#麦克风
mic = sr.Microphone(sample_rate=16000)
x=0
while x<3:
    x+=1
    logging.info('录音中')
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    logging.info('录音结束，识别中...')
    start_time = time.time()
    print(type(audio))
    audio_data = audio.get_wav_data()
    print(type(audio_data))
    #识别本地文件
    ret = aip_speech.asr(audio_data,'wav',16000,{'dev_pid':1536,})
    print(ret)
    if ret and ret['err_no'] == 0:
        result = ret['result'][0]
        print(result)
    else:
        print(ret['err_msg'])
    logging.info('end')
    params = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": result  # 输入图灵聊天文本的地方
            },
            "inputImage": {
                "url": "imageUrl"
            },
            "selfInfo": {
                "location": {
                    "city": "北京",
                    "province": "北京",
                    "street": "信息路"
                }
            }
        },
        "userInfo": {
            "apiKey": 'b3926d6810c240e881e938f78f101a52',#图灵密钥
            "userId": 'tesme'  # 不超过8个字符
        }
    }
    session = requests.session()
    result = session.post(url=url, data=json.dumps(params), headers=headers)
    print(result.json()['results'][0]['values']['text'])#图灵的文本输出
    with open("audio.txt", "w") as f:
        f.write(result.json()['results'][0]['values']['text'])#把图灵输出的内容写入文本
        b = f.read()
    result = client.synthesis(b,"zh",1, {
        "vol": 5,
        "spd": 3,
        "pit": 9,
        "per": 3
    })
    with open("audio.mp3", "wb") as f:#把文本转为语音
        f.write(result)
    playsound('audio.mp3')#输出音频



