# -*- coding: UTF-8 -*-
import os
import cv2
import time
import pymysql
import easyocr
import uiautomator2 as u2
from PiaDataReadNew import PiaDataPicNew
from PiaDBAccessNew import PiaDBNew
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

# 截图函数
def getTaiData(x,y,width,height, pic_name):
    uiObjectBox = [x, y, x + width, y +height]
    d.screenshot().crop(uiObjectBox).save(pic_name + '.jpg')

# 大小变化函数
def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

# DB保存函数
def savedata(outpu):
    taiNo, adate, fileName = outpu
    print(fileName)
    # # 打开数据库连接
    db = pymysql.connect(host='localhost',user='root',password='541880qw',database='pia')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL
    sql = "INSERT INTO piadata__c (adate, Name, asort,kaiten,atype,orgkaiten) values (%s,%s,%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE kaiten = %s,orgkaiten = %s"

    reader = easyocr.Reader(['ja','en']) 
    # 读取图像
    img1 = cv2.imread(fileName+'.jpg')
    # img1_gray = cv2.threshold(img1, 90, 255, cv2.THRESH_BINARY)[1]
    # 变换大小
    img1 =  resize(img1, width=550)
    # 读取文本
    result = reader.readtext(img1)
    # 结果
    output = []
    # 最终结果
    totalOutput = []
    startMidY = 0
    _w,(_x,_y),(_x1,_y1),_z = tuple(result[0][0])
    startMidY = _y + (_y1 - _y)/2
    # print('1')
    # print(startMidY)
    totalCount = len(result)

    _index = 1
    for i in result:
        w,(x,y),(x1,y1),z = tuple(i[0])
        strVal = i[1]
        midY = y + (y1 - y)/2
        if not((startMidY - 10) < midY < (startMidY + 10)):
            startMidY = midY
            if len(output) >= 3:
                totalOutput.append(output)
                output = []
            else:
                output = []
        # 数字，確変，通常的场合
        if (strVal.isnumeric() or strVal == '確変' or strVal == '通常'):
            output.append(strVal)
        if (_index == totalCount) :
            if len(output) >= 3:
                totalOutput.append(output)
        _index = _index + 1
    for j in totalOutput:
        x,y,z = tuple(j)
        valInt = 0
        if z == '確変':
            valInt = 0
        elif z == '通常':
            valInt = 1
        # print(taiNo_adate + (x,y,z,y))
        val = (adate,taiNo) + (x,y,valInt,y,y,y)
        print((adate,taiNo) + (x,y,valInt))
        cursor.execute(sql, val)
    db.commit()
    db.close()
    # 删除文件
    if os.path.exists(fileName+'.jpg'):
        os.remove(fileName+'.jpg')


def saveLastStartData(adate,strTaiNo,totalAtari,lastKaiten):
    # # 打开数据库连接
    db = pymysql.connect(host='localhost',user='root',password='541880qw',database='pia')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL
    sql = "INSERT INTO piadata__c (adate, Name, asort,kaiten,atype,orgkaiten) values (%s,%s,%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE kaiten = %s,orgkaiten = %s"
    # save
    cursor.execute(sql, (adate,strTaiNo,(totalAtari+1),lastKaiten,2,lastKaiten,lastKaiten,lastKaiten))
    db.commit()
    db.close()

##########################################################################################################################################################
# adate = 250506
# adddays = 1
datetimetmp = datetime.now() - timedelta(days=1)
adate = int(datetimetmp.strftime("%y%m%d"))
print(adate)
strTaiNo = 585
########################################################### allcnt ##########################################################################
allcnt = 28
if strTaiNo >= 585:
    allcnt = 28 - strTaiNo + 585

########################################################### uiautomator2 ##########################################################################
d = u2.connect('14241JECB07010')
print('connected ok')
# d.app_start("jp.co.piagroup.app","com.google.firebase.MessagingUnityPlayerActivity")
###################################################################################################################################################
objPiaHead = PiaDataPicNew() 
# piaDB = PiaDB()
time.sleep(1)
# 移动到最高点
for k in range(8):
    d.swipe(40,1250,40, 1900)
time.sleep(1)
with ThreadPoolExecutor(max_workers=8) as t:
    # 番号
    for k in range(allcnt):
        # 総当り 取得
        time.sleep(2)
        getTaiData(165,898,190,120,'totalinfov1')
        getTaiData(165,1154,190,80,'totalinfov2')

        x, = objPiaHead.getHeadInfo('totalinfov1.jpg')
        y, = objPiaHead.getHeadInfo('totalinfov2.jpg')
        print('台号:' + str(strTaiNo))
        print('総当り:' + x)
        print('スタート:' + y)
        # 删除文件
        if os.path.exists('totalinfov1.jpg'):
            os.remove('totalinfov1.jpg')
        if os.path.exists('totalinfov2.jpg'):
            os.remove('totalinfov2.jpg')
        
        time.sleep(1)
        totalAtari = int(x)
        lastKaiten = int(y)
        saveLastStartData(adate,strTaiNo,totalAtari,lastKaiten)
        seed = 0
        if 0 <totalAtari <= 12:
            seed = 1
        elif 12 < totalAtari <=20:
            seed = 2
        elif 20 < totalAtari <=30:
            seed = 3
        elif 30 < totalAtari <=40:
            seed = 4
        elif 40 < totalAtari <=50:
            seed = 5
        elif 50 < totalAtari <=60:
            seed = 6
        elif 60 < totalAtari <=70:
            seed = 7
        elif 70 < totalAtari <=80:
            seed = 8
        elif 80 < totalAtari <=90:
            seed = 9
        elif 90 < totalAtari <=100:
            seed = 10
        elif 100 < totalAtari <=110:
            seed = 11
        # 移动到最低点
        for j in range(seed+3):
            d.swipe(40,1900,40, 1150)
        time.sleep(1)
        if seed > 0 :
            output1 = []
            r = range(seed)
            for i in r:
                strFileName =  str(strTaiNo) + '_' + str(i)
                # print(strFileName)
                getTaiData(90, 1125,650,900, strFileName)
                time.sleep(3)
                output1.append((strTaiNo, adate, strFileName))
                d.swipe(40, 1250, 40, 1900)
            # 维持执行的进程总数为8，当一个进程执行完后启动一个新进程. 
            t.map(savedata, output1)       
        time.sleep(1)
        # 移动到最高点
        for j in range(seed + 2):
            d.swipe(40,1250,40, 1900)
        # 下一台移动
        d.click(873, 615)
        time.sleep(3)
        strTaiNo = strTaiNo + 1
        # if strTaiNo == 576:
        #     time.sleep(1)
        #     piaDB = PiaDBNew()
        #     piaDB.getRen(adate,1)
        #     strTaiNo = 585
# 连续数计算
time.sleep(5)
piaDB = PiaDBNew()
piaDB.getRen(adate,2)
# python -m weditor
