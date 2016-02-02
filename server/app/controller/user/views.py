# -*- coding: utf-8 -*- 

from . import user
from config import *
from ..errors import *
from ..models import User, Model

from bson import ObjectId
from datetime import datetime
from flask import request, jsonify
from ..decorators import login_required, valid_id_required


@user.route("/user/<string:user_id>", methods=["GET"])
@login_required
@valid_id_required("Users", "user_id")
def get_user_info(user_id):
	user = Model.db.Users.find_one({"_id": ObjectId(user_id)})
	user["_id"] = str(user["_id"])
	return jsonify({"status": "success", "user": user})