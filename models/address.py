from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length, OneOf, And, Regexp

VALID_STREET_TYPES = ('Street', 'Lane', 'Road', 'Boulevard')

# SQLAlchemy: Address Details
class Address(db.Model):
    __tablename__= 'addresses'

    id            = db.Column(db.Integer, primary_key=True)
    apt_number    = db.Column(db.Integer)
    street_number = db.Column(db.Integer, nullable=False)
    street_name   = db.Column(db.String(100), nullable=False)
    suburb        = db.Column(db.String(100), nullable=False)
    street_type   = db.Column(db.String(20), nullable=False)
    state         = db.Column(db.String(100), nullable=False)
    zip           = db.Column(db.Integer, nullable=False)
    country       = db.Column(db.String(100), nullable=False)
    # Foreign Key
    profile_id    = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    # Foreign Key Relationship
    profile       = db.relationship('Profile', back_populates='address')
 
# Marshmallow: Address Schema
class AddressSchema(ma.Schema):
    # Nested Attributes
    profile       = fields.List(fields.Nested('ProfileSchema'), exclude=['address'])

    # Address Validation
    apt_number = fields.Integer(required=True)
    street_number = fields.Integer(required=True)
    street_name = fields.String(required=True, validate=And(
        Length(min=1, error='Must be at least 1 character.'), 
        Regexp('^[a-zA-Z]+$', error='Only letters and spaces are allowed.')))
    suburb = fields.String(required=True, validate=And(
        Length(min=1, error='Must be at least 1 character.'), 
        Regexp('^[a-zA-Z]+$', error='Only letters and spaces are allowed.')))
    street_type = fields.String(required=True, validate=OneOf(VALID_STREET_TYPES))
    state = fields.String(required=True, validate=And(
        Length(min=1, error='Must be at least 1 character.'), 
        Regexp('^[a-zA-Z]+$', error='Only letters and spaces are allowed.')))
    zip = fields.Integer(required=True)
    country = fields.String(required=True, validate=And(
        Length(min=1, error='Must be at least 1 character.'), 
        Regexp('^[a-zA-Z]+$', error='Only letters and spaces are allowed.')))

    class Meta:
        fields    = ('id', 'apt_number', 'street_number', 'street_name', 'suburb', 'state', 'zip', 'country')
        ordered   = True

