# -*- coding: utf-8 -*-

from . import medicine
from config import *
from ..utils import *
from ..errors import *
from ..models import User, Model, Medicine
from ..decorators import (login_required, valid_id_required,
										valid_uid_required)

from bson import ObjectId
from datetime import datetime
from flask import request, jsonify, g


@medicine.route("/medicine", methods=["POST"])
# @login_required
def post_medicine():
	uid               = request.args.get("uid")
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

	for key in ["name", "feature", "company", "usage",
				"taboo", "place", "buy_time", "overdue_time",
				"purchase_quantity", "residue_quantity"]:
		if not eval(key):
			return healthmanager_error("2009")

	if Model.db.Medicine.find_one({"name": name, "company": company}):
		return healthmanager_error("2017")

	if thumbnail:
		print thumbnail
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


@medicine.route("/medicine/<string:medicine_id>", methods=["PUT"])
@login_required
@valid_id_required("Medicine", "medicine_id")
def put_medicine(medicine_id):
	uid               = request.args.get("uid")
	thumbnail         = request.files.get("thumbnail", None)
	reaction          = request.form.get("reaction", None)
	place             = request.form.get("place", None)
	long_term_use     = request.form.get("long_term_use", None)
	residue_quantity  = request.form.get("residue_quantity", None)

	medicine = Model.db.Medicine.find_one({"uid": uid,
								"_id": ObjectId(medicine_id)})
	if not medicine:
		return healthmanager_error("2099", info="you don't have such medicine")

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


@medicine.route("/medicine", methods=["GET"])
@login_required
def get_medicines():
	uid = request.args.get("uid")
	page_num = request.args.get("page_num", 1)
	medicines = []
	for medicine in Model.db.Medicine.find() \
					 .skip((int(page_num)-1) * MAX_MEDICINE_NUM_PER_PAGE) \
					 .limit(MAX_MEDICINE_NUM_PER_PAGE):
		temp_medicine = {
			"_id": str(medicine["_id"]),
			"name": medicine["name"],
			"thumbnail": NETWORK_ADDRESS + medicine["thumbnail"],
			"company": medicine["company"],
			"uid": medicine["uid"]
		}
		medicines.append(temp_medicine)
	return jsonify({"status": "success", "medicines": medicines,
						"curr_page": page_num})


@medicine.route("/medicine/lilac", methods=["GET"])
def get_medicines_from_lilac():
	_type    = request.args.get("type", None)
	keyword  = request.args.get("keyword", None)
	if not _type:
		return healthmanager_error("2009")

	medicines = []
	if _type == "barcode":
		temp_medicine = Model.db.Barcode.find_one({"barcode": keyword})
		if temp_medcine:
			for medicine in Model.db.Medicine.find({"name": temp_medicine["name"]}):
				medicines.append(change_object_attr(medicine))

	elif _type == "medicine":
		condition = {"name": {"$regex": keyword, "$options": "i"}} if keyword else {}
		for medicine in Model.db.TempMedicine.find(condition):
			medicines.append(change_object_attr(medicine))

	return jsonify({"status": "success", "medicines": medicines})


@medicine.route("/medicine/lilac/<string:medicine_id>", methods=["GET"])
@valid_id_required("TempMedicine", "medicine_id")
def get_medicine_from_lilac_by_id(medicine_id):
	medicine = Model.db.TempMedicine.find_one({"_id": ObjectId(medicine_id)})
	return jsonify({"status": "success", "medicine": change_object_attr(medicine)})


@medicine.route("/medicine/<string:medicine_id>", methods=["GET"])
@login_required
@valid_id_required("Medicine", "medicine_id")
def get_medicine(medicine_id):
	uid = request.args.get("uid")
	medicine = Model.db.Medicine.find_one({"uid": uid,
										"_id": ObjectId(medicine_id)})
	del medicine["_id"]
	medicine["thumbnail"] = NETWORK_ADDRESS + medicine["thumbnail"]
	x
	return jsonify({"status": "success", "medicine": medicine})


@medicine.route("/medicine/<string:medicine_id>", methods=["DELETE"])
@login_required
@valid_id_required("Medicine", "medicine_id")
def delete_medicine(medicine_id):
	uid = request.args.get("uid")
	medicine = Model.db.Medicine.find_one({"uid": uid, "_id": ObjectId(medicine_id)})
	delete_img(medicine["thumbnail"])
	Model.db.Medicine.remove(medicine)

	return jsonify({"status": "success"})
