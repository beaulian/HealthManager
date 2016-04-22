from flask import Blueprint

jpush = Blueprint('jpush',__name__)

from . import views
