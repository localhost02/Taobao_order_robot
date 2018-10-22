# -*- coding: utf-8 -*-
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import re
import os
import requests
import sys
# from cn.localhost01.util.str_util import print_msg
from util.str_util import print_msg

reload(sys)
sys.setdefaultencoding('utf8')  # 对于py2，将ascii改为utf8


class CsdnDownloader:
    def __init__(self, username, password):
        self.__username = username
        self.__password = password

    driver = None
    action = None

    # CSDN账号
    __username = ""
    # 登录密码
    __password = ""
    # 会话
    __session = requests.session()
    # 下载次数
    download_count = 0

    def download(self, remote_url, local_dir):
        # 切换回窗口
        self.driver.switch_to_window(self.driver.window_handles[1])

        # 1.进入下载页面
        try:
            self.driver.get(remote_url)
        except exceptions.TimeoutException:  # 当页面加载时间超过设定时间，JS来停止加载
            self.driver.execute_script('window.stop()')

        # 2.判断是否需要登录
        try:
            self.driver.find_element_by_xpath("//*[@id='download_top']/div[4]/a[2 and text()='立即下载']")  # 未登录
            self.__login()
            time.sleep(2)
        except exceptions.NoSuchElementException:  # 已登录
            pass

        # 下载次数+1
        self.download_count += 1

        count = 0
        while count < 3:
            count += 1
            # 3.下载
            vip_download_a = self.driver.find_element_by_class_name("direct_download")
            vip_download_a.click()

            download_url = self.driver.find_element_by_id("vip_btn").get_attribute("href")
            source = self.__session.get(download_url, stream=True)

            # 3.1获取下载名
            filename = re.findall(r".*\"(.*)\"$", source.headers.get("Content-Disposition", "\"None\""))[0]
            if filename == "None":
                continue
            filename = re.sub("\s", "_", filename)
            # 3.2创建本地文件
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            _local_path = local_dir + filename
            # 3.3分段下载
            local_file = open(_local_path.encode("gbk"), "wb")
            for file_buffer in source.iter_content(chunk_size=512):
                if file_buffer:
                    local_file.write(file_buffer)
            return _local_path
        return None

    def __login(self):
        vip_download_a = self.driver.find_element_by_class_name("direct_download")
        vip_download_a.click()
        time.sleep(2)

        # 1.切换到登录iframe
        form_iframe = self.driver.find_element_by_xpath("//*[@id='loginWrap']/iframe")
        self.driver.switch_to_frame(form_iframe)
        # 2.进行登录
        change_login_button = self.driver.find_element_by_class_name("login-user__active")
        change_login_button.click()
        time.sleep(2)

        username_input = self.driver.find_element_by_id("username")
        username_input.send_keys(self.__username)
        password_input = self.driver.find_element_by_id("password")
        password_input.send_keys(self.__password)
        submit_input = self.driver.find_element_by_class_name("logging")
        submit_input.submit()
        time.sleep(3)
        # 3.保存cookies
        list_cookies = self.driver.get_cookies()
        cookies = {}
        for s in list_cookies:
            cookies[s['name']] = s['value']
            requests.utils.add_dict_to_cookiejar(self.__session.cookies, cookies)  # 将获取的cookies设置到session

        self.driver.switch_to_default_content()  # 返回主页面


if __name__ == '__main__':
    # 初始化
    CsdnDownloader.driver = webdriver.Firefox()  # 应将浏览器驱动放于python根目录下，且python已配置path环境变量
    CsdnDownloader.action = ActionChains(CsdnDownloader.driver)
    CsdnDownloader.driver.maximize_window()  # 浏览器最大化
    CsdnDownloader.driver.execute_script("window.open('')")
    CsdnDownloader.driver.execute_script("window.open('')")

    count = 0
    while True:
        down_loader = CsdnDownloader('CSDN VIP账号', 'CSDN VIP密码')
        local_path = down_loader.download('http://download.csdn.net/download/lqkitten/10113904', "c://Robot_Download/")
        if local_path is not None:
            print_msg("下载完成，本地路径：" + local_path + "，重试次数：" + str(count))
            break
        count += 1
