from init import db, ma

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    # profile_id = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'login_name', 'password_hash', 'is_admin')