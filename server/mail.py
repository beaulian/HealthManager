# -*-coding:utf8 -*-

import smtplib
from config import *
from email.mime.text import MIMEText

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def send_email(fuction, mail_receiver_list, content):
    msg = MIMEText(content,_subtype="html",_charset="utf-8")
    msg["Subject"] = fuction
    msg["From"] = APP_NAME + "<" + MAIL_SENDER + ">"
    msg["To"] = ";".join(mail_receiver_list)
    
    server = smtplib.SMTP()
    server.connect(MAIL_HOST)
    server.starttls()
    server.login(MAIL_SENDER, MAIL_PASSWORD)
    server.sendmail(MAIL_SENDER,mail_receiver_list,msg.as_string())
    server.close()
    
