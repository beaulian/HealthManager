# -*- coding: utf-8 -*- 

from config import *
from models import User, Model
from errors import *

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


def valid_id_required(db_name, id_name):
	def handle(func):
	    @wraps(func)
	    def wrapper(*args, **kwargs):
	        if not Model.verify_id(db_name, kwargs.get(id_name)):
	            return healthmanager_error("2004")
	        return func(*args, **kwargs)
	    return wrapper
	return handle
		