import requests
import json
url = "http://openapi.tuling123.com/openapi/api/v2"
headers = {
    'User-Agent': '....' #请求头信息，这里就不列出来了，可以搜搜怎么得到自己的请求头信息，然后把User-Agent这一行的列出来
}
while 1 > 0:
    params = {
        "reqType":0,
        "perception": {
            "inputText": {
                "text": input("你想对我说什么呢:")
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
            "apiKey": '51e979d289364f80a5851da2f73b06b5',
            "userId": 'tesme' #不超过8个字符
        }
    }
    session = requests.session()
    result = session.post(url = url, data = json.dumps(params), headers = headers)
    print(result.json()['results'][0]['values']['text'])
