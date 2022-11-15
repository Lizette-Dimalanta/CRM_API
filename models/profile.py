from init import db, ma
from marshmallow import fields

# SQLAlchemy: Profile Details
class Profile(db.Model):
    __tablename__= 'profiles'

    id          = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(50), nullable=False)
    last_name   = db.Column(db.String(100), nullable=False)
    birthday    = db.Column(db.Date, nullable=False)
    phone       = db.Column(db.Integer, unique=True, nullable=False)
    email       = db.Column(db.String(100), unique=True, nullable=False)
    is_customer = db.Column(db.Boolean, default=True, nullable=False)
    join_date   = db.Column(db.Date, nullable=False)
    occupation   = db.Column(db.String(100))
    company     = db.Column(db.String(100))
    
    # Foreign Key
    address_id  = db.Column(db.Integer, db.ForeignKey('addresses.id'), nullable=False)
    # Foreign Key Relationship
    address     = db.relationship('Address', back_populates='profiles', cascade='all, delete')

# Marshmallow: Profile Schema
class ProfileSchema(ma.Schema):
    # Nested Attributes
    address     = fields.List(fields.Nested('AddressSchema', exclude = ['profile']))

    class Meta:
        fields  = ('id', 'first_name', 'last_name', 'birthday', 'phone', 'email', 'is_customer', 'join_date', 'occupation', 'address')
        ordered = True