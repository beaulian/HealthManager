#!/usr/bin/python
# -*- coding: utf-8 -*- 

from os import urandom

SECRET_KEY = urandom(24)
STATIC_SECRET_CODE = "hard to guess"
DEBUG = True
MONGO_DBNAME = "healthmanager"
MONGO_HOST = "localhost"
MONGO_PORT = 27017