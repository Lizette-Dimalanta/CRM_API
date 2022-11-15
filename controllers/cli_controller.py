from flask import Blueprint
from init import db, bc
from datetime import date
from models.employee import Employee
from models.profile import Profile
from models.address import Address

db_commands = Blueprint('db', __name__)

# Create Database
@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables Created.")

# Drop Database
@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables Dropped.")

@db_commands.cli.command('seed')
def seed_db():
    addresses = [
        Address(
            apt_number    = '2',
            street_number = '8',
            street_name   = 'Hurricane',
            street_type   = 'Lane',
            suburb        = 'Noosa',
            state         = 'Queensland',
            zip           = '4562',
            country       = 'Australia'
        )
    ]

    # Add employees to database
    db.session.add_all(addresses)
    # Push to database
    db.session.commit()

    profiles = [
        Profile(
            first_name  = 'Michelle',
            last_name   = 'Joy',
            birthday    = '24-08-1987',
            phone       = '0474397540',
            email       = 'michellejoy@email.com',
            is_customer = False,
            join_date   = '28-10-2020',
            occupation  = 'Lead Vocalist',
            company     = 'Cannons',
            address     = addresses[0]
    )
    ]

    # Add profiles to database
    db.session.add_all(profiles)
    # Push to database
    db.session.commit()

    employees = [
        Employee(
            username = 'devtest',
            password = bc.generate_password_hash('french fires').decode('utf-8'),
            is_admin = True,
            profile = profiles[0]
        )
    ]

    # Add employees to database
    db.session.add_all(employees)
    # Push to database
    db.session.commit()

    print('Tables Seeded.')