# 发货机器人
**帮你实现：淘宝虚拟商品的`自动值守`、`资源下载`、`Email发货`**

## 1、运作流程
![](http://p27z4ahy7.bkt.clouddn.com/2018/08/19/2e3aba61a8652cac683c3e12b4694c31.png)

**Trip：**
* 使用小附件方式发送邮件，大于50M文件可能发送失败（QQ邮箱通病）。文件已压缩为zip，再进行发送，这样文件更小，而且可规避某些邮箱服务器不允许直接发送exe文件
* 发送新的下载地址到买家邮箱，**需要自有服务器**。然后配置静态文件服务器（如nginx），直接将服务器本地文件夹映射出来（详见：[Nginx作为静态文件服务器](http://localhost01.cn/2017/04/03/Linux%E4%B8%8BNginx%E4%BD%9C%E4%B8%BA%E9%9D%99%E6%80%81%E6%96%87%E4%BB%B6%E6%9C%8D%E5%8A%A1%E5%99%A8/ "Nginx作为静态文件服务器")）
* 登录QQ邮箱发送方式，使用了AutoIt配合完成附件上传，理论上附件大小不限。

## 2、其他功能
* 售卖订单数（即对应CSDN下载次数）可控，到达设定数，立即**下架商品**，并且可开启邮件提醒
* 自动检查退款订单，进行**自动退款**
* 发货完成后，自动修改卖家订单为**发货状态**
* **统计功能**：统计成功、失败订单，且失败订单可开启邮件提醒

## 3、运行环境
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

## 4、可能问题
* 在**火狐57.0版本**能完美运行，其他浏览器及版本自测
* 开启钱盾后，可能导致首次进入卖家中心失败，请手动关闭**钱盾匹配弹窗**，或立即打开手机，进行**钱盾匹配**

## 5、使用方法
1. 先将`geckodriver-32.exe`或`geckodriver-64.exe`改名为`geckodriver.exe`，并放于python根目录
2. pip安装上面三方库以及火狐浏览器
3. 打开cn/localhost01/__init__.py，根据自己情况修改配置参数
4. 运行“启动.bat”
