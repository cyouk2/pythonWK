# -*- coding: UTF-8 -*-
import os
import cv2
import imutils
import numpy as np 
from imutils import contours

class PiaDataPicNew:
    digits =[]
    def __init__(self):
        self.digits = self.loadDigits()

    def cv_show(self, name, img):
        # cv2.imshow(name, img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        pass


    def loadDigits(self):
        digits =[]
        rectKernel4 = cv2.getStructuringElement(cv2.MORPH_RECT, (5 , 5))
        now_dir = os.getcwd()
        # print("当前运行目录：" + now_dir)
        numbers_address = now_dir + "\\digits"
        # 加载数字模板
        path = numbers_address
        filename = os.listdir(path)
        for file in filename:
            # print(file)
            image = cv2.imread(numbers_address + "\\" + file)
            image = imutils.resize(image, height=70)
            img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            group_02 = cv2.morphologyEx(img_gray, cv2.MORPH_CLOSE, rectKernel4)
            # 预处理
            group_04 = cv2.threshold(group_02, 0, 255, cv2.THRESH_BINARY  | cv2.THRESH_OTSU)[1]  # 二值化的group_1
            # self. cv_show("Output_image_2", group_04)
            # 计算每一组的轮廓 这样就分成n个小轮廓了
            digitCnts = cv2.findContours(group_04.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            x, y, w, h = cv2.boundingRect(digitCnts[0])
            digit_roi = imutils.resize(group_04[y:y+h, x:x+w], height=40)
            # self. cv_show('digit_roi',digit_roi)
            # 将数字模板存到列表中
            digits.append(digit_roi)
            # self. cv_show("666", digit_roi)
        # print("加载数字模板成功")
        return digits
    
    def getHeadInfo(self, fileName):
        digits = self.digits
        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 5))
        rectKernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5 , 5))
        # rectKernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (6 , 6))
        # 读取图片
        image = cv2.imread(fileName)
        # 设置图片大小
        image = imutils.resize(image, height=60)
        # 灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self. cv_show('gray', gray)
        # 高斯模糊
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        self. cv_show('blurred', blurred)
        # 轮廓
        edged = cv2.Canny(blurred, 50, 200, 255)
        # self. cv_show('name1', edged)
        thresh = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, rectKernel)
        self. cv_show('dst', thresh) 
        # 轮廓
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        card_copy = image.copy()
        cv2.drawContours(card_copy, cnts, -1, (0, 0, 255), 2)

        # displayCnt = None
        locs = []  # 存符合条件的轮廓
        # card_copy2 = image.copy()
        for i, c in enumerate(cnts):
            # 计算矩形
            x, y, w, h = cv2.boundingRect(c)
            # print((x, y, w, h,x+w,y+h))
            ar = w / float(h)
            # print(ar)
            if 0 < ar < 4 :
                if (x > 0 ):
                    locs.append((x, y, w, h))
            # locs.append((x, y, w, h))
        locs = sorted(locs, key=lambda x: x[1])

        result01=[]
        for (k, (gx, gy, gw, gh)) in enumerate(locs):  # 遍历每一组大轮廓(包含4个数字)

            # 根据坐标提取每一个组(4个值)
            group_01 = gray[gy - 5:gy + gh + 5, gx - 5:gx + gw + 5]  # 往外扩一点
            self. cv_show("Output_image_",group_01)
            group_02 = cv2.morphologyEx(group_01, cv2.MORPH_CLOSE, rectKernel2)
            # 预处理
            group_04 = cv2.threshold(group_02, 0, 255, cv2.THRESH_BINARY  | cv2.THRESH_OTSU)[1]  # 二值化的group_1
            # 计算每一组的轮廓 这样就分成4个小轮廓了
            digitCnts = cv2.findContours(group_04.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            # 排序
            digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]
            
            groupOutput=[]
            # # 计算并匹配每一组中的每一个数值
            # print('*****************************')
            for i, c in enumerate(digitCnts):
                (x, y, w, h) = cv2.boundingRect(c)  # 外接矩形
                # print((k, x, y, w, h))
                self. cv_show("Output_image_",group_04 [y:y + h, x:x + w])
                # 数字1的宽度最小
                if w < 20:
                    groupOutput.append('1')
                else:
                    roi = group_04 [y:y + h, x:x + w]  # 在原图中取出小轮廓覆盖区域,即数字
                    # roi = cv2.GaussianBlur(roi, (5, 5), 0)
                    roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY  | cv2.THRESH_OTSU)[1]  # 二值化的group_1
                    roi = imutils.resize(roi, height=40)
                    # self. cv_show("Output_image_"+str(i), roi)
                    scores = []  # 单次循环中,scores存的是一个数值 匹配 10个模板数值的最大得分
                    # 在模板中计算每一个得分
                    # digits的digit正好是数值0,1,...,9;digitROI是每个数值的特征表示
                    for digitROI in digits:
                        # 进行模板匹配, res是结果矩阵
                        res = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF)  # 此时roi是X digitROI是0 依次是1,2.. 匹配10次,看模板最高得分多少
                        Max_score = cv2.minMaxLoc(res)[1]  # 返回4个,取第二个最大值Maxscore
                        scores.append(Max_score)  # 10个最大值
                    # 得到最合适的数字
                    groupOutput.append(str(np.argmax(scores)))  # 返回的是输入列表中最大值的位置
            result01.append("".join(groupOutput))
        # print(result01)
        return tuple(result01)

# objPiaHead = PiaDataPicNew() 
# x = objPiaHead.getHeadInfo('totalinfov1.jpg')
# y = objPiaHead.getHeadInfo('totalinfov2.jpg')
    # getTaiData(165,1230,190,120,'totalinfov1')
    
    # getTaiData(165,1490,190,80,'totalinfov2')
