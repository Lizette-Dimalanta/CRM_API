from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, And, Regexp

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
    complaints   = db.relationship('Complaint', back_populates='profile', cascade ='all, delete')
    task       = db.relationship('Task', back_populates='profile', cascade ='all, delete')

# Marshmallow: Profile Schema
class ProfileSchema(ma.Schema):
    # Nested Attributes
    employee    = fields.List(fields.Nested('EmployeeSchema'), exclude=['password', 'profile'])
    address     = fields.List(fields.Nested('AddressSchema'))
    complaints   = fields.List(fields.Nested('ComplaintSchema'), exclude=['complaints', 'profile'])
    task        = fields.List(fields.Nested('TaskSchema'), exclude=['task', 'profile'])

    # Profile Validation
    first_name = fields.String(required=True, validate=And(
        Length(min=1, error='Must be at least 1 character.'), 
        Regexp('^[a-zA-Z]+$', error='Only letters and spaces are allowed.')))
    last_name = fields.String(required=True, validate=And(
        Length(min=1, error='Must be at least 1 character.'), 
        Regexp('^[a-zA-Z]+$', error='Only letters and spaces are allowed.')))
    phone = fields.Integer(required=True, validate=And(
        Length(min=8, error='Must be at least 8 character.'), 
        Regexp('^[0-9]+$', error='Only numbers are allowed.')))
    email = fields.String(required=True, validate=And(
        Length(min=5, error='Must be at least 5 character.'), 
        Regexp('^[a-zA-Z0-9 @.]+$', error='Only letters, numbers, and symbols @ and . are allowed.')))
    is_customer = fields.Boolean(required=True)

    class Meta:
        fields  = ('id', 'first_name', 'last_name', 'phone', 'email', 'is_customer', 'join_date', 'occupation', 'employee', 'address', 'complaints', 'task')
        ordered = True