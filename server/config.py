# -*- coding: utf-8 -*-  = "/sta"

import re, os, platform

def get_netloc():
	if platform.uname()[1] == "Ubuntu":
		return "127.0.0.1:5000"
	elif platform.uname()[1] == "pub-PowerEdge-R820":
		return "222.198.155.138:5000"

basedir = os.path.abspath(os.path.dirname(__file__))

APP_NAME = "家庭健康助手"
NETWORK_ADDRESS = "http://" + get_netloc()
NETLOC_NAME = get_netloc()

# print NETLOC_NAME

SECRET_KEY = os.urandom(24)
STATIC_SECRET_CODE = "hard to guess"
EMAIL_SALT = "hard to think"
DEBUG = True
MONGO_DBNAME = "healthmanager"
MONGO_HOST = "localhost"
MONGO_PORT = 27017

# email
MAIL_HOST = "smtp.163.com"
MAIL_SENDER = "gjw870402916@163.com"
MAIL_PASSWORD = "08151997bc"

MAX_MEDICINE_NUM_PER_PAGE = 8

DEFAULT_IMAGE_PATH = "/static/img/user/default.jpg"
# DEFAULT_FAMILY_IMAGE_PATH = "/static/img/family/default.jpg"
HEAD_IMAGE_PATH = "/static/img/user/"
MEDICINE_THUMBNAIL_PATH = "/static/img/medicine/"

CHECK_EMAIL_REGEX = re.compile(r'[a-zA-Z0-9][-_.a-zA-Z0-9]*@[-_.a-zA-Z0-9]+((\.[-_a-zA-Z0-9]){2,5}){1,2}')

EMAIL_HTML = u"""<p>{username}, 您好</p>
				 <p>欢迎注册家庭健康助手,我们竭诚为您提供最优质的家庭健康管理,如果有好的意见和建议,欢迎联系我们</p>
				 <p>请点击<a href='http://{netloc}/validate/{verifycode}'>此处</a>
				 验证您的邮箱</p>
			  """
