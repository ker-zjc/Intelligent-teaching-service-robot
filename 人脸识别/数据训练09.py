import os
import cv2 as cv
from PIL import Image
import numpy as np

def getImageAndLabels(path):
    # 存储人脸数据:二维列表，二维数组
    facesSamples = []
    # 存储姓名数据
    ids = []
    # 储存图片信息
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    # 加载分类器
    face_detector = cv.CascadeClassifier('./haarcascade_frontalface_alt2.xml')
    # 遍历列表中的图片：保存身份信息
    for imagePath in imagePaths:
        # 打开图片，灰度化PIL有九种不同模式：1(黑白，有像素为1，没像素为0), L(灰度图像，把每个像素点变成0-255的数值，颜色越深，值越大),P, RGB, RGBA, CMYK, YCbCr, I, F.
        PIL_img = Image.open(imagePath).convert('L')
        # 图片灰度化处理后进行向量化处理，将图像转换为数组（把每个像素点变成数值），以黑白深浅
        # img_numpy:列表
        img_numpy = np.array(PIL_img,'uint8')
        # 通过分类器提取人脸特征，获取图片人脸特征，将人脸的特征数组存储在faces中
        faces = face_detector.detectMultiScale(img_numpy)
        # 获取每张图片的id和姓名
        id = int(os.path.split(imagePath)[1].split('.')[0])
        # 预防无面容照片
        # 将所画的方框添加到facesSamples列表中，所以每一个ids(0)和facesSamples(0)它们对应的是同一个人和同一个人向量下的特征
        for x,y,w,h in faces:
            ids.append(id)
            facesSamples.append(img_numpy[y:y+h,x:x+w])
    #打印脸部特征和id
    print('id:',id)
    print('fs:',facesSamples)
    return facesSamples,ids


if __name__ == '__main__':
    # 图片路径
    path = './data/jm/'
    # 获取图像数组id标签数组和姓名
    faces,ids = getImageAndLabels(path)
    # 加载识别器:加载LBPH识别器将面部和身份信息通过训练整合在一起，最后写入.yml文件中
    # 最后面部信息和身份信息就一一对应保存于文件中，在识别人脸时调用关系文件即可完成识别
    recognizer = cv.face.LBPHFaceRecognizer_create()
    # 训练
    recognizer.train(faces,np.array(ids))
    # 保存文件：生成一个一一对应的关系文件
    recognizer.write('trainer/trainer.yml')
