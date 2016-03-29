# -*- coding: utf-8 -*- 

from . import family
from config import *
from ..utils import *
from ..errors import *
from ..models import User, Model, Family, FamilyUser, FamilyUserNot
from ..decorators import (login_required, valid_id_required, can,
							 creater_required, admin_required,
							 valid_uid_required, valid_family_uid_required)

from bson import ObjectId
from datetime import datetime
from flask import request, jsonify, g


@family.route("/family", methods=["POST"])
@login_required
def create_family():
	uid = request.args.get("uid")
	if Model.db.Family.find_one({"create_uid": uid}):
		return healthmanager_error("2015")
	
	relationship = request.form.get("relationship", None)
	if not relationship:
		return healthmanager_error("2009")

	family = Family(create_uid = uid)
	family_id = family.insert()

	family_user = FamilyUser(
		uid = uid,
		family_id = family_id,
		permission = 4,
		relationship = relationship
	)
	family_user.insert()

	return jsonify({"status": "success", "family": family.to_json()})


@family.route("/family/<string:uid>", methods=["GET"])
@login_required
@valid_uid_required(user_required=False)
def get_family(uid):
	family_user = Model.db.FamilyUser.find_one({"uid": uid})
	if family_user:
		family = Model.db.Family.find_one({"_id": ObjectId(family_user["family_id"])})
		family["_id"] = str(family["_id"])
		return jsonify({"status": "success", "family": family, "exist": 1})
	return jsonify({"status": "success", "exist": 0})


@family.route("/family/<string:family_id>/manager", methods=["POST"])
@creater_required
@valid_id_required("Family", "family_id")
def post_manager(family_id):
	uid = request.form.get("uid")
	user = Model.db.FamilyUser.find_one({"family_id": family_id, "uid": uid})
	if not user:
		return healthmanager_error("2005")
	user["permission"] = 2
	Model.db.FamilyUser.save(user)

	return jsonify({"status": "success"})


@family.route("/family/<string:family_id>/manager/<string:uid>", methods=["DELETE"])
@creater_required
@valid_id_required("Family", "family_id")
@valid_family_uid_required(user_required=False)
def delete_manager(family_id, uid):
	Model.db.FamilyUser.update({"uid": uid, "family_id": family_id}, {"$set": {"permission": 1}})

	return jsonify({"status": "success"})


@family.route("/family/<string:family_id>/user", methods=["POST"])
@admin_required
@valid_id_required("Family", "family_id")
def post_family_user(family_id):
	uid = request.form.get("uid", None)
	relationship = request.form.get("relationship", None)
	if (not uid) or (not relationship):
		return healthmanager_error("2009")
	if not Model.db.User.find_one({"$or": [{"username": uid},{"email": uid}]}):
		return healthmanager_error("2005")
	if Model.db.FamilyUser.find_one({"uid": uid, "family_id": family_id}):
		return healthmanager_error("2016")

	family_user = FamilyUser(
		uid = uid,
		family_id = family_id,
		permission = 1,
		relationship = relationship
	)
	family_user.insert()

	return jsonify({"status": "success"})


@family.route("/family/<string:family_id>/newuser", methods=["POST"])
@admin_required
@valid_id_required("Family", "family_id")
def post_new_family_user(family_id):
	username = request.form.get("username", None)
	relationship = request.form.get("relationship", None)
	if (not username) or (not relationship):
		return healthmanager_error("2009")
	if Model.db.User.find_one({"username": username}):
		return healthmanager_error("2002")

	family_user_not = FamilyUserNot(
		username = username,
		head_image = DEFAULT_IMAGE_PATH,
		age = 0,
		sex = "男",
		family_id = family_id,
		permission = 1,
		relationship = relationship,
		register_time = datetime.now().__format__("%Y-%m-%d %H:%M:%S")
	)
	family_user_not.insert()

	return jsonify({"status": "success"})


@family.route("/family/<string:family_id>/user", methods=["GET"])
@login_required
@valid_id_required("Family", "family_id")
def get_family_users(family_id):
	users = []
	for family_user in Model.db.FamilyUser.find({"family_id": family_id}):
		user = Model.db.User.find_one({"$or": [{"username": family_user["uid"]},{"email": family_user["uid"]}]})
		user_info = {
			"_id": str(user["_id"]),
			"username": user["username"],
			"head_image": NETWORK_ADDRESS + user["head_image"]
		}
		users.append(user_info)

	for family_user_not in Model.db.FamilyUserNot.find({"family_id": family_id}):
		user_info_two = {
			"_id": str(family_user_not["_id"]),
			"username": family_user_not["username"],
			"head_image": NETWORK_ADDRESS + family_user_not["head_image"]
		}
		users.append(user_info_two)

	return jsonify({"status": "success", "users": users})


@family.route("/family/<string:family_id>/user/<string:uid>", methods=["GET"])
@can
@valid_id_required("Family", "family_id")
@valid_family_uid_required(user_required=True)
def get_family_user(family_id, uid):
	g.user["_id"] = str(g.user["_id"])
	if g.can:
		g.user["medicines"] = get_specific_info(Model.db.Medicine.find({"uid": uid}), "name", "feature", "place")
		g.user["diseases"] = get_specific_info(Model.db.Disease.find({"uid": uid}), "describe", "long_term")
		g.user["healing_records"] = get_specific_info(Model.db.HealingRecord.find({"uid": uid}), "type", "time", "hospital")
		g.user["common_buy_records"] = get_specific_info(Model.db.CommonBuyRecord.find({"buyer_uid": uid}), "medicine_name", "time", "place")
		return jsonify({"status": "success", "user": g.user})
	else:
		return jsonify({"status": "success", "user": g.user})


@family.route("/family/<string:family_id>/user/<string:uid>", methods=["DELETE"])
@admin_required
@valid_id_required("Family", "family_id")
@valid_family_uid_required(user_required=True)
def delete_family_user(family_id, uid):
	if g.is_register:
		Model.db.FamilyUser.remove(g.user)
	else:
		Model.db.FamilyUserNot.remove(g.user)

	family = Model.db.Family.find_one({"create_uid": uid})
	if family:
		Model.db.Family.remove(family)
		
	return jsonify({"status": "success"})


@family.route("/family/<string:family_id>/user/self", methods=["DELETE"])
@login_required
@valid_id_required("Family", "family_id")
def delete_family_myself(family_id):
	uid = request.args.get("uid")
	Model.db.FamilyUser.remove({"uid": uid})

	family = Model.db.Family.find_one({"create_uid": uid})
	if family:
		Model.db.Family.remove(family)

	return jsonify({"status": "success"})