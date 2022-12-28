from aip import AipSpeech
""" 你的 APPID AK SK"""
import re
app_id = "17991059"
api_key = "p9bitGtcyv0OcgQ2o6cbGBe0"
secret_key = "fPmpMxVNLi0P2KNheibRYUKfGYQMkX0i"

client = AipSpeech(app_id,api_key,secret_key)
f = open("audio.txt")
a = f.read()
f.close

result = client.synthesis(a,"zh",1,{
    "vol": 5,
    "spd": 3,
    "pit": 9,
    "per": 3
})
with open("audio.mp3","wb") as f:
    f.write(result)
