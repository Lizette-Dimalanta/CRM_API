from init import db, ma
from marshmallow import fields
from marshmallow import fields
from marshmallow.validate import Length

class Employee(db.Model):
    __tablename__ = 'employees'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String, unique=True, nullable=False)
    password      = db.Column(db.String, nullable=False)
    is_admin      = db.Column(db.Boolean, default=False)
    # Foreign Key
    profile_id    = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    # Foreign Key Relationship
    profile    = db.relationship('Profile', back_populates='employee', cascade ='all, delete')
    complaints  = db.relationship('Complaint', back_populates='employee', cascade ='all, delete')
    task       = db.relationship('Task', back_populates='employee', overlaps='complaints', cascade ='all, delete')


class EmployeeSchema(ma.Schema):
    # Nested Attributes
    profile   = fields.List(fields.Nested('ProfileSchema'))
    complaints = fields.List(fields.Nested('ComplaintSchema'), exclude=['employee'])
    tasks      = fields.List(fields.Nested('TaskSchema'), exclude=['employee'])

    # Employee Validation
    # Must have username, must be unique, minimum length of 1 character.
    username = fields.String(required=True, unique=True, validate=Length(min=1, error='Must be at least 1 character.'))

    # Defining fields
    class Meta:
        fields    = ('id', 'username', 'password', 'is_admin', 'profile', 'complaints', 'tasks')