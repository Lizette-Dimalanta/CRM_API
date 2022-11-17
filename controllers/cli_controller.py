from flask import Blueprint
from init import db, bc
from datetime import datetime, date
from models.employee import Employee
from models.profile import Profile
from models.address import Address
from models.complaint import Complaint
from models.task import Task

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

# Seed Database
@db_commands.cli.command('seed')
def seed_db():
    profiles = [
        Profile(
            first_name  = 'Michelle',
            last_name   = 'Joy',
            phone       = '0474397540',
            email       = 'michellejoy@email.com',
            is_customer = False,
            join_date   = date.today(),
            occupation  = 'Lead Vocalist',
            company     = 'Cannons'
    )
    ]

    # Add profiles to database
    db.session.add_all(profiles)
    # Push to database
    db.session.commit()

    addresses = [
        Address(
            apt_number    = '2',
            street_number = '8',
            street_name   = 'Hurricane',
            street_type   = 'Lane',
            suburb        = 'Noosa',
            state         = 'Queensland',
            zip           = '4562',
            country       = 'Australia',
            profile       = profiles[0]
        )
    ]

    # Add employees to database
    db.session.add_all(addresses)
    # Push to database
    db.session.commit()

    employees = [
        Employee(
            username = 'devtest',
            password = bc.generate_password_hash('frenchfries').decode('utf-8'),
            is_admin = True,
            profile  = profiles[0]
        )
    ]

    # Add complaints to database
    db.session.add_all(employees)
    # Push to database
    db.session.commit()

    complaints = [
        Complaint(
            subject     = 'Devtest 1',
            description = 'This is a test complaint.',
            entry_time  = datetime.now(),
            profile     = profiles[0],
            employee    = employees[0]
        )
    ]

    # Add complaints to database
    db.session.add_all(complaints)
    # Push to database
    db.session.commit()

    tasks = [
        Task(
            name         = 'Send report to client',
            status       = 'In Progress',
            task_created = datetime.now(),
            date_due     = 'Wednesday, 15 December 2022',
            profile      = profiles[0],
            employee     = employees[0]
        )
    ]

    # Add tasks to database
    db.session.add_all(tasks)
    # Push to database
    db.session.commit()

    print('Tables Seeded.')