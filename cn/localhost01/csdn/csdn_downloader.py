# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import time
import re
import os
import requests
import sys
from cn.localhost01.util.str_util import print_msg

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
    # 是否登录
    __is_logined = False
    __login_url = "https://passport.csdn.net/account/login"

    def download(self, remote_url, local_dir):

        # 1.是否登录
        if not self.__is_logined:
            self.__login()

        # 下载次数+1
        self.download_count += 1

        count = 0
        while count < 3:
            count += 1

            # 2.解析真实下载URL
            html_text = self.__session.get(remote_url).text
            html = BeautifulSoup(html_text, "html5lib")
            real_url = html.find("a", id="vip_btn").attrs["href"]

            # 3.下载
            source = self.__session.get(real_url)

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
        # 1.请求登录页面，获取登录前的必要参数
        html_text = requests.get(self.__login_url).text
        html = BeautifulSoup(html_text, "html5lib")
        form = html.find("form", id="fm1")
        location = form.attrs["action"]  # 每次表单action后面有个随机数
        lt = form.select("input[name=lt]")[0].attrs["value"]
        execution = form.select("input[name=execution]")[0].attrs["value"]
        _eventId = form.select("input[name=_eventId]")[0].attrs["value"]
        params = {"username": self.__username, "password": self.__password, "lt": lt, "execution": execution,
                  "_eventId": _eventId}

        time.sleep(1)  # CSDN貌似判断机器人，睡眠一下，增加成功率

        # 2.进行登录
        response = requests.post(location, params)

        # 3.保存cookies
        self.__session.cookies = response.cookies
        self.__is_logined = True


if __name__ == '__main__':
    down_loader = CsdnDownloader("test", "123456")
    local_path = down_loader.download('http://download.csdn.net/download/lqkitten/10113904', "c://Robot_Download/")
    if local_path is not None:
        print_msg("CSDN下载完成，本地路径：" + local_path)
    else:
        print_msg("CSDN下载失败")
