# -*- coding: utf-8 -*- 

from . import record
from config import *
from ..utils import *
from ..errors import *
from ..models import User, Model, Medicine
from ..decorators import (login_required, valid_id_required,
										valid_uid_required)

from bson import ObjectId
from datetime import datetime
from flask import request, jsonify, g


