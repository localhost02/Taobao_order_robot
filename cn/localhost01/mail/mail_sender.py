# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import Utils
import zipfile
import os.path
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class MailSender:
    def __init__(self, username, mail_authorization_code):
        self.__username = username
        self.__mail_authorization_code = mail_authorization_code

    __username = ""
    __mail_authorization_code = ""

    def send(self, mail):

        if mail.text is "":
            return False

        server = smtplib.SMTP_SSL(mail.server, mail.port)
        server.login(self.__username, self.__mail_authorization_code)  # 仅smtp服务器需要验证时

        # 构造MIMEMultipart对象做为邮件主体
        body_mail = MIMEMultipart()

        # 构造显示内容并添加到邮件主体
        text_mail = None
        if mail.mode == 0:
            text_mail = MIMEText(mail.text, _charset="utf-8")
        elif mail.mode == 1:
            text_mail = MIMEText(mail.file_path.decode("gbk") + "\r\n\r\n\r\n" + mail.text, _charset="utf-8")
        else:  # 构造附件并添加到邮件主体
            text_mail = MIMEText(mail.text, _charset="utf-8")

            file_mail = MIMEText(open(mail.file_path, 'rb').read(), 'base64', 'utf-8')
            file_mail["Content-Type"] = 'application/x-zip-compressed'
            basename = os.path.basename(mail.file_path)
            file_mail["Content-Disposition"] = 'attachment; filename=' + basename
            body_mail.attach(file_mail)

        body_mail.attach(text_mail)

        # 设置邮件主体属性
        body_mail['From'] = mail.Special_Form
        body_mail['To'] = mail.Special_To
        body_mail['Reply-to'] = mail.Special_Reply
        body_mail['Subject'] = mail.subject
        body_mail['Date'] = Utils.formatdate()

        # 得到格式化后的完整文本
        full_text = body_mail.as_string()

        # 用smtp发送邮件
        try:
            server.sendmail(self.__username, mail.to_user, full_text)
            return True
        except smtplib.SMTPDataError:
            return False
        finally:
            server.quit()


class Mail:
    # mode：0=邮件提醒，1=仅发送资源地址，2=发送资源附件
    def __init__(self, to_user, file_path, mode=1):
        self.to_user = to_user
        self.file_path = file_path.encode("gbk")
        self.mode = mode
        if mode == 0:
            self.subject = "邮件提醒"
            self.Special_To = "【尊贵的主人】"
            self.Special_Reply = "不用回复！"
            self.text = "\r\n" + file_path
        elif mode == 1:
            self.subject += "-下载地址"
        else:
            # 如果不是压缩文件，则打包成zip
            if re.match(r"^[\s\S]+\.((?!(RAR|ZIP|TAR|ARJ|CAB|LZH|ACE|GZ|UUE|BZ2|JAR|ISO)).)+$", self.file_path.upper()):
                zip_path = re.sub(r"\.((?!\.).)+$", ".zip", self.file_path, 1)
                zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
                zip_file.write(self.file_path)
                self.file_path = zip_path

    # 发送模式
    mode = 1

    # 邮箱个性显示
    Special_Form = "自动发货机器人"
    Special_To = "【尊贵的淘宝买家】"
    Special_Reply = "请旺旺联系！"

    # 邮箱内容及附件
    subject = "CSDN资源文件"
    text = "\r\nTrip：如果有任何问题，请旺旺上联系客服，客服将每天定时处理【问题订单】，谢谢支持！"
    file_path = ""  # 附件地址（本地路径 | 网上路径）

    # 邮箱配置
    server = "smtp.qq.com"
    port = 465
    to_user = ""


if __name__ == "__main__":
    # 发送邮件
    mail_sender = MailSender("邮箱账号", "授权码")
    mail_sender.send(Mail("接收邮箱", "c://Robot_Download/大话Oracle_RAC：集群、高可用性、备份与恢复.pdf", 2))
