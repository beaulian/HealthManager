# -*- coding: utf-8 -*- 

from . import comment
from config import *
from ..utils import *
from ..errors import *
from ..models import User, Model, Comment
from ..decorators import login_required, valid_id_required

from bson import ObjectId
from datetime import datetime
from flask import request, jsonify


@comment.route("/comment/<string:news_id>", methods=["GET"])
@login_required
@valid_id_required("HealthNews", "news_id")
def get_comment(news_id):
	comments = [] 
	for comment in Model.db.Comment.find({"news_id": news_id}):
		comment["_id"] = str(comment["_id"])
		user = Model.db.User.find_one({"$or": [{"username": comment["uid"]},{"email": comment["uid"]}]})
		comment["user"] = {
				"username": user["username"],
				"head_image": user["head_image"]
		}
		comments.append(comment)

	return jsonify({"status": "success", "comments": comments})


@comment.route("/comment/<string:news_id>", methods=["POST"])
@login_required
@valid_id_required("HealthNews", "news_id")
def post_comment(news_id):
	uid = request.args.get("uid")
	text = request.form.get("text", None)
	time = datetime.now().__format__("%Y-%m-%d %H:%M:%S")

	comment = Comment(
		uid = uid,
		text = text,
		time = time,
		news_id = news_id,
		parent_id = False
	)
	comment.insert()
	return jsonify({"status": "success"})


@comment.route("/comment/<string:news_id>/<string:comment_id>", methods=["POST"])
@login_required
@valid_id_required("HealthNews", "news_id")
@valid_id_required("Comment", "comment_id")
def post_comment_comment(news_id, comment_id):
	uid = request.args.get("uid")
	text = request.form.get("text", None)
	time = datetime.now().__format__("%Y-%m-%d %H:%M:%S")

	comment = Comment(
		uid = uid,
		text = text,
		time = time,
		news_id = news_id,
		parent_id = comment_id
	)
	comment.insert()
	return jsonify({"status": "success"})


@comment.route("/comment/<string:news_id>/<string:comment_id>", methods=["DELETE"])
@login_required
@valid_id_required("HealthNews", "news_id")
@valid_id_required("Comment", "comment_id")
def delete_comment(news_id, comment_id):
	Model.db.Comment.remove({"_id": ObjectId(comment_id), "news_id": news_id})
	return jsonify({"status": "success"})
