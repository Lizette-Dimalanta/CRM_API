DROP TABLE IF EXISTS profiles;
-- DROP TABLE IF EXISTS customers;

    id          = db.Column(db.Integer, primary_key=True)
    # profile_id = db.Column(db.Integer, db.ForeignKey=True)
    job_title   = db.Column(db.String(50))
    company     = db.Column(db.String(50))
    join_date = db.Column(db.Date)
    expected_end = db.Column(db.Date)

CREATE TABLE profiles(
    id SERIAL PRIMARY KEY NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    address_id INT,
    birthday DATE NOT NULL,
    phone INT,
    email INT,
    FOREIGN KEY(address_id) REFERENCES address_id
)

-- CREATE TABLE customers(
--     id SERIAL PRIMARY KEY NOT NULL,
--     profile_id INT,
--     job_title VARCHAR(50),
--     company = VARCHAR(50),
--     join_date date NOT NULL,
--     expected_end Date,
--     FOREIGN KEY(profile_id) REFERENCES profile_id
-- )
