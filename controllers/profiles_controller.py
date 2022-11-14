from flask import Blueprint, Request
from init import db
from models.profile import Profile, ProfileSchema

profiles_bp = Blueprint('profiles', __name__, url_prefix='/profiles')

@profiles_bp.route('/')
# @jwt_required()
def all_profiles():
    stmt= db.select(Profile)
    profiles = db.session.scalars(stmt)
    return ProfileSchema(many=True).dump(profiles)

@profiles_bp.route('/<int:id>/')
def one_profile(id):
    stmt= db.select(Profile).filter_by(id=id)
    profile = db.session.scalar(stmt)
    if profile:
        return ProfileSchema().dump(profile)
    else:
        return {'error': f'Profile not found with id {id}'}, 404