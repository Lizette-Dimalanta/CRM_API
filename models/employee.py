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
    profile    = db.relationship('Profile', back_populates='employee', cascade ='all, delete')
    complaints  = db.relationship('Complaint', back_populates='employee', cascade ='all, delete')
    task       = db.relationship('Task', back_populates='employee', overlaps='complaints', cascade ='all, delete')


class EmployeeSchema(ma.Schema):
    # Nested Attributes
    profile   = fields.List(fields.Nested('ProfileSchema'))
    complaints = fields.List(fields.Nested('ComplaintSchema'), exclude=['employee'])
    tasks      = fields.List(fields.Nested('TaskSchema'), exclude=['employee'])

    class Meta:
        fields    = ('id', 'username', 'password', 'is_admin', 'profile', 'complaints', 'tasks')