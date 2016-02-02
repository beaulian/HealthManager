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
    from .controller.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .controller.user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .controller.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .controller.medicine import medicine as medicine_blueprint
    app.register_blueprint(medicine_blueprint)

    from .controller.record import record as record_blueprint
    app.register_blueprint(record_blueprint)

    return app