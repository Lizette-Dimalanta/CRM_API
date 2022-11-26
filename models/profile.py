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
    # Must have first name, minimum length of 1 character, only letters and spaces are allowed.
    first_name = fields.String(required=True, validate=And(
        Length(min=1, error='Must be at least 1 character.'), 
        Regexp('^[a-zA-Z]+$', error='Only letters and spaces are allowed.')))
    # Must have last name, minimum length of 1 character, only letters and spaces are allowed.
    last_name = fields.String(required=True, validate=And(
        Length(min=1, error='Must be at least 1 character.'), 
        Regexp('^[a-zA-Z]+$', error='Only letters and spaces are allowed.')))
    # Must have phone number.
    phone = fields.Integer(required=True, unique=True)
    # Must have email address.
    email = fields.String(required=True, unique=True)
    # Must state profile type: Is the profile a customer?
    is_customer = fields.Boolean(required=True)

    # Defining fields
    class Meta:
        fields  = ('id', 'first_name', 'last_name', 'phone', 'email', 'is_customer', 'join_date', 'occupation', 'employee', 'address', 'complaints', 'task')
        ordered = True