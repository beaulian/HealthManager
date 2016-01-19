#!/usr/bin/python
# -*- coding: UTF-8 -*- 

import config
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    # 蓝本
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from medicine import medicine as medicine_blueprint
    app.register_blueprint(medicine_blueprint)

    from record import record as record_blueprint
    app.register_blueprint(record_blueprint)

    return app