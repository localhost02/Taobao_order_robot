# 背景
之前看到朋友下载csdn资源，但因为没有下载积分，因此他会在淘宝上购买一个叫做“csdn资源代下”的业务。对我来说，也许这是一个商机（因为刚好提交了一个csdn漏洞，得到了一年的vip下载会员，不能白白浪费了嘛）。因此借助python和selenium实现了一个自动下载发货的机器人，想着只需要把它运行在服务器上，就能躺着赚钱了！

# 简介
一个能在淘宝上进行虚拟商品自动值守、CSDN资源下载、Email发货的全自动机器人

## 运作流程
1. Selenium开启浏览器【火狐浏览器驱动】
2. 进行登录【淘宝登录页面】
3. *滑块验证（chorme滑块验证会失败）【若需要验证】*
4. 登录定位页面【卖家待发货订单页面】
5. 获取订单列表，并借用cookies请求订单留言【每间隔时间获取一次】
6. 传值给CSDN下载类，进行下载【CSDN下载页面】
7. *进行登录【若需要登录】*
8. 借用cookies，进行分段下载【下载到本地指定位置】
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
* 在火狐57.0版本能完美运行，其他浏览器及版本自测
* 开启钱盾后，可能导致首次进入卖家中心失败，请手动关闭钱盾匹配弹窗或立即打开手机进行钱盾匹配

## 使用方法
1. 先将geckodriver-32.exe/geckodriver-64.exe改名为geckodriver.exe，并放到python根目录
2. pip安装上面三方库以及火狐浏览器
3. 打开cn/localhost01/__init__.py，根据自己情况修改配置参数
4. 运行“启动.bat”
