import datetime
from . import db


class Admin(db.Model):
    """A superuser that has access to the rest of the application."""
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return f"<Admin {self.username} />"


class Employer(db.Model):
    """An entity that is referenced as the one who pays an Employee."""
    __tablename__ = "employers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    total_amount_paid = db.Column(db.Integer, default=0)
    date_registered = db.Column(db.DateTime, default=datetime.datetime.now())
    payment = db.relationship('Payment',
                              backref=db.backref('employer', lazy=True),
                              cascade="save-update, merge, delete")

    def __str__(self):
        return f"<Employer {self.name} />"


class Employee(db.Model):
    """An entity that is references as the one who is paid by an Employer."""
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    date_employed = db.Column(db.DateTime, default=datetime.datetime.now())
    payment = db.relationship('Payment',
                              backref=db.backref('employee', lazy=True),
                              cascade="save-update, merge, delete")

    def __str__(self):
        return f"<Employee {self.name} />"


class Payment(db.Model):
    """A table that references payments between an Employer and Employee."""
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    amount = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.datetime.now())

    def __str__(self):
        return f"<Payment {self.employer} - {self.employee} />"
