#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
import base64
import hashlib
import requests


URL = 'https://app.slashme.com/n/vnsratMMPFqcc8omW'
PIC_PATH = os.path.join(os.path.expanduser('~'), 'Desktop/weeklyreport')
PIC_NAME = 'screenshot.png'


def screenshot_web(url=URL, path=PIC_PATH, name=PIC_NAME):
    if not os.path.exists(path):
        os.makedirs(path)
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(3)
    user_name = browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Cancel'])[1]/following::input[1]")
    password = browser.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Cancel'])[1]/following::input[2]")
    user_name.clear
    user_name.send_keys("pangshengfang@126.com")
    password.clear
    password.send_keys("aiggie01")
    password.send_keys(Keys.RETURN)
    time.sleep(10)
    browser.find_element_by_xpath('//li[@class="collection-item dropzone-item drag-item drag-handle"][last()]').click()
    time.sleep(5)
    report = browser.find_element_by_xpath('//div[@class="nest-list"]')
    left = report.location['x']
    top = report.location['y']
    elementWidth = report.location['x'] + report.size['width']
    elementHeight = report.location['y'] + report.size['height']
    pic_path = os.path.join(os.path.join(path, name))
    print(pic_path)
    if browser.save_screenshot(pic_path):
        picture = Image.open(pic_path)
        picture = picture.crop((left, top, elementWidth, elementHeight))
        picture.save(pic_path)
        print('Done!')
    else:
        print('Failed!')
    browser.close()

def send_to_WX():
    if not os.path.exists("～/Desktop/weeklyreport/screenshot.png"):
        return 0
    fd = open("～/Desktop/weeklyreport/screenshot.png", "rb")
    fcont = fd.read()
    fmd5 = hashlib.md5(fcont)
    base64_data = base64.b64encode(fcont).decode()
    print(fmd5.hexdigest())
    fmd5_str = str(fmd5.hexdigest())
    base64_data_str = str(base64_data)
    print(fmd5_str)
    print(base64_data_str)
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=3c7877ac-7a17-4c29-9d9d-3b42174544e1'
    headers = {'Content-Type': 'application/json'}
    payload_pic = {
        "msgtype": "image",
        "image": {
            "base64": base64_data_str,
            "md5": fmd5_str
        }
    }
    payload_text = {
        "msgtype": "text",
        "text": {
            "content": "还没有提交周报的小伙伴，请速度提交噢"
        }
    }
    r1 = requests.post(url, json=payload_pic, headers=headers)
    r2 = requests.post(url, json=payload_text, headers=headers)
    print(r1.text)
    print(r2.text)

if __name__ == '__main__':
    screenshot_web()
    send_to_WX()