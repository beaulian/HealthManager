# -*- coding: utf-8 -*-

from . import jpush
from config import *
from ..utils import *
from ..errors import *
from ..models import User, Model, Jpush
from ..decorators import login_required

from bson import ObjectId
from datetime import datetime
# from hcelery.jpush import push
from flask import request, jsonify


@jpush.route("/jpush/registerationid", methods=["POST"])
@login_required
def post_registeration():
    uid = request.args.get("uid", None)
    registeration_id = request.form.get("registeration_id", None)
    if not registeration_id:
        return healthmanager_error("2009")
    if not Model.db.Jpush.find_one({"uid": uid}):
        _jpush = Jpush(uid=uid, registeration_id=registeration_id)
        _jpush.insert()
    return jsonify({"status": "success"})


@jpush.route("/jpush", methods=["POST"])
@login_required
def post_jpush():
    uid     = request.form.get("uid", None)
    title   = request.form.get("title", None)
    hour    = request.form.get("hour", None)
    minute  = request.form.get("minute", None)
    weeks   = 
