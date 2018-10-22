# -*- coding: utf-8 -*-
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import sys
import os
import random
# from cn.localhost01.util.str_util import print_msg
from util.str_util import print_msg

reload(sys)
sys.setdefaultencoding('utf8')  # 对于py2，将ascii改为utf8

is_cmd_run = False
if len(sys.argv) == 2:  # cmd启动
    is_cmd_run = True


class MailSenderBrowser:
    def __init__(self, username, password, password2):
        self.__username = username
        self.__password = password
        self.__password2 = password2

    driver = None
    action = None

    # 是否登录
    __is_logined = False

    # 淘宝账户
    __username = ""
    # 登录密码
    __password = ""
    # 独立密码
    __password2 = ""
    # 登陆URL
    __login_path = "https://mail.qq.com/"

    def __login(self):
        # 1.进入登陆页面
        try:
            self.driver.get(self.__login_path)
        except exceptions.TimeoutException:  # 当页面加载时间超过设定时间，JS来停止加载
            self.driver.execute_script('window.stop()')

        # 2.切换到登录iframe
        login_frame = self.driver.find_element_by_id("login_frame")
        self.driver.switch_to_frame(login_frame)

        switch_login_a = self.driver.find_element_by_id("switcher_plogin")
        switch_login_a.click()
        username_input = self.driver.find_element_by_id("u")
        username_input.clear()
        # 点击，防止腾讯判断机器人操作而网络繁忙
        username_input.click()
        username_input.send_keys(self.__username)
        password_input = self.driver.find_element_by_id("p")
        password_input.clear()
        # 点击，防止腾讯判断机器人操作而网络繁忙
        password_input.click();
        password_input.send_keys(self.__password)
        self.driver.find_element_by_id("login_button").click()
        time.sleep(2)
        self.driver.switch_to_default_content()
        try:
            password2_input = self.driver.find_element_by_id("pp")
            if self.__password2 is "":
                print_msg("邮箱登录失败，请在__init__.py中配置邮箱独立密码！")
                return False
            password2_input.send_keys(self.__password2)
            self.driver.find_element_by_id("btlogin").submit()
        except exceptions.NoSuchElementException:
            pass
        time.sleep(2)
        try:
            self.driver.find_element_by_id("useralias")
            return True
        except exceptions.NoSuchElementException:
            return False

    def send(self, user_to, local_path):
        # 切换回窗口
        self.driver.switch_to_window(self.driver.window_handles[2])

        if self.__is_logined is False:
            count = 0
            while count < 7:
                count += 1
                if self.__login() is False:
                    continue
                else:
                    self.__is_logined = True
                    break
            if count >= 7:
                return "邮箱登录失败！"

        # 1.写信
        write_a = self.driver.find_element_by_id("composebtn")
        write_a.click()
        time.sleep(1)
        # 2.输入邮件信息
        form_iframe = self.driver.find_element_by_id("mainFrame")
        self.driver.switch_to_frame(form_iframe)
        user_to_input = self.driver.find_element_by_xpath("//*[@id='toAreaCtrl']/div[2]/input")
        user_to_input.send_keys(user_to)
        subjuct_input = self.driver.find_element_by_id("subject")
        subjuct_input.send_keys(u"【尊贵的淘宝买家】")

        # 3.超大附件上传
        self.driver.find_element_by_class_name("ico_attbig").click()
        time.sleep(2)
        self.driver.switch_to_default_content()
        upload_iframe = self.driver.find_element_by_id("ftnupload_attach_QMDialog__dlgiframe_")
        self.driver.switch_to_frame(upload_iframe)
        upload_input = self.driver.find_element_by_xpath("//*[@class='upload_btn_center']/a")
        upload_input.click()

        time.sleep(2)
        local_path = local_path.replace("//", "\\").replace("/", "\\").decode('utf-8').encode('gbk')
        if is_cmd_run:  # 外部cmd批处理文件启动该程序
            os.system(os.path.abspath("./cn/localhost01/mail/upload.exe") + r' "firefox" "' + local_path + '"')
        else:  # 开发软件启动该程序
            if os.path.exists(os.path.abspath("./mail/upload.exe")):  # main.py位置启动
                os.system(os.path.abspath("./mail/upload.exe") + r' "firefox" "' + local_path + '"')
            else:  # 本文件的main方法位置启动
                os.system(os.path.abspath("upload.exe") + r' "firefox" "' + local_path + '"')
        # 4.等待上传
        while True:
            try:
                speed = self.driver.find_element_by_xpath("//*[@class='probar_tips']/span[2]/span[1]").text
                if speed == "完成":
                    break
            except exceptions.NoSuchElementException:
                pass
            time.sleep(3)
        self.driver.find_element_by_xpath("//*[@id='operate']/a[1]").click()

        # 6.发送
        self.driver.switch_to_default_content()
        form_iframe = self.driver.find_element_by_id("mainFrame")
        self.driver.switch_to_frame(form_iframe)
        self.driver.find_element_by_xpath("//*[@id='toolbar']/div/a[1]").click()

        time.sleep(1)
        self.driver.switch_to_default_content()
        try:
            error = self.driver.find_element_by_class_name("errmsg").text
            return error
        except exceptions.NoSuchElementException:
            return None


if __name__ == "__main__":
    # 初始化
    MailSenderBrowser.driver = webdriver.Firefox()  # 应将浏览器驱动放于python根目录下，且python已配置path环境变量
    MailSenderBrowser.action = ActionChains(MailSenderBrowser.driver)
    MailSenderBrowser.driver.maximize_window()  # 浏览器最大化
    MailSenderBrowser.driver.execute_script("window.open('')")
    MailSenderBrowser.driver.execute_script("window.open('')")

    sender_browser = MailSenderBrowser("QQ邮箱账号", "登录密码", "授权码")
    sender_browser.send("接收邮箱", r"C:\Robot_Download\新建文本文档.txt")
