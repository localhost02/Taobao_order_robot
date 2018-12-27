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
import requests
# from http import cookiejar
from urllib2 import urlopen
from bs4 import BeautifulSoup

# from cn.localhost01.util.str_util import print_msg
from util.str_util import print_msg



# 对于py2，将ascii改为utf8
reload(sys)
sys.setdefaultencoding('utf8')


class TaobaoClimber:
    def __init__(self, username, password):
        self.__session = requests.Session()
        self.__username = username
        self.__password = password
        # 用户信息
    driver = None
    action = None
    # 是否登录
    __is_logined = False
    # 登陆URL
    __login_path = "https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d9nrX75I&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F"
    # 卖家待发货订单URL
    __orders_path = "https://trade.taobao.com/trade/itemlist/list_sold_items.htm?action=itemlist/SoldQueryAction&event_submit_do_query=1&auctionStatus=PAID&tabCode=waitSend"
    orders_path = "https://trade.taobao.com/trade/itemlist/list_sold_items.htm?action=itemlist/SoldQueryAction&event_submit_do_query=1&auctionStatus=PAID&tabCode=waitSend"
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
        cookies = self.driver.get_cookies()  # 导出cookie
        for cookie in cookies:
            self.__session.cookies.set(cookie['name'], cookie['value'])  # 转换cookies
        # self.driver.get("https://myseller.taobao.com/home.htm")
        # self.driver.get("https://trade.taobao.com/trade/itemlist/list_sold_items.htm?action=itemlist/SoldQueryAction&event_submit_do_query=1&auctionStatus=PAID&tabCode=waitSend")
        # self.driver.find_element_by_link_text("已卖出的宝贝").click()
        time.sleep(2)
        # html = BeautifulSoup(self.driver.page_source, "html5lib")
        # order_div_list = html.find_all("div", {"class": "item-mod__trade-order___2LnGB trade-order-main"})
        # print order_div_list
        return True

    def __get_orders_page(self):
        # 1.bs4将资源转html
        self.driver.get("https://myseller.taobao.com/home.htm")
        self.driver.find_element_by_link_text("已卖出的宝贝").click()
        self.driver.refresh
        self.driver.switch_to_window(self.driver.window_handles[3])
        # self.driver.get(__orders_path)
        print self.driver.page_source
        html = BeautifulSoup(self.driver.page_source, "html.parser")
        # html = BeautifulSoup(self.driver.page_source, "html5lib")
        print html
        # 2.取得所有的订单div
        # order_div_list = html.find_all("div", {"class": "item-mod__trade-order___2LnGB trade-order-main"})
        order_div_list = html.find_all("div", {"class": "item-mod__trade-order___2LnGB trade-order-main"})

        # 3.遍历每个订单div，获取数据
        print order_div_list
        data_array = []
        for index, order_div in enumerate(order_div_list):
            print index, order_div
            # send_judge = order_div.find("div", {"class": "text-mod__link___1AAaX"})
            # print send_judge
            # # send_judge = self.driver.find_elements_by_class_name("卖家已发货")
            # if send_judge:
            #     continue
            order_id = order_div.find("input", attrs={"name": "orderid"}).attrs["value"]
            order_date = order_div.find("span",
                                        attrs={"data-reactid": re.compile(r"\.0\.5\.3:.+\.0\.1\.0\.0\.0\.6")}).text
            order_buyer = order_div.find("a", attrs={"class": "buyer-mod__name___S9vit"}).text
            # 4.根据订单id组合url，请求订单对应留言
            order_message = json.loads(self.__session.get(self.__message_path + order_id).text)['tip']
            data_array.append((order_id, order_date, order_buyer, order_message))
        return data_array

    def climb(self):
        # FIXME 没有真实订单的模拟测试，生产环境注释即可
        # order_test = [(u"留言: 820713556@qq.com"),]
        self.__session = requests.Session()
        # 切换回窗口
        self.driver.switch_to_window(self.driver.window_handles[0])  # _homepage
        result = []
        if self.__is_logined is False:
            if self.__login() is False:
                return result
            else:
                self.__is_logined = True
            while True:
                # 2.获取当前页面的订单信息
                time.sleep(2)  # 两秒等待页面加载
                _orders = self.__get_orders_page()
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
            return _orders

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
    def deliver_judge(self, orderId):
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
            # no_need_logistics_a = self.driver.find_element_by_xpath("//*[@id='dummyTab']/a")
            # print no_need_logistics_a
            # no_need_logistics_a.click()
            # self.driver.find_element_by_id("logis:noLogis").click()
            test = self.driver.find_element_by_id("logis:noLogis")
            print test
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




