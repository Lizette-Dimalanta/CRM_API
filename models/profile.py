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
    # Foreign Key
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    # Foreign Key Relationship
    address = db.relationship('Address', back_populates='profiles')

# Marshmallow: Profile Schema
class ProfileSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'birthday', 'phone', 'email', 'address')
        ordered = True
