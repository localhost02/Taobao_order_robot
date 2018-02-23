# -*- coding: utf-8 -*-
from cn.localhost01.mail.mail_sender import Mail
from cn.localhost01.__init__ import master_mail
import chardet
import sys

# 初始化输出编码
print_code_mode = 'utf-8'

if len(sys.argv) == 2:
    print_code_mode = sys.argv[1]


def send_mail(sender, model, insert=None, insert2=None):
    if insert is None:
        sender.send(Mail(master_mail, model, 0))
    elif insert2 is None:
        message = model.replace("$1", str(insert))
        sender.send(Mail(master_mail, message, 0))
    else:
        message = model.replace("$1", str(insert)).replace("$2", str(insert2))
        sender.send(Mail(master_mail, message, 0))


def print_msg(message):
    encoding = chardet.detect(str(message))['encoding']
    if encoding == print_code_mode:
        print message
    else:
        print message.decode(encoding).encode(print_code_mode)
