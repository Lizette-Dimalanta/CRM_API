from flask import Blueprint, request
from init import db
from models.address import Address, AddressSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize

addresses_bp = Blueprint('addresses', __name__, url_prefix='/addresses')

# Retrieve All Addresses: AUTHORISATION REQUIRED
@addresses_bp.route('/')
@jwt_required()
def get_all_addresses():
    authorize()
    stmt      = db.select(Address)
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)

# Retrieve One Address: AUTHORISATION REQUIRED
@addresses_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_one_address(id):
    authorize()
    stmt    = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    if address:
        return AddressSchema().dump(address)
    else:
        return {'error': f'Addresses not found with id {id}'}, 404

# Create New Address: AUTHORISATION REQUIRED
@addresses_bp.route('/', methods=['POST'])
@jwt_required()
def create_address():
    authorize()
    # Create new Address model instance
    address = Address(
        apt_number      = request.json['apt_number'],
        street_number   = request.json['street_number'],
        street_name     = request.json['street_name'],
        suburb          = request.json['suburb'],
        street_type     = request.json['street_type'],
        state           = request.json['state'],
        zip             = request.json['zip'],
        country         = request.json['country'],
        employee_id     = get_jwt_identity()
    )
    # Add and commit user to DB
    db.session.add(address)
    db.session.commit()
    # Respond to client
    return AddressSchema().dump(address), 201

# Update Address: AUTHORISATION REQUIRED
@addresses_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_address(id):
    authorize()
    stmt    = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    if address:
        address.apt_number      = request.json.get('apt_number') or address.apt_number
        address.street_number   = request.json.get('street_number') or address.street_number
        address.street_name     = request.json.get('street_name') or address.street_name
        address.suburb          = request.json.get('suburb') or address.suburb
        address.street_type     = request.json.get('street_type') or address.street_type
        address.state           = request.json.get('state') or address.state
        address.zip             = request.json.get('zip') or address.zip
        address.country         = request.json.get('country') or address.country
        # Updates Changes
        db.session.commit()
        return AddressSchema().dump(address)
    else:
        return {'error': f'Address not found with id {id}'}, 404

# Delete Address: AUTHORISATION REQUIRED
@addresses_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_address(id):
    authorize()
    stmt    = db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    if address:
        db.session.delete(address)
        db.session.commit()
        return {'message':'Address deleted successfully'}
    else:
        return {'error': f'Address not found with id {id}'}, 404

