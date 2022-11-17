from init import db, ma
from marshmallow import fields

# SQLAlchemy: Task Details
class Task(db.Model):
    __tablename__= 'tasks'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    status       = db.Column(db.String(20), nullable=False)
    task_created = db.Column(db.DateTime, nullable=False)
    date_due     = db.Column(db.String(50))
    # Foreign Keys
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    # Foreign Key Relationships
    profile     = db.relationship('Profile', back_populates='task', cascade ='all, delete')
    employee    = db.relationship('Employee', back_populates='task', cascade ='all, delete')

    @property
    def formatted_date_due(self):
        return self.date_due.strftime("%m/%Y")

# Marshmallow: Task Schema
class TaskSchema(ma.Schema):
    # Nested Attributes
    profile    = fields.List(fields.Nested('ProfileSchema'))
    employee   = fields.List(fields.Nested('EmployeeSchema'), exclude=['password'])

    class Meta:
        fields  = ('id', 'name', 'status', 'task_created', 'due_date', 'profile', 'employee')
        ordered = True