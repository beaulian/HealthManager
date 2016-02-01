# -*- coding: utf-8 -*- 

from config import *
from controller.models import User
from controller.errors import *

from flask import request, g
from functools import wraps


def login_required(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		uid = request.args.get("uid", None)
		token = request.args.get("token", None)
		if (not uid) or (not token):
			if (not uid) and (not token):
				return healthmanager_error("2003")
			else:
				return healthmanager_error("2009")
		else:
			if User.verify_uid(uid):
				if User.verify_token(token, uid):
					pass
				else:
					return healthmanager_error("2006")
			else:
				return healthmanager_error("2005")
		return func(*args, **kwargs)
	return wrapper
		