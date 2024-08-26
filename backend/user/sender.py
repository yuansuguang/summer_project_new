import random
from django.core.mail import send_mail
from user.models import *

from django.conf import settings

import datetime

from utils.hashcode import *

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

def make_code(user):
    code = hashcode(user.username, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ConfirmCode.objects.create(code=code, user=user)
    return code

def send_code_email(email, code):

    email_title = "问卷星球邮箱验证"
    email_body = "感谢您注册问卷星球！请使用下面的链接激活您的帐号。\n"
    email_body += "http://localhost:8000/user/confirm/?code={0}".format(code)

    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

    return send_status

# def check_code(code):
    # if ConfirmCode.filter(code=code).exists() == False:
        # return False
    # else:
        # ConfirmCode.filter(code=code).delete()
        # return True
        
# 发送重置密码邮件        
def send_reset_password_email(email, code):

    email_title = "密码重置"
    email_body = "您好！\n\n"
    email_body += f"请点击以下链接重置您的密码：\n{settings.FRONTEND_URL}/reset-password/{code}/\n\n"
    email_body += "如果这不是您的操作，请忽略此邮件。"

    send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])

    return send_status