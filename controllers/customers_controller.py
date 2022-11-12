from flask import Blueprint
from db import db
from models.customer import Customer, CustomerSchema

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customers_bp.route('/')
# @jwt_required()
def all_customers():
    stmt= db.select(Customer).order_by(Customer.priority.desc(), Customer.title)
    customers = db.session.scalars(stmt)
    return CustomerSchema(many=True).dump(customers)

@customers_bp.route('/<int:id>/')
def one_customer(id):
    stmt= db.select(Customer).filter_by(id=id)
    customer = db.session.scalar(stmt)
    return CustomerSchema().dump(customer)