from .models import Employee, Employer
from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")


class UpdatePaymentForm(FlaskForm):
    employer_choices = [ (employer.id, employer.name) for employer in Employer.query.all()]
    employer = SelectField("Employer", choices=employer_choices, coerce=int)

    employee_choices = [ (employee.id, employee.name) for employee in Employee.query.all()]
    employee = SelectField("Employee", choices=employee_choices, coerce=int)

    amount = IntegerField("Amount")

    submit = SubmitField("Save")
