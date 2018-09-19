# -*- coding: utf-8 -*-
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import random
import re
import requests
import json
import sys
from bs4 import BeautifulSoup
# from cn.localhost01.util.str_util import print_msg
from util.str_util import print_msg

# 对于py2，将ascii改为utf8
reload(sys)
sys.setdefaultencoding('utf8')


class TaobaoClimber:
    def __init__(self, username, password):
        self.__username = username
        self.__username = username
        self.__password = password

    driver = None
    action = None

    # 是否登录
    __is_logined = False

    # 登陆URL
    # __login_path = "https://auth.alipay.com/login/index.htm?loginScene=7&goto=https%3A%2F%2Fauth.alipay.com%2Flogin%2Ftaobao_trust_login.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.taobao.com%252Fmember%252Falipay_sign_dispatcher.jhtml%253Ftg%253D&params=VFBMX3JlZGlyZWN0X3VybD0%3D"


    __login_path = "https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9nrX75I&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F"
    # 卖家待发货订单URL
    __orders_path = "https://trade.taobao.com/trade/itemlist/list_sold_items.htm?action=itemlist/SoldQueryAction&event_submit_do_query=1&auctionStatus=PAID&tabCode=waitSend"
    # 卖家正出售宝贝URL
    __auction_path = "https://sell.taobao.com/auction/merchandise/auction_list.htm"
    # 卖家仓库中宝贝URL
    __repository_path = "https://sell.taobao.com/auction/merchandise/auction_list.htm?type=1"
    # 卖家确认发货URL
    __deliver_path = "https://wuliu.taobao.com/user/consign.htm?trade_id="
    # 卖家退款URL
    __refunding_path = "https://trade.taobao.com/trade/itemlist/list_sold_items.htm?action=itemlist/SoldQueryAction&event_submit_do_query=1&auctionStatus=REFUNDING&tabCode=refunding"
    # 请求留言URL
    __message_path = "https://trade.taobao.com/trade/json/getMessage.htm?archive=false&biz_order_id="
    # 淘宝首页
    _homepage = "https://www.taobao.com/?spm=a1z02.1.1581860521.1.584d782d3EbMH6"
    # requests会话
    __session = None

    def __login(self):
        self.driver.get(self.__login_path)
        self.driver.maximize_window()
        self.driver.find_element_by_id("J_Quick2Static").click()
        self.driver.find_element_by_class_name("alipay-login").click()
        self.driver.find_element_by_xpath("//li[@data-status='show_login']").click()

        for username_ in self.__username:
            self.driver.find_element_by_id("J-input-user").send_keys(username_)
            time.sleep(0.2)
        for password_ in self.__password:
            self.driver.find_element_by_id("password_rsainput").send_keys(password_)
            time.sleep(0.2)
        # time.sleep(10)
        self.driver.find_element_by_id("J-login-btn").click()
        time.sleep(2)
        return True


    def climb(self):
        # 切换回窗口
        self.driver.switch_to_window(self.driver.window_handles[0])  # _homepage
        # result = []
        # if self.__is_logined is False:
        #     if self.__login() is False:
        #         print ("test10....")
        #     # return result
        #     else:
        #         print("...is true")
        #         self.__is_logined = True
        # if self.__is_logined is False:
        #     self.driver.find_element_by_link_name(u"淘宝网首页");
        if self.__login() is True:
           self.driver.get(self.__orders_path)
        while True:
            # 2.获取当前页面的订单信息
            time.sleep(2)  # 两秒等待页面加载
            _orders = self.__get_orders_page()
            result.extend(_orders)
            try:
                # 3.获取下一页按钮
                next_page_li = self.driver.find_element_by_class_name("pagination-next")
                # 4.判断按钮是否可点击，否则退出循环
                next_page_li.get_attribute("class").index("pagination-disabled")
                # 到达最后一页
                break
            except ValueError:
                # 跳转到下一页
                print(next_page_li.find_element_by_tag_name("a").text)
                next_page_li.click()
                time.sleep(1)
            except exceptions.NoSuchElementException:
                pass
        return result

    # def unshelve(self):
    #     # 切换回窗口
    #     self.driver.switch_to_window(self.driver.window_handles[0])
    #
    #     # if self.__is_logined is False:
    #     #     if self.__login() is False:
    #     #         return False
    #     #     else:
    #     self.__is_logined = True
    #
    #     try:
    #         # 1.进入正出售宝贝页面
    #         self.driver.get(self.__auction_path)
    #         # 2.点击下架
    #         choose_checkbox = self.driver.find_element_by_xpath(
    #             "//*[@id='J_DataTable']/table/tbody[1]/tr[1]/td/input[1]")
    #         choose_checkbox.click()
    #         unshelve_btn = self.driver.find_element_by_xpath(
    #             "//*[@id='J_DataTable']/div[2]/table/thead/tr[2]/td/div/button[2]")
    #         unshelve_btn.click()
    #         return True
    #     except:
    #         return False

    def shelve(self):
        # 切换回窗口
        try:
            self.driver.switch_to_window(self.driver.window_handles[0])
        except exceptions:
            print exceptions

        if self.__is_logined is False:
            if self.__login() is False:
                return False
            else:
                self.__is_logined = True

        # 1.进入仓库宝贝页面
        self.driver.get(self.__repository_path)
        # 2.点击上架
        try:
            choose_checkbox = self.driver.find_element_by_xpath("//*[@id='J_DataTable']/table/tbody[1]/tr[1]/td/input")
            choose_checkbox.click()
            shelve_btn = self.driver.find_element_by_xpath("//*[@id='J_DataTable']/div[3]/table/tbody/tr/td/div/button[2]")
            shelve_btn.click()
        except exceptions.NoSuchElementException:
            pass

    def delivered(self, orderId):
        # 切换回窗口
        self.driver.switch_to_window(self.driver.window_handles[0])

        if self.__is_logined is False:
            if self.__login() is False:
                return False
            else:
                self.__is_logined = True
        try:
            # 1.进入确认发货页面
            self.driver.get(self.__deliver_path + orderId)
            no_need_logistics_a = self.driver.find_element_by_xpath("//*[@id='dummyTab']/a")
            no_need_logistics_a.click()
            self.driver.find_element_by_id("logis:noLogis").click()
            time.sleep(1)
            return True
        except:
            return False

    def exists_refunding(self):
        # 切换回窗口
        self.driver.switch_to_window(self.driver.window_handles[0])

        if self.__is_logined is False:
            if self.__login() is False:
                return False
            else:
                self.__is_logined = True
        try:
            # 1.进入退款页面
            self.driver.get(self.__refunding_path)
            self.driver.find_element_by_class_name("item-mod__trade-order___2LnGB trade-order-main")
            return True
        except exceptions.NoSuchElementException:
            return False




# if __name__ == '__main__':
#     # 初始化
#     TaobaoClimber.driver = webdriver.Firefox()  # 应将浏览器驱动放于python根目录下，且python已配置path环境变量
#     TaobaoClimber.action = ActionChains(TaobaoClimber.driver)
#     TaobaoClimber.driver.maximize_window()  # 浏览器最大化
#     TaobaoClimber.driver.execute_script("window.open('')")
#     TaobaoClimber.driver.execute_script("window.open('')")
#
#     climber = TaobaoClimber(u"淘宝账户", "登录密码")
#     while True:
#         # 循环爬取订单
#         orders = climber.climb()
#         for order in orders:
#             print_msg("订单号：%s\t订单日期：%s \t买家：%s\t备注：%s" % order)
#         # 每30秒抓一次
#         time.sleep(30)
