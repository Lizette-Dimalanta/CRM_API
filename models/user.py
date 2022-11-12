from main import db

class User(db.Model):
    __tablename__= 'users'

    id          = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(50) NOT NULL)
    last_name   = db.Column(db.String(100) NOT NULL)
    DOB         = db.Column(db.Datetime)
    job_title   = db.Column(db.String(50))
    company     = db.Column(db.String(50))
    join_date = db.Column(db.Date NOT NULL)
    expected_end = db.Column(db.Datetime)
    # employment_type_id = db.Column(db.Integer, foreign_key=True)
    # address_id = db.Column(db.Integer, foreign_key=True)
