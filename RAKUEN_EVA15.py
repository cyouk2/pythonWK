# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
from RAKUEN_DBNEW import RAKUENDBNew
# from PiaDBAccessNew import PiaDBNew
import pymysql
import time
import random
import re

def wairForRandom():
   time.sleep(random.randint(3,6))
# getFormatDate
def getFormatDate(dindex):
    datetimetmpEnd = datetime.now() - timedelta(days=dindex)
    adateEnd = int(datetimetmpEnd.strftime("%y%m%d"))
    return adateEnd

# saveLastStartData
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
# 次へ
def goToNextPage(driver):
    wairForRandom()
    element = driver.find_element(By.XPATH, "//*[@class='list_navigation']/div/a[text()='次へ']")
    print('次へ')
    element.click()

# goToCommon
def goToCommon(driver, xpath2):
    wairForRandom()
    element = driver.find_element(By.XPATH, xpath2)
    element.click()

# getDataForPage
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

    # 番台
    xpath_strTaiNo = f"//div[@class='daiban' and text()='{strTaiNo}']"
    # 戻る
    xpath_return = "//*[@id='footer']/a[text()='戻る']"
    # Ｘ日前を押下する
    xpath_dateFlg = f"//*[@class='date_link']//*[text()='{dateFlg}']"
    # ＞＞
    # xpath_NEXT = "//*[@class='date_link']//*[text()='＞＞']"

    # 番台を押下する
    goToCommon(driver, xpath_strTaiNo)
    # Ｘ日前を押下する
    goToCommon(driver, xpath_dateFlg)
    # 大当り回数 X回
    wairForRandom()
    daiban_els = driver.find_element(By.CSS_SELECTOR, '.sort_order')
    print(daiban_els.text)
    # 大当り回数
    first_num = int(re.search(r'\d+', daiban_els.text).group())

    # 画面データ取得
    getDataForPage(driver,strTaiNo,adate,first_num)

    # 次へ
    for i in range(5):
        try:
            goToNextPage(driver)
            # 画面データ取得
            getDataForPage(driver,strTaiNo,adate,first_num)
        except NoSuchElementException:
            break

    # 戻る
    goToCommon(driver, xpath_return)
    print('戻る')
    if strTaiNo > 970:
        # ９７０以降のデータは次の画面にあるから
        goToNextPage(driver)
###########################################################################################################################################

driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
driver.set_window_position(0, 0)
driver.get('https://www.d-deltanet.com/pc/D0301.do?pmc=22021004&clc=01&urt=400&pan=1')

########################################################### xpath ##########################################################################
# 承諾
xpath_agree = "//*[@class='overlay-cookie-policy']/div[@class='agree']"
# P新世紀エヴァンゲリオン１５　未来への咆哮 [40]
xpath_EVAXX = "//*[@id='model_link']//*[text()='P新世紀エヴァンゲリオン１５　未来への咆哮 [40]']"
# 大当り履歴データ
xpath_BONUSHIS = "//*[@id='menu_link']//*[contains(text(), '大当り履歴データ')]"

# 承諾
goToCommon(driver, xpath_agree)

# P新世紀エヴァンゲリオン１５　未来への咆哮 [40]
goToCommon(driver, xpath_EVAXX)
print('P新世紀エヴァンゲリオン１５　未来への咆哮 [40]')

# 大当り履歴データ
goToCommon(driver, xpath_BONUSHIS)

###########################################################################################################################################
dateFlg = 1
strTaiNoT = 941
###########################################################################################################################################
dateFlgT = '前日'
dateFlgT = f"{dateFlg}日前" if dateFlg > 1 else dateFlgT
print(dateFlgT)

adate = getFormatDate(dateFlg)
print(adate)

if strTaiNoT > 970:
    # 次へ
    goToNextPage(driver)
for strTaiNo in range(strTaiNoT,981):
    # 台移動
    getDataForBan(driver,strTaiNo,adate,dateFlgT)
    if strTaiNo == 970:
        # 次へ
        goToNextPage(driver)
wairForRandom()
piaDB = RAKUENDBNew()
piaDB.getRen(adate,1)
print('OK')