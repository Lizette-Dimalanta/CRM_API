from flask import Flask
from init import db, ma, bc, jwt
from flask_marshmallow import Marshmallow

# Import Controllers
# from controllers.customers_controller import customers_bp
from controllers.profiles_controller import profiles_bp

import os

# Defines App
def create_app():
    app = Flask(__name__)

    # Disable JSON sort
    app.config['JSON_SORT_KEYS'] = False

    # Retrieve Database URL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    app.config['JSON_SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # Creating Objects
    db.init_app(app)
    ma.init_app(app)
    bc.init_app(app)
    jwt.init_app(app)

    # Activate Blueprints
    # app.register_blueprint(customers_bp)
    app.register_blueprint(profiles_bp)

    @app.route('/')
    def index():
        return 'Hello'

    return app

# Blueprint: Modularise flask application (like class)