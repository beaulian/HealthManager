# -*- coding: utf-8 -*- 

import re, os

basedir = os.path.abspath(os.path.dirname(__file__))

APP_NAME = "家庭健康助手"
NETLOC_NAME = "127.0.0.1:5000"

SECRET_KEY = os.urandom(24)
STATIC_SECRET_CODE = "hard to guess"
EMAIL_SALT = "hard to think"
DEBUG = True
MONGO_DBNAME = "healthmanager"
MONGO_HOST = "localhost"
MONGO_PORT = 27017

# email
MAIL_HOST = "smtp.qq.com"
MAIL_SENDER = "870402916@qq.com"
MAIL_PASSWORD = "08151997bccb"

DEFAULT_IMAGE_PATH = "/static/img/user/default.jpg"
CHECK_EMAIL_REGEX = re.compile(r'[a-zA-Z0-9][-_.a-zA-Z0-9]*@[-_.a-zA-Z0-9]+((\.[-_a-zA-Z0-9]){2,5}){1,2}')