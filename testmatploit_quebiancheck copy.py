# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get('https://www.d-deltanet.com/pc/D0301.do?pmc=22021004&clc=01&urt=400&pan=1')
time.sleep(5)
# 获取登录后的 cookie
# cookies = driver.get_cookies()
element = driver.find_element(By.ID, "model_link")
elements = element.find_elements(By.TAG_NAME, 'a')
# for e in elements:
print(elements[1].text)
# ｅ 新世紀エヴァンゲリオン ～はじまりの記憶～ [28]
elements[1].click()
time.sleep(2)

element1 = driver.find_element(By.ID, "menu_link")
elements1 = element1.find_elements(By.TAG_NAME, 'a')

time.sleep(2)
print(elements1[11].text)
# 大当り履歴データ
elements1[11].click()

elements2 = driver.find_element(By.CSS_SELECTOR, '.daiban')
time.sleep(2)
# for e in elements2:
#     print(e.text)
print(elements2.text)
elements2.click()
time.sleep(20)