from init import db, ma

class Customer(db.Model):
    __tablename__= 'customers'

    id          = db.Column(db.Integer, primary_key=True)
    # profile_id = db.Column(db.Integer, db.ForeignKey=True)
    job_title   = db.Column(db.String(50))
    company     = db.Column(db.String(50))
    join_date = db.Column(db.Date)
    expected_end = db.Column(db.Datetime)

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'job_title', 'company', 'join_date', 'expected_end')
        ordered = True