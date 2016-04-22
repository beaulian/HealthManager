# # -*- coding: utf-8 -*- 

# from . import disease
# from config import *
# from ..utils import *
# from ..errors import *
# from ..models import User, Model, Medicine
# from ..decorators import (login_required, valid_id_required,
# 										valid_uid_required)

# from bson import ObjectId
# from datetime import datetime
# from flask import request, jsonify, g


# @disease.route("/disease", methods=["POST"])
# @login_required
# def post_disease():
# 	uid              = request.args.get("uid")
# 	describe         = request.form.get("describe", None)
# 	start_time       = request.form.get("start_time", None)
# 	end_time         = request.form.get("end_time", "未填写")
# 	ill_reason       = request.form.get("ill_reason", None)
# 	recovery_reason  = 