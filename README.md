Todolist[20181226]
1 删除CsdnDownloader类相关代码；
2 增加订单状态，以过滤已发货订单；
3 增加功能：如果留言格式不正确，发邮件提醒客户/卖家；


# 背景
淘宝上搜到很多资源代下的相关业务，也许这是一个赚零花钱的办法，因此想尝试借助python和selenium实现一个自动下载发货的机器人。

# 简介
一个能在淘宝上进行虚拟商品自动值守、Email或者网盘发货的全自动机器人

## 运作流程
1. Selenium开启浏览器【火狐浏览器驱动】
2. 进行登录【以支付宝账号登录淘宝】
3. 首次登录可能需要手机验证码
4. 登录定位页面【卖家待发货订单页面】
5. 获取订单列表，并借用cookies请求订单留言【每间隔时间获取一次】
6/7/8 待续
9. 传值给邮件发送类，选择邮件发送模式：
    * 直接发送资源到买家邮箱【大于50M文件可能发送失败】；
    Trip：文件压缩为zip，再进行发送（文件更小，且某些邮箱服务器不允许直接发送exe文件）
    * 发送新的下载地址到买家邮箱【需自有服务器】；`推荐`
    Trip：需配置静态资源服务器，如nginx，直接将下载文件夹映射出来；
    * 登录QQ邮箱，进行邮件发送。使用了AutoIt配合完成附件上传。

## 附加功能
* 订单数（下载次数）可控，到达设定数，下架商品并邮件提醒
* 自动检查退款订单，自动退款
* 发货完成后，自动去修改卖家订单为发货
* 统计功能，统计成功、失败订单。且失败订单会立马邮件提醒

## 技术点
* selenium
* bs4
* requests
* smtplib、email
* zipfile
* chardet
* regex expression
* autoit

## 运行环境
`python2.7`

```bash
pip install requests
```
```bash
pip install beautifulsoup4
```
```bash
pip install html5lib
```
```bash
pip install selenium
```
```bash
pip install chardet
```

## 其他说明
* 已通过测试的浏览器版本：Firefox 62.0/Chrome 69.0
* 开启钱盾后，可能导致首次进入卖家中心失败，请手动关闭钱盾匹配弹窗或立即打开手机进行钱盾匹配

## 使用方法
1. 下载Firefox驱动geckodriver.exe或者Chrome驱动chromedriver.exe，并复制到python根目录
2. pip安装上面三方库以及浏览器
3. 打开cn/localhost01/__init__.py，根据自己情况修改配置参数
4. 运行“启动.bat”
