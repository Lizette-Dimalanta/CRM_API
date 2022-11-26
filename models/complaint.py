from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length

# SQLAlchemy: Complaint Details
class Complaint(db.Model):
    __tablename__= 'complaints'

    id          = db.Column(db.Integer, primary_key=True)
    subject     = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    entry_time  = db.Column(db.Date)
    # Foreign Keys
    profile_id  = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    # Foreign Key Relationships
    profile     = db.relationship('Profile', back_populates='complaints', cascade ='all, delete')
    employee    = db.relationship('Employee', back_populates='complaints', cascade ='all, delete')

# Marshmallow: Complaint Schema
class ComplaintSchema(ma.Schema):
    # Nested Attributes
    profile    = fields.List(fields.Nested('ProfileSchema'))
    employee   = fields.List(fields.Nested('EmployeeSchema'), exclude=['password','employee'])

    # Complaint Validation
    # Must have subject, minimum length of 1 character.
    subject = fields.String(required=True, validate=Length(min=1, error='Must be at least 1 character.'))
    # Minimum length of 1 character.
    description = fields.String(validate=Length(min=1, error='Must be at least 1 character.'))

    class Meta:
        fields  = ('id', 'subject', 'description', 'entry_time', 'profile', 'employee')
        ordered = True