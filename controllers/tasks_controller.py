from flask import Blueprint, request
from datetime import datetime
from init import db
from models.task import Task, TaskSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Retrieve All Tasks
@tasks_bp.route('/')
def get_all_tasks():
    stmt     = db.select(Task)
    tasks = db.session.scalars(stmt)
    return TaskSchema(many=True).dump(tasks)

# Retrieve One Task
@tasks_bp.route('/<int:id>/')
def get_one_task(id):
    stmt    = db.select(Task).filter_by(id=id)
    task = db.session.scalar(stmt)
    if task:
        return TaskSchema().dump(task)
    else:
        return {'error': f'Task not found with id {id}'}, 404

# Create New Task: AUTHORISATION REQUIRED
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    authorize()
    # Create new Task model instance
    task = Task( 
        name     = request.json['name'],
        status = request.json['status'],
        task_created  = datetime.now(),
        task_due = datetime(),
        profile_id  = request.json['profile.id'],
        employee_id = get_jwt_identity(),
    # Foreign Key Relationships 
        profile     = request.json['profile'],
        employee    = request.json['employee']
    )
    # Add and commit user to DB
    db.session.add(task)
    db.session.commit()
    # Respond to client
    return TaskSchema().dump(task), 201

# Update Task: AUTHORISATION REQUIRED
@tasks_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_task(id):
    authorize()
    stmt    = db.select(Task).filter_by(id=id)
    task = db.session.scalar(stmt)
    if task:
        task.name     = request.json.get('name') or task.name
        task.status = request.json.get('status') or task.status
        task.task_created  = datetime.now() or task.task_created
        task.task_due = datetime() or task.task_due
        task.profile     = request.json.get('profile') or task.profile
        task.employee    = get_jwt_identity() or task.employee
        # Updates Changes
        db.session.commit()
        return TaskSchema().dump(task)
    else:
        return {'error': f'Task not found with id {id}'}, 404 

# Delete Task: AUTHORISATION REQUIRED
@tasks_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_task(id):
    authorize()
    stmt    = db.select(Task).filter_by(id=id)
    task = db.session.scalar(stmt)
    if task:
        db.session.delete(task)
        db.session.commit()
        return {'message':'Task deleted successfully'}
    else:
        return {'error': f'Task not found with id {id}'}, 404

