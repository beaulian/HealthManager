# -*- coding: utf-8 -*- 

from config import *
from models import User, Model
from errors import *

from flask import request, g
from functools import wraps


def creater_required(func):
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
				if User.verify_creater(uid):
					if User.verify_token(token, uid):
						pass
					else:
						return healthmanager_error("2006")
				else:
					return healthmanager_error("2007")
			else:
				return healthmanager_error("2005")
		return func(*args, **kwargs)
	return wrapper


def admin_required(func):
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
				if User.verify_admin(uid):
					if User.verify_token(token, uid):
						pass
					else:
						return healthmanager_error("2006")
				else:
					return healthmanager_error("2007")
			else:
				return healthmanager_error("2005")
		return func(*args, **kwargs)
	return wrapper


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


def can(func):
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
					if User.verify_admin(uid) or uid == kwargs.get("uid"):
						g.can = True
					else:
						g.can = False
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
	            return healthmanager_error("2014")
	        return func(*args, **kwargs)
	    return wrapper
	return handle
		

def valid_uid_required(**kwargs0):
	def handle(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			user = Model.db.User.find_one({"$or": [{"username": kwargs.get("uid")},{"email": kwargs.get("uid")}]})
			if not user:
				return healthmanager_error("2005")
			else:
				if kwargs0.get("user_required"):
					g.user = user
			return func(*args, **kwargs)
		return wrapper
	return handle


def valid_family_uid_required(**kwargs0):
	def handle(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			user = Model.db.FamilyUser.find_one({"family_id": kwargs.get("family_id"), "uid": kwargs.get("uid")})
			if not user:
				user_again = Model.db.FamilyUserNot.find_one({"family_id": kwargs.get("family_id"), "username": kwargs.get("uid")})
				if not user_again:
					return healthmanager_error("2005")
				else:
					g.is_register = False
					if kwargs0.get("user_required"):
						g.user = user_again
			else:
				g.is_register = True
				if kwargs0.get("user_required"):
					g.user = user
			return func(*args, **kwargs)
		return wrapper
	return handle