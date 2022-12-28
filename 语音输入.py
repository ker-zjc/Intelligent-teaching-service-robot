import time
import speech_recognition as sr
import logging
logging.basicConfig(level=logging.DEBUG)
from aip import AipSpeech
app_id = "17991059"
api_key = "p9bitGtcyv0OcgQ2o6cbGBe0"
secret_key = "fPmpMxVNLi0P2KNheibRYUKfGYQMkX0i"
aip_speech = AipSpeech(app_id,api_key,secret_key)

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
        end_time = time.time()
        print(end_time - start_time)
    else:
        print(ret['err_msg'])
    logging.info('end')
