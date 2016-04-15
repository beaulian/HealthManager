# -*- coding: utf-8 -*-

from flask import jsonify, request
from bson import ObjectId
from config import *

from . import news
from ..models import Model
from ..utils import change_object_attr
from ..decorators import valid_id_required


@news.route("/news/index", methods=["GET"])
def get_index_news():
	mutinews = []
	for temp_news in Model.db.HealthNews.find({"news_type": "index"}):
		news = {
			"id": str(temp_news["_id"]),
			"title": temp_news["title"],
			"classf": temp_news["classf"],
			"thumbnail": temp_news["thumbnail"]
		}
		mutinews.append(news)

	return jsonify({"status": "success", "mutinews": mutinews})


@news.route("/news/<string:classf>/<string:news_id>", methods=["GET"])
@valid_id_required("HealthNews", "news_id")
def get_news_detail(classf, news_id):
	news = Model.db.HealthNews.find_one({"_id": ObjectId(news_id), "classf": classf})

	return jsonify({"status": "success", "news": change_object_attr(news)})


@news.route("/news/main/<string:classf>", methods=["GET"])
def get_main_news(classf):
	main_mutinews = []
	for temp in Model.db.HealthNews.find({"classf": classf, "news_type": "main"}):
		temp["_id"] = str(temp["_id"])
		main_mutinews.append(temp)

	return jsonify({"status": "success", "main_mutinews": main_mutinews})
