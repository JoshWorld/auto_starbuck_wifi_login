#!/usr/bin/env python3

import time
import os.path
from selenium import webdriver

curdir = os.path.join(os.path.dirname(__file__))

# 스타벅스 로그인 과정 자동 입력기
# Selenium을 이용해서 웹브라우저를 하나 만들고 웹브라우저를 통해서
# 자동 로그인한다.
class StarbuckPage(object):
    def __init__(self):
        self.driver = self._create_webdriver()

    def _create_webdriver(self):
        driver = webdriver.Chrome(os.path.join(curdir, 'webdriver', "chromedriver"))
        return driver

    def current_url(self):
        return self._exec_js('return location.toString()')

    def go_url(self, url):
        self.driver.get(url)

    def _exec_js(self, js):
        try:
            ret = self.driver.execute_script(js)
            return ret
        except Exception as e:
            print(type(e))
            print(e)

    def clickAccessWifi(self):
        while True:
            # 확인 버튼 누르기
            element = self.driver.find_element_by_css_selector(".goWifi a")
            if element:
                element.click()
                break
            
            time.sleep(0.5)

    def inputPersonInfo(self, person):
        "필요한 정보들을 입력한다."
        
        element = self.driver.find_element_by_css_selector("#userNm")
        element.send_keys(person.name)
        element = self.driver.find_element_by_css_selector("#cust_email_addr")
        element.send_keys(person.email)
        element = self.driver.find_element_by_css_selector("#kt_btn")
        element = self.driver.find_element_by_css_selector("#agree1")
        if element:
            element.click()
        element = self.driver.find_element_by_css_selector("input[name=cust_hp_no]")
        element.send_keys(person.tel)

        # SEND
        self._exec_js('goAct()')

def auto_login(me):
    page = StarbuckPage()
    page.go_url('http://www.naver.com')
    
    while True:
        url = page.current_url()

        # 바로 원하는 페이지로 가게 되면
        if url == 'http://www.naver.com/':
            return True

        # Login 페이지로 넘어가면
        if url.startswith('http://first.wifi.olleh.com/'):
            # 혹시 영어 페이지로 이동하도록
            page.go_url('http://first.wifi.olleh.com/starbucks/index_en_new.html')
            sleep(0.5)

    # 확인 버튼 클릭
    page.clickAccessWifi()
    time.sleep(0.5)

    # 사용자 데이터 입력하고 
    page.inputPersonInfo(me)
    while True:
        url = page.current_url()
        if url == 'http://www.istarbucks.co.kr:8000/wireless/wireless.asp':
            return True
        time.sleep(0.5)

if __name__ == '__main__':
    import os.path
    import json

    #{{{ 여기서를 자신에게 맞게 수정
    my_data = json.load(open(os.path.expanduser("~/.me/me.json"), encoding='utf-8'))

    info = {
        "name": my_data["name"],
        "email": my_data["email"],
        "tel": my_data["tel"]
    }
    #}}}
    
    if auto_login(info):
        print("[!] Enjoy starbuck life")


