# -*- coding: utf-8 -*- 

from config import *
from errors import *

from flask import request, jsonify, make_response
from controller.decorators import login_required
from controller.models import User, Model
from controller.errors import *
from datetime import datetime
from mail import send_email
from . import auth


@auth.route("/user/register", methods=["POST"])
def register():
	username = request.form.get("username", None)
	email = request.form.get("email", None)
	password = request.form.get("password", None)
	if (not username) or (not email) or (not password):
		return healthmanager_error("2008")

	if Model.db.Users.find_one({"username": username}):
		return healthmanager_error("2002")
	if Model.db.Users.find_one({"email": email}):
		return healthmanager_error("2001")

	user = User(
			username = username, 
			email = email,
			password_hash = User.encrypt(password),
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
	if send_email("验证邮箱", [email], u"""<p>{username}, 您好</p>
					<p>欢迎注册家庭健康助手,我们竭诚为您提供最优质的家庭健康管理,如果有好的意见和建议,欢迎联系我们</p>
					<p>请点击<a href='http://{netloc}/validate/{verifycode}'>此处</a>
					验证您的邮箱</p>""".format(username=username, netloc=NETLOC_NAME,
																verifycode=user["verify_code"])):
		Model.db.Users.insert(user.__dict__)
		user["head_image"] = "http://" + NETLOC_NAME + user["head_image"]
		return jsonify({"status": "success", "user": user.to_json()})
	else:
		return healthmanager_error("2099")


@auth.route("/user/login", methods=["POST", "PUT"])
def login():
	uid = request.form.get("uid", None)
	password = request.form.get("password", None)
	status = User.verify_user(uid, password)
	if status == 2:
		token = User.generate_token(uid)
		if request.method == "POST":
			return jsonify({"status": "success", "token": token})
		elif request.method == "PUT":
			return jsonify({"status": "success", "refresh_token": token})
	elif status == 1:
		return healthmanager_error("2000")
	else:
		return healthmanager_error("2004")


@auth.route("/validate/<string:verifycode>")
def validate(verifycode):
	"""not restful api"""
	user = Model.db.Users.find_one({"verify_code": verifycode})
	if user:
		user["confirmed"] = True
		Model.db.Users.save(user)
		print user["confirmed"]
		return make_response("<p>您已成功验证!</p>")










