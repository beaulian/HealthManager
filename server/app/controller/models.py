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

    def to_json(self):
        import copy
        element = copy.copy(self.__dict__)
        if element.has_key("_id"):
            element["_id"] = str(element["_id"])
        return element

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

    def insert(self):
        self.db.Users.insert(self.__dict__)

    @classmethod
    def generate_token(self, uid):
        user = self.db.Users.find_one({"$or": [{"username": uid},{"email": uid}]})
        s = TimestampSigner(user["password_hash"]+STATIC_SECRET_CODE)
        return s.sign(uid)
    
    @classmethod
    def verify_token(self, token_to_check, uid):
        user = self.db.Users.find_one({"$or": [{"username": uid},{"email": uid}]})
        s = TimestampSigner(user["password_hash"]+STATIC_SECRET_CODE)
        try:
            s.unsign(token_to_check, max_age=7200)
        except Exception:
            return False
        return True

    @classmethod
    def verify_uid(self, uid):
    	if self.db.Users.find_one({"$or": [{"username": uid},{"email": uid}]}):
    		return True
    	return False

    @classmethod
    def verify_user(self, uid, password):
    	user = self.db.Users.find_one({"$or": [{"username": uid},{"email": uid}]})
        if user:
            if md5_crypt.verify(password, user["password_hash"]):
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


if __name__ == '__main__':
    user = User(username=1)
    print user["username"]
    print user.to_json()