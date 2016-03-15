# -*- coding: utf-8 -*- 

from . import user
from config import *
from ..utils import *
from ..errors import *
from ..models import User, Model
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