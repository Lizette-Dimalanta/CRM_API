from flask import Flask
from init import db, ma, bc, jwt
from marshmallow.exceptions import ValidationError

# Import Controllers
# from controllers.customers_controller import customers_bp
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.profiles_controller import profiles_bp
from controllers.addresses_controller import addresses_bp
from controllers.complaints_controller import complaints_bp
from controllers.tasks_controller import tasks_bp

import os

# Defines App
def create_app():
    app = Flask(__name__)

    # Error Handlers
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': 'err.messages'}, 400

    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': 'You are not authorized to perform this action.'}, 401

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field (err) is required.'}, 400

    # Disable JSON sort
    app.config['JSON_SORT_KEYS'] = False

    # Retrieve Database URL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    # JWTManager Secret Key
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # Creating Objects
    db.init_app(app)
    ma.init_app(app)
    bc.init_app(app)
    jwt.init_app(app)

    # Activate Blueprints
    # app.register_blueprint(customers_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(addresses_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(tasks_bp)

    @app.route('/')
    def index():
        return 'Hello'

    return app