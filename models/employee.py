from init import db, ma
from marshmallow import fields

class Employee(db.Model):
    __tablename__ = 'employees'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String, unique=True, nullable=False)
    password      = db.Column(db.String, nullable=False)
    is_admin      = db.Column(db.Boolean, default=False)
    # Foreign Key
    profile_id    = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
        # Foreign Key Relationship
    profile    = db.relationship('Profile', back_populates='employee')

class EmployeeSchema(ma.Schema):
    # Nested Attributes
    profile       = fields.List(fields.Nested('ProfileSchema'))
    class Meta:
        fields    = ('id', 'username', 'password', 'is_admin', 'profile')
