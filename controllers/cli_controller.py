from flask import Blueprint
from init import db, bc
from models.profile import Profile
from models.address import Address
# from models.customer import Customer

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
    profiles = [
        Profile(
        first_name  = 'Michelle',
        last_name   = 'Joy',
        birthday    = '24-08-1987',
        phone       = '0474397540',
        email = 'michellejoy@email.com',
    )
    ]

    addresses = [
        Address(
            apt_number = '2',
            street_number = '8',
            street_name = 'Hurricane',
            street_type = 'Lane',
            suburb      = 'Noosa',
            state       = 'Queensland',
            zip         = '4562',
            country     = 'Australia'
        )
    ]

    # Add information into commit
    db.session.add_all(profiles)
    # Push to database
    db.session.commit()

    # customers = [
    #     Customer(
    #         join_date       = '24-05-2022',
    #         expected_close  = '31-06-2023',
    #         job_title       = 'Lead Vocalist',
    #         company         = 'Cannons'
    #     )
    # ]

    # # Add information into commit
    # db.session.add_all(customers)
    # # Push to database
    # db.session.commit()

    print('Tables Seeded.')