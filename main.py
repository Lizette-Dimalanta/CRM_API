from flask import Flask
from db import db
from flask_marshmallow import Marshmallow

from controllers.customers_controller import customers_bp
from controllers.customers_controller import profiles_bp

import os

def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(customers_bp)
    app.register_blueprint(profiles_bp)

    # @app.route('/')
    # def index():
    #     return 'Hello'

    return app

# Blueprint: Modularise flask application (like class)