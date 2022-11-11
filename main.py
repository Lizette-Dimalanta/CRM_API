from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    db = SQLAlchemy(app)

    @app.route('/')
    def index():
        return 'Hello'

    return app