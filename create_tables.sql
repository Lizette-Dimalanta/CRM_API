CREATE TABLE "Address" (
  "address_id" int NOT NULL,
  "apartment_number" int[10],
  "street_number" int[10] NOT NULL,
  "street_name" varchar(50) NOT NULL,
  "street_type" varchar(50) NOT NULL,
  "suburb" varchar(50) NOT NULL,
  "state" varchar(50) NOT NULL,
  "zip" int[5] NOT NULL,
  "country" varchar(50),
  PRIMARY KEY ("address_id")
);

CREATE TABLE "Login" (
  "login_id" int NOT NULL,
  "employee_id" int NOT NULL,
  "user_login" varchar(50) NOT NULL, unique=True,
  "password_hash" varchar(50) NOT NULL,
  "is_admin" bool default=False,
  PRIMARY KEY ("login_id")
);

CREATE TABLE "Customer_Reference" (
  "customer_reference_id" int NOT NULL,
  "task_id" int NOT NULL,
  "note_id" int NOT NULL,
  "customer_id" Type,
  PRIMARY KEY ("customer_reference_id")
);

CREATE TABLE "Employee" (
  "employee_id" int NOT NULL,
  "profile_id" int NOT NULL,
  "hire_date" date,
  PRIMARY KEY ("employee_id")
);

CREATE TABLE "Customer" (
  "customer_id" int NOT NULL,
  "profile_id" int NOT NULL,
  "join_date" date,
  "expected_close" datetime,
  "job_title" varchar(50) NOT NULL,
  "company" varchar(50) NOT NULL,
  PRIMARY KEY ("customer_id")
);

CREATE TABLE "Task" (
  "task_id" int NOT NULL,
  "employee_id" int NOT NULL,
  "task_name" varchar(100) NOT NULL,
  "task_due" datetime,
  "customer_reference_id" int NOT NULL,
  PRIMARY KEY ("task_id"),
  CONSTRAINT "FK_Task.task_id"
    FOREIGN KEY ("task_id")
      REFERENCES "Customer_Reference"("task_id"),
  CONSTRAINT "FK_Task.employee_id"
    FOREIGN KEY ("employee_id")
      REFERENCES "Employee"("employee_id")
);

CREATE TABLE "Note" (
  "note_id" int NOT NULL,
  "employee_id" int NOT NULL,
  "note_title" varchar(50) NOT NULL,
  "note_description" varchar(1000),
  "entry_time" datetime,
  "customer_reference_id" int NOT NULL,
  PRIMARY KEY ("note_id"),
  CONSTRAINT "FK_Note.note_id"
    FOREIGN KEY ("note_id")
      REFERENCES "Customer_Reference"("note_id")
);

CREATE TABLE "Profile" (
  "profile_id" int NOT NULL,
  "first_name" varchar(50) NOT NULL,
  "last_name" varchar(50) NOT NULL,
  "birthday" date,
  "phone" int[11] NOT NULL, unique=True,
  "email" varchar(50) NOT NULL, unique=True,
  "address_id" datetime NOT NULL,
  PRIMARY KEY ("profile_id"),
  CONSTRAINT "FK_Profile.address_id"
    FOREIGN KEY ("address_id")
      REFERENCES "Address"("address_id")
);

