# -*- coding: utf-8 -*- 

from . import family
from config import *
from ..utils import *
from ..errors import *
from ..models import User, Model, Family, FamilyUser, FamilyUserNot, Medicine
from ..decorators import (login_required, valid_id_required, can,
							 creater_required, admin_required,
							 valid_uid_required, valid_family_uid_required,
							 admin_required_if_not_self)

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


#---------------------------------- 家庭药品管理---------------------------------


@family.route("/family/<string:family_id>/medicine/<string:uid>", methods=["POST"])
@admin_required_if_not_self
@valid_id_required("Family", "family_id")
@valid_family_uid_required(user_required=False)
def post_medicine(family_id, uid):
	name              = request.form.get("name", None)
	thumbnail         = request.files.get("thumbnail", None)
	feature           = request.form.get("feature",None)
	company           = request.form.get("company", None)
	usage             = request.form.get("usage", None)
	taboo             = request.form.get("taboo", None)
	reaction          = request.form.get("reaction", None)
	place             = request.form.get("place", None)
	buy_time          = request.form.get("buy_time", None)
	overdue_time      = request.form.get("overdue_time", None)
	long_term_use     = request.form.get("long_term_use", 0)
	purchase_quantity = request.form.get("purchase_quantity", None)
	residue_quantity  = request.form.get("residue_quantity", None)
	
	for key in ["name", "feature", "company", "usage", "thumbnail",
				"taboo", "place", "buy_time", "overdue_time",
				"purchase_quantity", "residue_quantity"]:
		if not eval(key):
			return healthmanager_error("2009")

	if Model.db.Medicine.find_one({"name": name, "company": company}):
		return healthmanager_error("2017")

	if allow_image(thumbnail.filename):
		thumbnail = save_img(thumbnail, 80, MEDICINE_THUMBNAIL_PATH)
	else:
		return healthmanager_error("2012")

	medicine = Medicine(
		uid = uid,
		name = name,
		thumbnail = thumbnail,
		feature = feature,
		company = company,
		usage = usage,
		taboo = taboo,
		reaction = reaction,
		place = place,
		buy_time = buy_time,
		overdue_time = overdue_time,
		long_term_use = long_term_use,
		purchase_quantity = purchase_quantity,
		residue_quantity = residue_quantity
	)
	medicine.insert()

	return jsonify({"status": "success"})


@family.route("/family/<string:family_id>/medicine/<string:uid>/<string:medicine_id>", methods=["PUT"])
@admin_required_if_not_self
@valid_id_required("Family", "family_id")
@valid_family_uid_required(user_required=False)
def put_medicine(family_id, uid, medicine_id):
	thumbnail         = request.files.get("thumbnail", None)
	reaction          = request.form.get("reaction", None)
	place             = request.form.get("place", None)
	long_term_use     = request.form.get("long_term_use", None)
	residue_quantity  = request.form.get("residue_quantity", None)

	medicine = Model.db.Medicine.find_one({"uid": uid, 
								"_id": ObjectId(medicine_id)})
	if not medicine:
		return healthmanager_error("2099", info="you no such medicine")

	if thumbnail:
		if allow_image(thumbnail.filename):
			delete_img(medicine["thumbnail"])
			thumbnail = save_img(thumbnail, 80, MEDICINE_THUMBNAIL_PATH)
			medicine["thumbnail"] = thumbnail
		else:
			return healthmanager_error("2012")

	for key in ["reaction", "place", "long_term_use", "residue_quantity"]:
		if eval(key):
			medicine[key] = eval(key)
	Model.db.Medicine.save(medicine)

	return jsonify({"status": "success"})


@family.route("/family/<string:family_id>/medicine", methods=["GET"])
@login_required
@valid_id_required("Family", "family_id")
def get_medicines(family_id):
	uid = request.args.get("uid")
	if not Model.db.FamilyUser.find_one({"family_id": family_id, "uid": uid}):
		return healthmanager_error("2007")

	page_num = request.args.get("page_num", 1)
	keyword  = request.args.get("keyword", None)
	search_condition = {"$or": [
								{key: {"$regex": keyword, "$options": "i"}} 
								for key in ["name", "company", "place", "usage"]
							   ]
					   } if keyword else {}
	medicine_list = Model.db.Medicine.find(search_condition) \
					 .skip((int(page_num)-1) * MAX_MEDICINE_NUM_PER_PAGE) \
					 .limit(MAX_MEDICINE_NUM_PER_PAGE)

	max_page = ( medicine_list.count() + MAX_MEDICINE_NUM_PER_PAGE - 1 ) / MAX_MEDICINE_NUM_PER_PAGE 
	max_page = 1 if max_page == 0 else max_page
	if int(page_num) > max_page:
		return healthmanager_error("2013")

	medicines = []
	for medicine in medicine_list:
		temp_medicine = {
			"_id": str(medicine["_id"]),
			"name": medicine["name"],
			"thumbnail": NETWORK_ADDRESS + medicine["thumbnail"],
			"company": medicine["company"]
		}
		medicines.append(temp_medicine)
	
	return jsonify({"status": "success", "medicines": medicines, 
						"curr_page": page_num, "max_page": max_page})


@family.route("/family/<string:family_id>/medicine/user/<string:uid>", methods=["GET"])
@login_required
@valid_id_required("Family", "family_id")
@valid_family_uid_required(user_required=False)
def get_user_medicines(family_id, uid):
	page_num = request.args.get("page_num", 1)
	medicine_list = Model.db.Medicine.find({"uid": uid}) \
					 .skip((int(page_num)-1) * MAX_MEDICINE_NUM_PER_PAGE) \
					 .limit(MAX_MEDICINE_NUM_PER_PAGE)

	max_page = ( medicine_list.count() + MAX_MEDICINE_NUM_PER_PAGE - 1 ) / MAX_MEDICINE_NUM_PER_PAGE 
	max_page = 1 if max_page == 0 else max_page
	if int(page_num) > max_page:
		return healthmanager_error("2013")

	medicines = []
	for medicine in medicine_list:
		temp_medicine = {
			"_id": str(medicine["_id"]),
			"name": medicine["name"],
			"thumbnail": NETWORK_ADDRESS + medicine["thumbnail"],
			"company": medicine["company"]
		}
		medicines.append(temp_medicine)
	
	return jsonify({"status": "success", "medicines": medicines, 
						"curr_page": page_num, "max_page": max_page})


@family.route("/family/<string:family_id>/medicine/<string:uid>/<string:medicine_id>", methods=["DELETE"])
@admin_required_if_not_self
@valid_id_required("Family", "family_id")
@valid_family_uid_required(user_required=False)
@valid_id_required("Medicine", "medicine_id")
def delete_medicine(family_id, uid, medicine_id):
	medicine = Model.db.Medicine.find_one({"uid": uid, "_id": ObjectId(medicine_id)})
	delete_img(medicine["thumbnail"])
	Model.db.Medicine.remove(medicine)

	return jsonify({"status": "success"})