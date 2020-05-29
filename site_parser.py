from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b

import time
import random
import re
import utils

from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import os

class Parser:
    def __init__(self,
                 driver_type='phantom',
                 browser_mode='headless'):
        from config import Config

        self.config = Config()
        self.driver = self.__set_browser_driver(driver_type, browser_mode)
        print("Parser instance created")


    def __set_browser_driver(self, driver_type, browser_mode):
        """
        Handling of browser driver type
        :return:
        """
        if driver_type == 'phantom':
            if self.config.os_type == "Windows":
                driver = webdriver.PhantomJS(executable_path='C:/Program Files (x86)/phantomjs/bin/phantomjs.exe',
                                             service_args=self.config.service_args,
                                             desired_capabilities=self.config.dcap,
                                             service_log_path=os.path.devnull)
                driver.set_window_size(1920, 1080)
            else:
                driver = webdriver.PhantomJS(service_args=self.config.service_args,
                                                  desired_capabilities=self.config.dcap,
                                             service_log_path=os.path.devnull)
                driver.set_window_size(1366, 768)

        elif driver_type == 'firefox':
            print('running firefox')
            from selenium.webdriver.firefox.options import Options
            firefox_options = Options()
            firefox_options.add_argument('--disable-logging')
            if browser_mode == 'headless':
                firefox_options.headless = True

            driver = webdriver.Firefox(firefox_options=firefox_options,
                                       executable_path=self.config.firefox_path,
                                       service_log_path=os.path.devnull)

        elif driver_type == 'chrome':
            from selenium.webdriver.chrome.options import Options
            print('running chrome')
            chrome_options = Options()

            if browser_mode == 'headless':
                chrome_options.headless = True

            driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=self.config.chrome_path)
                                       # desired_capabilities=self.config.dcap,
                                       # service_args=self.config.service_args)
        else:
            raise AttributeError('Driver type should be | phantom | firefox | chrome')

        return driver


    def parse_google(self):
        site = 'http://www.google.com'
        self.driver.get(site)
        print(self.driver.current_url)
        self.driver.save_screenshot(self.config.output_dir + 'test.png')
        self.driver.close()



class InstagramParser(Parser):



    if __name__ == '__main__':
        main()

    """docstrinzg for Parser"""
    def __init__(self, username:str, password:str):
        super(InstagramParser, self).__init__(driver_type='chrome', browser_mode = 'headless')
        self.username = username
        self.password = password

    def login(self):
        print('login')
        self.driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
        uid = WebDriverWait(self.driver,4).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(2) > div > label')))
        uid.click()
        uid.send_keys(self.username)

        pswd = self.driver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(3) > div > label > input')
        pswd.click()
        pswd.send_keys(self.password)

        btn = self.driver.find_element_by_css_selector('#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button > div')
        btn.click()
        self.driver.save_screenshot(self.config.output_dir + 'login.png')
        time.sleep(3)



    def get_followers(self, url='https://www.instagram.com/katlinamberg/'):
        self.driver.get(url)
        self.driver.save_screenshot(self.config.output_dir + 'followers.png')
        print('get followers')
        time.sleep(3)
        flw_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > header > section > ul > li:nth-child(2) > a')))
        flw_btn.click()
        time.sleep(3)
        self.popup = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]')))
        self.driver.save_screenshot(self.config.output_dir + 'popup.png')

        hrefs = []
        for h in range (11):
            time.sleep(1)
            print('scrolling')
            print(h)
            print('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)))
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight/{}'.format(str(11-h)), self.popup)
            if h == 2:
                break

        for i in range(1):
            time.sleep(2)
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', self.popup)
        self.popup = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]')))
        b_popup = b(self.popup.get_attribute('innerHTML'), 'html.parser')
        for p in b_popup.findAll('li', {'class': 'wo9IH'}):
            try:
                hlink = p.find_all('a')[0]['href']
                if 'div' in hlink:
                    return hrefs
                else:
                    hrefs.append(hlink)
            except:
                #print(p.find_all('a')[0])
                pass
        return hrefs

    def is_public(self):
        try:
            astate = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'rkEop')))
            if astate.text == 'This Account is Private':
                return False
            else:
                return True
        except:
            return True

    def like_post(self):
        self.driver.save_screenshot(self.config.output_dir + 'like post.png')
        print('Liking post')

        try:
            post = self.driver.find_element_by_css_selector('#react-root > section > main > div > div._2z6nI > article > div:nth-child(1) > div > div:nth-child(1) > div:nth-child(1)')
            html = post.get_attribute('innerHTML')
            h = b(html, 'html.parser')
            href = h.a['href']
            self.driver.get('https://www.instagram.com' + href)
            like_btn = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main > div > div.ltEKP > article > div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > svg')))
            like_btn.click()
        except:
            # ignore this page
            pass

    def follow_page(self):
        print('Following page')
        self.driver.save_screenshot(self.config.output_dir + 'following page.png')
        follow = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[2]')))
        f_text = follow.text
        if f_text.lower() == 'follow' or f_text.lower() == 'follow back':
            follow.click()
        elif f_text == 'already following':
            print('already following')
        self.driver.save_screenshot(self.config.output_dir + 'following page§.png')
        time.sleep(10)


    def start_parse(self):
        self.login()
        time.sleep(3)
        self.get_followers()
        time.sleep(3)
        self.is_public()
        time.sleep(3)
        self.like_post()
        time.sleep(3)
        self.follow_page()
        time.sleep(3)

        self.driver.close()
