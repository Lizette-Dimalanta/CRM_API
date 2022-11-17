from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError
from datetime import datetime

VALID_STATUSES = ('To Do', 'Done', 'Ongoing', 'Testing', 'Deployed')

# SQLAlchemy: Task Details
class Task(db.Model):
    __tablename__= 'tasks'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    status       = db.Column(db.String(20), default=[0])
    task_created = db.Column(db.DateTime, nullable=False)
    date_due     = db.Column(db.String(50))
    # Foreign Keys
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    # Foreign Key Relationships
    profile     = db.relationship('Profile', back_populates='task', cascade ='all, delete')
    employee    = db.relationship('Employee', back_populates='task', cascade ='all, delete')

    # Convert date_due string to date format
    @property
    def formatted_date_due(self):
        return self.date_due.strftime("%d %B, %Y")

# Marshmallow: Task Schema
class TaskSchema(ma.Schema):
    # Nested Attributes
    profile    = fields.List(fields.Nested('ProfileSchema'))
    employee   = fields.List(fields.Nested('EmployeeSchema'), exclude=['password'])

    # Task Validation
    # Must have task name, minimum length of 1 character.
    name = fields.String(required=True, validate=Length(min=1, error='Must be at least 1 character.'))
    # Must be one of the hard-coded values
    status = fields.String(load_default=VALID_STATUSES[0], validate=OneOf(VALID_STATUSES))
    # Must be in format DAY, MONTH, YEAR.
    date_due = fields.String(validate=And(Regexp('^[a-zA-Z0-9]+$', error='Must be in format DAY, MONTH, YEAR')))

    # Defining Fields
    class Meta:
        fields  = ('id', 'name', 'status', 'task_created', 'due_date', 'profile', 'employee')
        ordered = True
