from flask import Blueprint, request
from datetime import datetime
from init import db
from models.complaint import Complaint, ComplaintSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize

complaints_bp = Blueprint('complaints', __name__, url_prefix='/complaints')

# Retrieve All Complaints
@complaints_bp.route('/complaints/')
def get_all_complaints():
    stmt     = db.select(Complaint)
    complaints = db.session.scalars(stmt)
    return ComplaintSchema(many=True).dump(complaints)

# Retrieve One Complaint
@complaints_bp.route('/<int:id>/')
def get_one_complaint(id):
    stmt    = db.select(Complaint).filter_by(id=id)
    complaint = db.session.scalar(stmt)
    if complaint:
        return ComplaintSchema().dump(complaint)
    else:
        return {'error': f'Complaint not found with id {id}'}, 404

# Create New Complaint
@complaints_bp.route('/<int:id>', methods=['POST'])
def create_complaint():
    # Create new Complaint model instance
    complaint = Complaint( 
        subject     = request.json['subject'],
        description = request.json['description'],
        entry_time  = datetime.now(),
        profile_id  = request.json['profile.id'],
        employee_id = get_jwt_identity(),
    # Foreign Key Relationships 
        profile     = request.json['profile'],
        employee    = request.json['employee']
    )
    # Add and commit user to DB
    db.session.add(complaint)
    db.session.commit()
    # Respond to client
    return ComplaintSchema().dump(complaint), 201

# Update Complaint
@complaints_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
def update_one_complaint(id):
    stmt    = db.select(Complaint).filter_by(id=id)
    complaint = db.session.scalar(stmt)
    if complaint:
        complaint.subject     = request.json.get('subject') or complaint.subject
        complaint.description = request.json.get('description') or complaint.description
        complaint.entry_time  = datetime.now() or complaint.entry_time
        complaint.profile     = request.json.get('profile') or complaint.profile
        complaint.employee    = get_jwt_identity() or complaint.employee
        # Updates Changes
        db.session.commit()
        return ComplaintSchema().dump(complaint)
    else:
        return {'error': f'Complaint not found with id {id}'}, 404 

# Delete Complaint: AUTHORISATION REQUIRED
@complaints_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_complaint(id):
    authorize('admin')
    stmt    = db.select(Complaint).filter_by(id=id)
    complaint = db.session.scalar(stmt)
    if complaint:
        db.session.delete(complaint)
        db.session.commit()
        return {'message':'Complaint deleted successfully'}
    else:
        return {'error': f'Complaint not found with id {id}'}, 404

