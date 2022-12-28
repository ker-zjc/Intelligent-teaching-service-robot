import abc
from typing import Text
import cv2
import numpy as np
import os
# coding=utf-8
import urllib
import urllib.request
import hashlib
from PIL import Image,ImageFont,ImageDraw
from playsound import playsound

#加载训练数据集文件
recogizer=cv2.face.LBPHFaceRecognizer_create()
# 可执行评分依靠训练数据集文件
recogizer.read('trainer/trainer.yml')
# 储存名字
names=[]

#------------------------------------------------------------------------------#

# 报警全局变量：防治检测到未训练人员，若有，发送短信提醒
warningtime = 0
abc = 0

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()

statusStr = {
    '0': '短信发送成功',
    '-1': '参数不全',
    '-2': '服务器空间不支持,请确认支持curl或者fsocket,联系您的空间商解决或者更换空间',
    '30': '密码错误',
    '40': '账号不存在',
    '41': '余额不足',
    '42': '账户已过期',
    '43': 'IP地址限制',
    '50': '内容含有敏感词'
}

def warning():
    smsapi = "http://api.smsbao.com/"
    # 短信平台账号
    user = 'Gean'
    # 短信平台密码
    password = md5('lry981222')
    # 要发送的短信内容
    content = '【安全提示】尊敬的主人，发现未知人员在实验室，请注意！'
    # 要发送短信的手机号码
    phone = '17302254866'

    data = urllib.parse.urlencode({'u': user, 'p': password, 'm': phone, 'c': content})
    send_url = smsapi + 'sms?' + data
    response = urllib.request.urlopen(send_url)
    the_page = response.read().decode('utf-8')
    print(statusStr[the_page])

#------------------------------------------------------------------------------#
#准备识别的图片
def face_detect_demo(img):
    # 导入图片灰度化
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    face_detector=cv2.CascadeClassifier('./haarcascade_frontalface_alt2.xml')
    face=face_detector.detectMultiScale(gray,1.1,5,cv2.CASCADE_SCALE_IMAGE,(100,100),(300,300))
    #face=face_detector.detectMultiScale(gray)
    for x,y,w,h in face:
        # 绘制矩形和圆形将人脸锁定
        cv2.rectangle(img,(x,y),(x+w,y+h),color=(0,0,255),thickness=2)
        cv2.circle(img,center=(x+w//2,y+h//2),radius=w//2,color=(0,255,0),thickness=1)
        # 人脸识别：人脸预测并评分（confidence）
        ids, confidence = recogizer.predict(gray[y:y + h, x:x + w])
        #print('标签id:',ids,'置信评分：', confidence)
        
        # 若评分大于80，说明人脸不可信，警报+1
        if confidence > 80:
            global warningtime
            warningtime += 1
            # 当警报超过100，说明该人脸不是所录入的人脸
            if warningtime > 100:
               warning()
               warningtime = 0
            # 创建一个可以在给定图像上绘图的对象
            # draw = ImageDraw.Draw(img)    
            # 设置中文格式
            # fontstyle = ImageFont.truetype("simsun.ttc",20,encoding="utf-8")
            # 绘制文本
            # draw.text((x + 10, y - 10),'不认识的陌生人',(0,255,0),font = fontstyle)

            cv2.putText(img, 'who?', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
        #如果评分低于80分，说明为可信人员，将其姓名显示在方框上
        else:
            cv2.putText(img,str(names[ids-1]), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
    cv2.namedWindow('result',0)
    cv2.imshow('result',img)
    #print('bug:',ids)

def name():
    path = './data/jm/'
    #names = []
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    for imagePath in imagePaths:
       name = str(os.path.split(imagePath)[1].split('.',2)[1])
       names.append(name)


cap=cv2.VideoCapture(0)
#cap = cv2.VideoCapture('http://admin:981222@192.168.43.182:8081/')

#默认分辨率为640x480,设置成1920x1080
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

name()
while True:
    flag,frame=cap.read()
    if not flag:
        break
    face_detect_demo(frame) 
    if ord(' ') == cv2.waitKey(10):
        break
cv2.destroyAllWindows()
cap.release()
playsound('asd.mp3')#输出音频
#print(names)
