# -*- coding: utf-8 -*- 

from . import user
from config import *
from ..utils import *
from ..errors import *
from ..models import User, Model, Collection
from ..decorators import login_required, valid_id_required

from bson import ObjectId
from datetime import datetime
from flask import request, jsonify


@user.route("/user/<string:uid>", methods=["GET"])
@login_required
def get_user_info(uid):
	user = Model.db.User.find_one({"$or": [{"username": uid},{"email": uid}]})
	user["head_image"] = "http://" + NETLOC_NAME + user["head_image"]
	return jsonify({"status": "success", "user": change_object_attr(user)})


@user.route("/user/self", methods=["GET"])
@login_required
def get_self_info():
	uid = request.args.get("uid")
	user = Model.db.User.find_one({"$or": [{"username": uid},{"email": uid}]})
	user["head_image"] = "http://" + NETLOC_NAME + user["head_image"]
	return jsonify({"status": "success", "user": change_object_attr(user)})


@user.route("/user/self", methods=["PUT"])
@login_required
def put_self_info():
	uid = request.args.get("uid")

	email = request.form.get("email", None)
	phone_number = request.form.get("phone_number", None)
	head_image = request.files.get("head_image", None)
	sex = request.form.get("sex", None)
	age = request.form.get("age", None)
	introduction = request.form.get("introduction", None)

	user = Model.db.User.find_one({"$or": [{"username": uid},{"email": uid}]})

	if head_image:
		if allow_image(head_image.filename):
			head_image = save_img(head_image, 80, HEAD_IMAGE_PATH)
		else:
			return healthmanager_error("2012")

	for key in user:
		if eval(key):
			user[key] = eval(key)
	Model.db.User.save(user)
	return jsonify({"status": "success"})


# ----------------------Collection---------------------


@user.route("/user/self/collection", methods=["GET"])
@login_required
def get_collection():
	uid = request.args.get("uid")
	
	collections = []
	for collection in Model.db.Collection.find({"uid": uid}):
		collection["news"] = Model.db.HealthNews.find_one({"_id": ObjectId(collection["news_id"])})
		del collection["news_id"]
		collections.append(change_object_attr(collection))
	return jsonify({"status": "success", "collections": collections})


@user.route("/user/self/collection", methods=["POST"])
@login_required
def post_collection():
	uid = request.args.get("uid")
	news_id = request.form.get("news_id", None)

	if not Model.verify_id("HealthNews", news_id):
		return healthmanager_error("2014")

	collection = Collection(
		uid = uid,
		news_id = news_id,
		time = datetime.now().__format__("%Y-%m-%d %H:%M:%S")
	)
	collection.insert()
	return jsonify({"status": "success"})


@user.route("/user/self/collection/<string:news_id>", methods=["DELETE"])
@login_required
@valid_id_required("HealthNews", "news_id")
def delete_collection(news_id):
	uid = request.args.get("uid")
	Model.db.Collection.remove({"uid": uid, "news_id": news_id})
	return jsonify({"status": "success"})
