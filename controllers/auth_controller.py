from flask import Blueprint, request
from init import db, bc
from datetime import timedelta
from models.employee import Employee, EmployeeSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/employees/')
def get_employees():
    stmt = db.select(Employee)
    employees = db.session.scalars(stmt)
    return EmployeeSchema(exclude=['password']).dump(employees)

@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try:
        # Create new Auth model instance from employee info
        employee = Employee(
            username   = request.json['username'],
            password   = bc.generate_password_hash(request.json['password']).decode('utf8'),
        )
        # Updates Changes
        db.session.add(employee)
        db.session.commit()
        # Respond to client
        return EmployeeSchema().dump(employee), 201
    except IntegrityError:
        return {'error': 'Username already in use'}, 409

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Find employee by username
    stmt        = db.select(Employee).filter_by(username=request.json['username'])
    employee    = db.session.scalar(stmt)
    # If employee exists and password is correct:
    if employee and bc.check_password(employee.password, request.json['password']):
        # Return EmployeeSchema(exclude=['password']).dump(employee)
        token   = create_access_token(identity=str(employee.id), expires_delta=timedelta(days=1))
        return {'username': employee.username, 'token': token, 'is_admin': employee.is_admin}
    else:
        return {'error': 'Invalid username or password'}, 401

# Authorization
def authorize():
    employee_id = get_jwt_identity()
    stmt        = db.select(Employee).filter_by(id=employee_id)
    employee    = db.session.scalar(stmt)
    if not employee.is_admin:
        abort(401)