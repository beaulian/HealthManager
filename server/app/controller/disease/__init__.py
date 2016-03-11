from flask import Blueprint

disease = Blueprint('disease',__name__)

from . import views