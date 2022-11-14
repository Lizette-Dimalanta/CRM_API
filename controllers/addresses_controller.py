from flask import Blueprint, Request
from init import db
from models.address import Address, AddressSchema

addresses_bp = Blueprint('addresses', __name__, url_prefix='/addresses')

@addresses_bp.route('/')
# @jwt_required()
def all_addresses():
    stmt= db.select(Address)
    addresses = db.session.scalars(stmt)
    return AddressSchema(many=True).dump(addresses)

@addresses_bp.route('/<int:id>/')
def one_address(id):
    stmt= db.select(Address).filter_by(id=id)
    address = db.session.scalar(stmt)
    if address:
        return AddressSchema().dump(address)
    else:
        return {'error': f'Addresses not found with id {id}'}, 404