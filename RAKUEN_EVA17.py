# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
from PiaDataReadNew import PiaDataPicNew
from PiaDBAccessNew import PiaDBNew
import pymysql
import time
import random
import re

def wairForRandom():
   time.sleep(random.randint(1,6))

def getFormatDate(dindex):
    datetimetmpEnd = datetime.now() - timedelta(days=dindex)
    adateEnd = int(datetimetmpEnd.strftime("%y%m%d"))
    return adateEnd

def saveLastStartData(data):
    adate,strTaiNo,asort,orgkaiten,atype = data
    # # 打开数据库连接
    db = pymysql.connect(host='localhost',user='root',password='541880qw',database='pia')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL
    sql = "INSERT INTO piadata__c (adate, Name, asort,kaiten,atype,orgkaiten) values (%s,%s,%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE kaiten = %s,orgkaiten = %s"
    # save
    cursor.execute(sql, (adate,strTaiNo,asort,orgkaiten,atype,orgkaiten,orgkaiten,orgkaiten))
    db.commit()
    db.close()

def getDataForPage(driver,strTaiNo,adate,first_num):
    # 大当り履歴データ
    wairForRandom()
    tbody = driver.find_element(By.XPATH, "//*[@id='dedama_data_list']/tbody")

    # 2. 获取 tbody 下的所有行 (tr)
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for row in rows:
        # 3. 获取当前行下的所有单元格 (td)
        cells = row.find_elements(By.TAG_NAME, "td")
        if cells[0].text == '回数':
            continue
        # data = [cell.text for cell in cells if cell.text.strip()]
        data =[]
        if cells[0].get_attribute("class") =='red':
            data.append(cells[0].text)
            data.append(cells[2].text)
            data.append('0')
        elif cells[0].text == '-':
            data.append(str(first_num + 1))
            data.append(cells[2].text)
            data.append('2')
        else:
            data.append(cells[0].text)
            data.append(cells[2].text)
            data.append('1')

        datatp = (str(adate),str(strTaiNo)) + tuple(data)
        print(datatp)
        saveLastStartData(datatp)

def getDataForBan(driver,strTaiNo,adate,dateFlg):
    xpath = f"//div[@class='daiban' and text()='{strTaiNo}']"

    # 番台
    daiban_els = driver.find_element(By.XPATH, xpath)
    wairForRandom()
    print(daiban_els.text)
    daiban_els.click()

    # ＞＞
    # wairForRandom()
    # element = driver.find_element(By.XPATH, "//*[@class='date_link']//*[text()='＞＞']")
    # element.click()

    
    xpath2 = f"//*[@class='date_link']//*[text()='{dateFlg}']"
    wairForRandom()
    # element = driver.find_element(By.XPATH, "//*[@class='date_link']//*[text()='3日前']")
    element = driver.find_element(By.XPATH, xpath2)
    element.click()

    # 大当り回数 X回
    wairForRandom()
    daiban_els = driver.find_element(By.CSS_SELECTOR, '.sort_order')
    daiban_els_text = daiban_els.text
    print(daiban_els_text)
    first_num = int(re.search(r'\d+', daiban_els_text).group())
    getDataForPage(driver,strTaiNo,adate,first_num)

    # 次へ
    for i in range(5):
        try:
            wairForRandom()
            element = driver.find_element(By.XPATH, "//*[@class='list_navigation']/div/a[text()='次へ']")
            print(element.text)
            element.click()
            getDataForPage(driver,strTaiNo,adate,first_num)
        except NoSuchElementException:
            print('NoSuchElementException')
            break

    # 戻る
    # print('戻る')
    wairForRandom()
    element = driver.find_element(By.XPATH, "//*[@id='footer']/a[text()='戻る']")
    print('戻る')
    element.click()
    # if strTaiNo > 970:
    #     wairForRandom()
    #     element = driver.find_element(By.XPATH, "//*[@class='list_navigation']/div/a[text()='次へ']")
    #     element.click()
###########################################################################################################################################

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
driver.set_window_position(0, 0)
driver.get('https://www.d-deltanet.com/pc/D0301.do?pmc=22021004&clc=01&urt=400&pan=1')
time.sleep(5)

model_link_element = driver.find_element(By.ID, "model_link")
model_link_elements = model_link_element.find_elements(By.TAG_NAME, 'a')
print(model_link_elements[2].text)
# ｅ 新世紀エヴァンゲリオン ～はじまりの記憶～ [28]
model_link_elements[2].click()
wairForRandom()

menu_link_element1 = driver.find_element(By.ID, "menu_link")
menu_link_elements1 = menu_link_element1.find_elements(By.TAG_NAME, 'a')

wairForRandom()
print(menu_link_elements1[11].text)
# 大当り履歴データ
menu_link_elements1[11].click()
# daiban
# daiban_els = driver.find_element(By.CSS_SELECTOR, '.daiban')
###########################################################################################################################################
dateFlg = 1
strTaiNoT = 898




###########################################################################################################################################
dateFlgT = '前日'
if dateFlg > 1:
    dateFlgT =f"{dateFlg}日前"
adate = getFormatDate(dateFlg)
print(adate)
# if strTaiNoT > 970:
#     wairForRandom()
#     element = driver.find_element(By.XPATH, "//*[@class='list_navigation']/div/a[text()='次へ']")
#     element.click()
for strTaiNo in range(strTaiNoT,941):
    if strTaiNo in range(912,927):
        continue
    getDataForBan(driver,strTaiNo,adate,dateFlgT)
    # if strTaiNo == 970:
    #     wairForRandom()
    #     element = driver.find_element(By.XPATH, "//*[@class='list_navigation']/div/a[text()='次へ']")
    #     print(element.text)
    #     element.click()

print('OK')
time.sleep(20)