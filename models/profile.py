from init import db, ma
from marshmallow import fields
from flask_jwt_extended import jwt_required

# SQLAlchemy: Profile Details
class Profile(db.Model):
    __tablename__= 'profiles'

    id          = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(50), nullable=False)
    last_name   = db.Column(db.String(100), nullable=False)
    phone       = db.Column(db.Integer, unique=True, nullable=False)
    email       = db.Column(db.String(100), unique=True, nullable=False)
    is_customer = db.Column(db.Boolean, default=True, nullable=False)
    join_date   = db.Column(db.Date)
    occupation  = db.Column(db.String(100))
    company     = db.Column(db.String(100))
    # Foreign Key Relationship
    employee    = db.relationship('Employee', back_populates='profile', cascade ='all, delete')
    address     = db.relationship('Address', back_populates='profile', cascade ='all, delete')
    complaints  = db.relationship('Complaint', back_populates='profile', cascade ='all, delete')

# Marshmallow: Profile Schema
class ProfileSchema(ma.Schema):
    # Nested Attributes
    employee    = fields.List(fields.Nested('EmployeeSchema'), exclude=['password'])
    address     = fields.List(fields.Nested('AddressSchema'))
    complaints  = fields.List(fields.Nested('ComplaintSchema'), exclude=['complaints'])

    class Meta:
        fields  = ('id', 'first_name', 'last_name', 'phone', 'email', 'is_customer', 'join_date', 'occupation', 'address', 'employee')
        ordered = True