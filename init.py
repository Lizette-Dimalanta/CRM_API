# SQLAlchemy: Object Relational Mapper (ORM)
from flask_sqlalchemy import SQLAlchemy
# Marshmallow: Converts other datatypes to standard python datatype
from flask_marshmallow import Marshmallow
# Bcrypt: Password hashing function
from flask_bcrypt import Bcrypt
# JWTManager: Handles tokens
from flask_jwt_extended import JWTManager


db  = SQLAlchemy()
ma  = Marshmallow()
bc  = Bcrypt()
jwt = JWTManager()