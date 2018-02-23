# -*- coding: utf-8 -*-
from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import re
import requests
import json
import sys
from bs4 import BeautifulSoup
from cn.localhost01.util.str_util import print_msg
from cn.localhost01.__init__ import delay_wait

# 对于py2，将ascii改为utf8
reload(sys)
sys.setdefaultencoding('utf8')

# driver = webdriver.Chrome()
driver = webdriver.Firefox()  # 应将浏览器驱动放于python根目录下，且python已配置path环境变量
action = ActionChains(driver)
driver.maximize_window()  # 浏览器最大化
driver.set_page_load_timeout(delay_wait)  # 设定页面加载限制时间


class TaobaoClimber:
    def __init__(self, username, password):
        self.__session = requests.Session()
        self.__username = username
        self.__password = password

    # 是否登录
    __is_logined = False

    # 淘宝账户
    __username = ""
    # 登录密码
    __password = ""
    # 登陆URL
    __login_path = "https://login.taobao.com/member/login.jhtml"
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
    # requests会话
    __session = None

    def __login(self):
        # 1.登陆
        try:
            driver.get(self.__login_path)
        except exceptions.TimeoutException:  # 当页面加载时间超过设定时间，JS来停止加载
            driver.execute_script('window.stop()')

        count = 0
        while count < 5:  # 重试5次
            count += 1
            if self.__login_one() is True:
                break
        if count == 5:
            return False

        # 2.保存cookies
        # driver.switch_to_default_content() #需要返回主页面，不然获取的cookies不是登陆后cookies
        list_cookies = driver.get_cookies()
        cookies = {}
        for s in list_cookies:
            cookies[s['name']] = s['value']
            requests.utils.add_dict_to_cookiejar(self.__session.cookies, cookies)  # 将获取的cookies设置到session
        return True

    def __login_one(self):
    	
        try:
            # 1.点击密码登录，切换到密码登录模式 默认是二维码登录
            username_login_btn = driver.find_element_by_xpath("//a[@class='forget-pwd J_Quick2Static']")
            if username_login_btn.is_displayed() is True:
                username_login_btn.click()
        except exceptions.ElementNotInteractableException:
            pass

        # 2.获取账户、密码输入框
        username_input = driver.find_element_by_id("TPL_username_1")
        password_input = driver.find_element_by_id("TPL_password_1")
        # 3.为账户、密码赋值
        username_input.clear()
        username_input.send_keys(self.__username)
        password_input.send_keys(self.__password)
        # 4.取得滑块所在div，判断是否display 一般首次登陆不需要滑块验证
        slide_div = driver.find_element_by_id("nocaptcha")
        if slide_div.is_displayed() is True:
            retry = 0
            while retry < 5:
                retry += 1
                slide_span = driver.find_element_by_id("nc_1_n1z")  # 取得滑块span
                action.click_and_hold(slide_span)  # 鼠标左键按住span
                action.move_by_offset(258, 0)  # 向右拖动258像素完成验证
                action.perform()
                time.sleep(1)
                action.reset_actions()  # 页面进行了刷新，需要清除action之前存储的elements
                try:
                    slide_refresh = driver.find_element_by_xpath(
                        "//div[@id='nocaptcha']/div/span/a")  # 页面没有滑块，而是“点击刷新再来一次”
                    slide_refresh.click()
                except exceptions.NoSuchElementException:  # 滑动成功
                    break

        # 5.获取登陆按钮，并点击登录
        submit_btn = driver.find_element_by_id("J_SubmitStatic")
        submit_btn.click()
        # 6.根据提示判断是否登录成功
        try:
            message = driver.find_element_by_id("J_Message").find_element_by_class_name("error")
            if message.text == u"为了你的账户安全，请拖动滑块完成验证":
                return False
        except exceptions.NoSuchElementException:
            pass

        # 7.有时检测当前环境是否异常，此时休眠一段时间让它检测
        try:
            driver.find_element_by_id("layout-center")
        except exceptions.NoSuchElementException:
            time.sleep(9)

        return True

    def __get_orders_page(self):
        # 1.bs4将资源转html
        html = BeautifulSoup(driver.page_source, "html5lib")
        # 2.取得所有的订单div
        order_div_list = html.find_all("div", {"class": "item-mod__trade-order___2LnGB trade-order-main"})
        # 3.遍历每个订单div，获取数据
        data_array = []
        for index, order_div in enumerate(order_div_list):
            order_id = order_div.find("input", attrs={"name": "orderid"}).attrs["value"]
            order_date = order_div.find("span",
                                        attrs={"data-reactid": re.compile(r"\.0\.5\.3:.+\.0\.1\.0\.0\.0\.6")}).text
            order_buyer = order_div.find("a", attrs={"class": "buyer-mod__name___S9vit"}).text
            # 4.根据订单id组合url，请求订单对应留言
            order_message = json.loads(self.__session.get(self.__message_path + order_id).text)['tip']
            data_array.append((order_id, order_date, order_buyer, order_message))
        return data_array

    def climb(self):
        result = []

        if self.__is_logined is False:
            if self.__login() is False:
                return result
            else:
                self.__is_logined = True

        # 1.进入待发货订单页面
        driver.get(self.__orders_path)
        while True:
            # 2.获取当前页面的订单信息
            time.sleep(2)  # 两秒等待页面加载
            _orders = self.__get_orders_page()
            result.extend(_orders)
            try:
                # 3.获取下一页按钮
                next_page_li = driver.find_element_by_class_name("pagination-next")
                # 4.判断按钮是否可点击，否则退出循环
                next_page_li.get_attribute("class").index("pagination-disabled")
                # print_msg("到达最后一页")
                break
            except ValueError:
                # print_msg("跳转到下一页")
                print(next_page_li.find_element_by_tag_name("a").text)
                next_page_li.click()
                time.sleep(1)
            except exceptions.NoSuchElementException:
                pass
        return result

    def unshelve(self):

        if self.__is_logined is False:
            if self.__login() is False:
                return False
            else:
                self.__is_logined = True

        try:
            # 1.进入正出售宝贝页面
            driver.get(self.__auction_path)
            # 2.点击下架
            choose_checkbox = driver.find_element_by_xpath("//*[@id='J_DataTable']/table/tbody[1]/tr[1]/td/input[1]")
            choose_checkbox.click()
            unshelve_btn = driver.find_element_by_xpath(
                "//*[@id='J_DataTable']/div[2]/table/thead/tr[2]/td/div/button[2]")
            unshelve_btn.click()
            return True
        except:
            return False

    def shelve(self):

        if self.__is_logined is False:
            if self.__login() is False:
                return False
            else:
                self.__is_logined = True

        # 1.进入仓库宝贝页面
        driver.get(self.__repository_path)
        # 2.点击上架
        try:
            choose_checkbox = driver.find_element_by_xpath("//*[@id='J_DataTable']/table/tbody[1]/tr[1]/td/input")
            choose_checkbox.click()
            shelve_btn = driver.find_element_by_xpath("//*[@id='J_DataTable']/div[3]/table/tbody/tr/td/div/button[2]")
            shelve_btn.click()
        except exceptions.NoSuchElementException:
            pass

    def delivered(self, orderId):

        if self.__is_logined is False:
            if self.__login() is False:
                return False
            else:
                self.__is_logined = True
        try:
            # 1.进入确认发货页面
            driver.get(self.__deliver_path + orderId)
            no_need_logistics_a = driver.find_element_by_xpath("//*[@id='dummyTab']/a")
            no_need_logistics_a.click()
            driver.find_element_by_id("logis:noLogis").click()
            time.sleep(1)
            return True
        except:
            return False

    def exists_refunding(self):

        if self.__is_logined is False:
            if self.__login() is False:
                return False
            else:
                self.__is_logined = True
        try:
            # 1.进入退款页面
            driver.get(self.__refunding_path)
            driver.find_element_by_class_name("item-mod__trade-order___2LnGB trade-order-main")
            return True
        except exceptions.NoSuchElementException:
            return False


if __name__ == '__main__':
    climber = TaobaoClimber(u"淘宝账号", "登录密码")
    while True:
        # 循环爬取订单
        orders = climber.climb()
        for order in orders:
            print_msg("订单号：%s\t订单日期：%s \t买家：%s\t备注：%s" % order)
        # 每30秒抓一次
        time.sleep(30)
