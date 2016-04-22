# -*- coding: utf-8 -*-

import json
import random
import string
import hashlib

from errors import *
from config import *
from bson import ObjectId
from flask import jsonify
from pymongo import MongoClient
from passlib.hash import md5_crypt
from pymongo.errors import InvalidId
from itsdangerous import (TimestampSigner,
                            SignatureExpired)


class Model(object):
    """init model"""
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DBNAME]

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    """
        test:
            >>> user = User(username="gavin")
            >>> print user["username"]
    """
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def to_json(self):
        import copy
        element = copy.copy(self.__dict__)
        if element.has_key("_id"):
            element["_id"] = str(element["_id"])
        return element

    def insert(self):
        _id = self.db[self.__class__.__name__].insert(self.__dict__)
        return str(_id)

    @classmethod
    def verify_id(cls, dbname, _id):
        try:
            if not cls.db[dbname].find_one({"_id": ObjectId(_id)}):
                raise InvalidId
        except InvalidId:
            return False
        return True

    def __del__(self):
        self.client.close()

   	def __str__(self):
   		return "<Model %r>" % self.db


#---------------------- data object ---------------------------------


class User(Model):
    """User model"""
    # __slots__ = (
    #         "_id", "username", "email", "password_hash", "verify_code",
    #         "head_image", "confirmed", "allow_reminded", "phone_number",
    #         "introduction", "age", "register_time", "last_seen"
    # )

    @classmethod
    def generate_token(cls, uid):
        # user = cls.db.User.find_one({"$or": [{"username": uid},{"email": uid}]})
        pwd = cls.db.Pwd.find_one({"$or": [{"username": uid},{"email": uid}]})
        s = TimestampSigner(pwd["password_hash"]+STATIC_SECRET_CODE)
        return s.sign(hashlib.md5(uid).hexdigest())

    @classmethod
    def verify_token(cls, token_to_check, uid):
        # user = cls.db.User.find_one({"$or": [{"username": uid},{"email": uid}]})
        pwd = cls.db.Pwd.find_one({"$or": [{"username": uid},{"email": uid}]})
        s = TimestampSigner(pwd["password_hash"]+STATIC_SECRET_CODE)
        try:
            s.unsign(token_to_check, max_age=7200)
        except Exception:
            return False
        return True

    @classmethod
    def refresh_token(cls, old_token, uid):
        pwd = cls.db.Pwd.find_one({"$or": [{"username": uid},{"email": uid}]})
        s = TimestampSigner(pwd["password_hash"]+STATIC_SECRET_CODE)
        try:
            s.unsign(old_token, max_age=7200)
        except Exception:
            return False

        return s.sign(uid)

    @classmethod
    def verify_uid(cls, uid):
    	if cls.db.User.find_one({"$or": [{"username": uid},{"email": uid}]}):
    		return True
    	return False

    @classmethod
    def verify_creater(cls, uid):
        family_user = cls.db.FamilyUser.find_one({"uid": uid})
        if family_user and family_user["permission"] == 4:
            return True
        return False

    @classmethod
    def verify_admin(cls, uid):
        family_user = cls.db.FamilyUser.find_one({"uid": uid})
        if family_user and family_user["permission"] >= 2:
            return True
        return False


    @classmethod
    def verify_user(cls, uid, password):
    	user = cls.db.User.find_one({"$or": [{"username": uid},{"email": uid}]})
        pwd = cls.db.Pwd.find_one({"$or": [{"username": uid},{"email": uid}]})
        if user:
            if md5_crypt.verify(password, pwd["password_hash"]):
                if user["confirmed"]:
                    return 2
                else:
                    return 1
        return 0

    @staticmethod
    def encrypt(seed):
        return md5_crypt.encrypt(seed, salt=random.choice(string.letters))

    @staticmethod
    def get_verify_code(email):
        return hashlib.md5(email+EMAIL_SALT).hexdigest()


class Pwd(Model):
    "Pwd model"
    pass

class Collection(Model):
    pass

class Comment(Model):
    pass

class Family(Model):
    pass

class FamilyUser(Model):
    pass

class FamilyUserNot(Model):
    pass

class Medicine(Model):
    pass

class Jpush(Model):
    pass



if __name__ == '__main__':
    user = User(username=1)
    print user["username"]
    print user.to_json()
