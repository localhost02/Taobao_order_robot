# -*- coding: utf-8 -*-
# 淘宝账号
taobao_username = u""
taobao_password = ""

# CSDN账户
csdn_username = ""
csdn_password = ""

# 七牛授权
qiniu_ak = ""
qiniu_sk = ""
qiniu_bucket = "csdn-data"
qiniu_domain = "http://example.com"

# 邮箱账号
mail_username = ""
# 邮箱登录密码（可选，mail_send_type=2有效）
mail_password = ""
# 邮箱独立密码（可选，mail_send_type=2有效）
mail_password2 = ""
# 邮箱授权码（可选，mail_send_type=1有效）
mail_authorization_code = ""

# 接收邮件号
master_mail = ""

# 本地保存下载文件地址
local_dir = "c://Robot_Download/"

# 自带文件下载服务器地址前缀，类似http://xx.com/（可选，mail_send_type=0有效）
server_file_url = "http://example.com:8080/"

# 下载次数总数
download_total = 20

# 爬虫每次检查待发货订单间隔/秒
check_order_period = 30

# 爬虫每次检查存在退款订单间隔/秒
check_refunding_period = 60

# 页面加载等待最长时间（推荐10秒以上，视网速而定）
delay_wait = 15

# 邮件发送方式 0=仅仅发送资源新的下载链接（需自带服务器） 1=发送邮件附件（50M以上问题发送有问题） 2=浏览器方式发送（推荐）
mail_send_type = 0

# 是否开启邮件提醒
is_mail_notice = False
