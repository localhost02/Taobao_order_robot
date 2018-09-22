# -*- coding: utf-8 -*-
# 账号参数
# taobao_username = u"淘宝登录账号"
# taobao_password = "淘宝登录密码"
account_info_file = "..\\..\\account_info.txt"
csdn_username = "csdn_vip账号"
csdn_password = "csdn登录密码"
mail_username = "邮箱登录账号"
# 邮箱登录密码（浏览器发送才需配置）
mail_password = "邮箱登录密码"
# 邮箱独立密码（浏览器发送才需配置，如果没有独立密码请配置为""）
mail_password2 = "邮箱独立密码"
# 邮箱授权码
mail_authorization_code = "邮箱授权码"

# 邮件提醒-接收账号
master_mail = "邮件提醒-接收账号"

# 本地保存下载文件地址
local_dir = "c://Robot_Download/"

# 文件下载服务器地址（可选）
server_file_url = ""

# 下载次数总数
download_total = 20

# 爬虫每次检查待发货订单间隔/秒
check_order_period = 30

# 爬虫每次检查存在退款订单间隔/秒900
check_refunding_period = 60

# 邮件发送方式 0=仅仅发送资源新的下载链接（需自带服务器） 1=发送邮件附件（50M以上问题发送有问题） 2=浏览器方式发送（推荐）
mail_send_type = 2

# 未留言订单是否邮件提醒
mail_notice_for_no_note = True

# 页面加载等待最长时间（推荐10秒以上，视网速而定）
delay_wait = 15

# 报警邮件，如果内容为空则不发送邮件报警
# 邮件下架失败
message_unshelve_false = "请注意：资源下载数已达到$1次，但下架失败！"

# 超出下载次数总数
message_over_download_total = "请注意：资源下载数已达到20次，但仍有$1个订单需发货！"

# 修改订单发货状态为已发货失败
message_delivered_false = "请注意：订单ID【$1】已发货，但修改订单发货状态失败！"

# 资源下载失败
message_download_false = "请注意：订单ID【$1】相关资源下载失败！"

# 资源发送失败
message_send_false = "请注意：订单ID【$1】相关资源发送失败！"

# 存在退款订单
message_exists_refunding = "请注意：存在退款订单，请主人处理！"

# 订单未留言
message_notice_for_no_note = "请注意：产生了无法操作的订单，请主人处理！"

message_send_mail_error = "请注意：订单ID【$1】相关资源发送失败，原因：$2"
