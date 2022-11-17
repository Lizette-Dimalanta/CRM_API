from flask import Blueprint, request
from datetime import date
from init import db
from models.profile import Profile, ProfileSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize

profiles_bp = Blueprint('profiles', __name__, url_prefix='/profiles')

@profiles_bp.route('/')
# @jwt_required()
def get_all_profiles():
    stmt     = db.select(Profile)
    profiles = db.session.scalars(stmt)
    return ProfileSchema(many=True).dump(profiles)

@profiles_bp.route('/<int:id>/')
def get_one_profile(id):
    stmt    = db.select(Profile).filter_by(id=id)
    profile = db.session.scalar(stmt)
    if profile:
        return ProfileSchema().dump(profile)
    else:
        return {'error': f'Profile not found with id {id}'}, 404

@profiles_bp.route('/', methods=['POST'])
@jwt_required()
def create_profile():
    authorize()
    # Create new Profile model instance
    profile = Profile(
        first_name  = request.json['first_name'],
        last_name   = request.json['last_name'],
        phone       = request.json['phone'],
        email       = request.json['email'],
        is_customer = request.json['is_customer'],
        join_date   = date.today(),
        occupation  = request.json['occupation'],
        company     = request.json['company'],
        employee_id = get_jwt_identity(),
    # Foreign Key Relationship
        address     = request.json['address']
    )
    # Add and commit user to DB
    db.session.add(profile)
    db.session.commit()
    # Respond to client
    return ProfileSchema().dump(profile), 201
# Add unique error: already in use
# except IntegrityError:
#     return {'error': 'Email address already in use'}, 409

@profiles_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_profile(id):
    authorize()
    stmt    = db.select(Profile).filter_by(id=id)
    profile = db.session.scalar(stmt)
    if profile:
        profile.first_name  = request.json.get('first_name') or profile.first_name
        profile.last_name   = request.json.get('last_name') or profile.last_name
        profile.phone       = request.json.get('phone') or profile.phone
        profile.email       = request.json.get('email') or profile.email
        profile.is_customer = request.json.get('is_customer') or profile.is_customer
        profile.join_date   = request.json.get('join_date') or profile.join_date
        profile.occupation  = request.json.get('occupation') or profile.occupation
        profile.company     = request.json.get('company') or profile.company
        profile.address     = request.json.get('address') or profile.address
        # Updates Changes
        db.session.commit()
        return ProfileSchema().dump(profile)
    else:
        return {'error': f'Profile not found with id {id}'}, 404


@profiles_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_profile(id):
    authorize('admin')
    stmt    = db.select(Profile).filter_by(id=id)
    profile = db.session.scalar(stmt)
    if profile:
        db.session.delete(profile)
        db.session.commit()
        return {'message':'Profile deleted successfully'}
    else:
        return {'error': f'Profile not found with id {id}'}, 404

