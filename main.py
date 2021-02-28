from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys

import vlc
from pynput.keyboard import Key, Controller

import subprocess
import time
import random
from config import *


class Bot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def run(self):
        self.wakingup()
        self.aang()
        self.spotify()
        self.driver.close()

    def spotify(self):
        # TODO: Ensure web player plays at twice speed
        self.driver.get('https://open.spotify.com/')
        time.sleep(2)

        # Login
        self.driver.find_element_by_xpath(
            '/html/body/div[3]/div/div[2]/div[1]/header/div[5]/button[2]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/form/div[1]/div/input').send_keys(work_email)
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/form/div[2]/div/input').send_keys(password)
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div/form/div[4]/div[2]/button').click()
        time.sleep(4)

        # Navigate to and play the 'not overthinking' podcast for 30 mins
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div[2]/nav/div[1]/ul/li[2]/a').click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div[2]/div[1]/header/div[3]/div/div/input').send_keys('not overthinking')
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/div/div/div/section[1]/div[2]/div/div/div/div[4]').click()
        time.sleep(2)
        self.driver.find_element_by_xpath(
            '/html/body/div[4]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[2]/div[2]/div/button').click()

        # TODO: time.sleep(30 * 60)
        time.sleep(5)

    def aang(self):
        aang = vlc.MediaPlayer("./chakra.mp3")
        aang.audio_set_volume(100)
        aang.play()
        # TODO:
        # duration = aang.get_length() / 1000
        # time.sleep(duration)
        time.sleep(5)
        aang.stop()

    def wakingup(self):
        self.driver.get('https://app.wakingup.com/')
        time.sleep(2)

        # Navigate to Waking up and login
        self.driver.find_element_by_xpath(
            '//*[@id="root"]/div[1]/div/div[1]/div/form/div/div/div/input').send_keys(work_email)
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/form/button').click()
        time.sleep(4)

        # Open a new tab and get the login code
        self.driver.execute_script(
            '''window.open("https://www.google.com","_blank");''')
        time.sleep(3)

        window_before = self.driver.window_handles[0]
        window_after = self.driver.window_handles[1]
        self.driver.switch_to.window(window_after)
        login_code = self.get_login_code(window_before, window_after)
        self.driver.execute_script('''window.close();''')
        self.driver.switch_to.window(window_before)

        # Return to Waking up and play the daily meditation
        signin_area = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div')
        codeinputs = signin_area.find_elements_by_tag_name('input')
        for i in range(len(login_code)):
            codeinputs[i].send_keys(login_code[i])
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/form/button').click()
        time.sleep(2)
        # TODO: Pause here and play some kind of alarm to actually wake me up
        self.driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div[2]').click()
        # TODO: time.sleep((60 * 10) + 15)
        time.sleep(5)

    def get_login_code(self, before, after):
        self.driver.get(
            'https://mail.yohanderose.dev/SOGo/so/contact@yohanderose.dev/Mail/view#!/Mail/0/INBOX')
        time.sleep(2)

        # Login to personal email server
        self.driver.find_element_by_xpath(
            '/html/body/main/md-content/div[2]/div/form/md-input-container[1]/input').send_keys(personal_email)
        self.driver.find_element_by_xpath(
            '/html/body/main/md-content/div[2]/div/form/md-input-container[2]/input').send_keys(password)
        self.driver.find_element_by_xpath(
            '/html/body/main/md-content/div[2]/div/form/div[3]/button[2]').click()
        time.sleep(8)

        # Loop and wait for verification email to arrive
        login_code = ''
        counter = 0
        while True:
            counter += 1
            try:
                # Open the most recently received email
                self.driver.find_element_by_xpath(
                    '/html/body/main/section/div/div[1]/md-content/md-virtual-repeat-container/div/div[2]/md-list/md-list-item/div/button').click()
                time.sleep(2)
                mail_area = self.driver.find_element_by_xpath(
                    '/html/body/main/section/div/div[2]/div/div[1]/md-card/md-card-content/div[6]/div/div/div/div/div')
                mail_contents = mail_area.find_elements_by_tag_name('p')[
                    0].text

                login_code = mail_contents.split('\n')[2]

                # Delete verification mail
                self.driver.find_element_by_xpath(
                    '/html/body/main/section/div/div[2]/div/div[1]/md-card/md-card-actions/button[8]').click()

                break
            except Exception as e:
                if counter % 4 == 0:
                    self.driver.switch_to.window(before)
                    time.sleep(10)
                    self.driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[1]/div/form/p/button').click()
                    self.driver.switch_to.window(after)
                time.sleep(2)
                self.driver.find_element_by_xpath(
                    '/html/body/main/section/div/div[1]/md-toolbar[2]/div/button[2]').click()

        return login_code


bot = Bot()
bot.run()
