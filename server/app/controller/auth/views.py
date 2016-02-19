# -*- coding: utf-8 -*- 

from flask import request, jsonify, make_response
from ..decorators import login_required
from ..models import User, Model, Pwd
from ..errors import *
from config import *
from datetime import datetime
from mail import send_email
from . import auth


@auth.route("/user/register", methods=["POST"])
def register():
	username = request.form.get("username", None)
	email = request.form.get("email", None)
	password = request.form.get("password", None)
	if (not username) or (not email) or (not password):
		return healthmanager_error("2009")

	if Model.db.User.find_one({"username": username}):
		return healthmanager_error("2002")
	if Model.db.User.find_one({"email": email}):
		return healthmanager_error("2001")

	user = User(
			username = username, 
			email = email,
			verify_code = User.get_verify_code(email),
			head_image = DEFAULT_IMAGE_PATH,
			confirmed = False,
			allow_reminded = False,
			phone_number = "",
			introduction = "",
			age = 0,
			register_time = datetime.now().__format__("%Y-%m-%d %H:%M:%S"),
			last_seen = datetime.now().__format__("%Y-%m-%d %H:%M:%S")
	)
	pwd = Pwd(
			username = username, 
			email = email,
			password_hash = User.encrypt(password)
	)
	if send_email("验证邮箱", [email], u"""<p>{username}, 您好</p>
					<p>欢迎注册家庭健康助手,我们竭诚为您提供最优质的家庭健康管理,如果有好的意见和建议,欢迎联系我们</p>
					<p>请点击<a href='http://{netloc}/validate/{verifycode}'>此处</a>
					验证您的邮箱</p>""".format(username=username, netloc=NETLOC_NAME,
																verifycode=user["verify_code"])):
		user.insert()
		pwd.insert()
		user["head_image"] = "http://" + NETLOC_NAME + user["head_image"]
		user["token"] = User.generate_token(username)
		return jsonify({"status": "success", "user": user.to_json()})
	else:
		return healthmanager_error("2099")


@auth.route("/user/login", methods=["POST"])
def login():
	uid = request.form.get("uid", None)
	password = request.form.get("password", None)
	status = User.verify_user(uid, password)
	if status == 2:
		token = User.generate_token(uid)
		return jsonify({"status": "success", "token": token})
	elif status == 1:
		return healthmanager_error("2000")
	else:
		return healthmanager_error("2004")


@auth.route("/user/login", methods=["PUT"])
def put_token():
	uid = request.args.get("uid", False)
	old_token = request.args.get("token", False)
	if not User.verify_uid(uid):
		return healthmanager_error("2005")
	token = User.refresh_token(old_token, uid)
	if token:
		return jsonify({"status": "success", "token": token})
	else:
		return healthmanager_error("2006", token=old_token)


@auth.route("/validate/<string:verifycode>")
def validate(verifycode):
	"""not restful api"""
	user = Model.db.User.find_one({"verify_code": verifycode})
	if user:
		user["confirmed"] = True
		del user["verify_code"]
		Model.db.User.save(user)
		print user["confirmed"]
		return make_response("<p>您已成功验证!</p>")










