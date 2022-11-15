from flask import Blueprint, request
from init import db
from models.profile import Profile, ProfileSchema

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
def create_profile():
    # Create new Profile model instance
    profile = Profile(
        first_name  = request.json['first_name'],
        last_name   = request.json['last_name'],
        birthday    = request.json['birthday'],
        phone       = request.json['phone'],
        email       = request.json['email'],
        is_customer = request.json['is_customer'],
        join_date   = request.json['join_date'],
        occupation   = request.json['occupation'],
        company     = request.json['company'],
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
def update_one_profile(id):
    stmt    = db.select(Profile).filter_by(id=id)
    profile = db.session.scalar(stmt)
    if profile:
        profile.first_name  = request.json.get('first_name') or profile.first_name
        profile.last_name   = request.json.get('last_name') or profile.last_name
        profile.birthday    = request.json.get('birthday') or profile.birthday
        profile.phone       = request.json.get('phone') or profile.phone
        profile.email       = request.json.get('email') or profile.email
        is_customer         = request.json.get('is_customer') or profile.is_customer
        join_date           = request.json.get('join_date') or profile.join_date
        occupation          = request.json.get('occupation') or profile.occupation
        company             = request.json.get('company') or profile.company
        profile.address     = request.json.get('address') or profile.address
        # Updates Changes
        db.session.commit()
        return ProfileSchema().dump(profile)
    else:
        return {'error': f'Profile not found with id {id}'}, 404


@profiles_bp.route('/<int:id>/', methods=['DELETE'])
def delete_one_profile(id):
    stmt    = db.select(Profile).filter_by(id=id)
    profile = db.session.scalar(stmt)
    if profile:
        db.session.delete(profile)
        db.session.commit()
        return {'message':'Profile deleted successfully'}
    else:
        return {'error': f'Profile not found with id {id}'}, 404

