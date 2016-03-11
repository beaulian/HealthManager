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
	for temp_news in Model.db.IndexNews.find():
		news = {
			"id": str(temp_news["_id"]),
			"title": temp_news["title"],
			"classf": temp_news["classf"],
			"thumbnail": temp_news["thumbnail"]
		}
		mutinews.append(news)

	return jsonify({"status": "success", "mutinews": mutinews}) 


@news.route("/news/<string:classf>/<string:news_id>", methods=["GET"])
@valid_id_required("IndexNews", "news_id")
def get_index_news_detail(classf, news_id):
	news = Model.db.IndexNews.find_one({"_id": ObjectId(news_id), "classf": classf})
	news = change_object_attr(news)

	return jsonify({"status": "success", "news": news})

