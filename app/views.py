from . import app, db
from .forms import EmployeeForm, EmployerForm, LoginForm, PaymentForm
from .models import Admin, Employee, Employer, Payment
from flask import flash, redirect, render_template, session, url_for
from functools import wraps
from passlib.hash import pbkdf2_sha256


def login_required(f):
    """Requires a logged in ADMIN account."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("ADMIN") is None:
            flash("Please login to continue", "info")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Looks awfully the same as login_required.
# TODO: DRY this up!
def logout_required(f):
    """Requires that no ADMIN account is logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("ADMIN"):
            flash("You are currently logged in.", "info")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@app.template_filter("time_format")
def time_format(timestamp):
    """ Format a timestamp as 'Month Day, Year - HourPM' """
    return timestamp.strftime("%b %d, %Y - %I%p")


@app.route("/")
def index():
    """Force the root url to the /login endpoint."""
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    """View for logging in users."""
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()

        if admin is not None and pbkdf2_sha256.verify(form.password.data, admin.password):
            session["ADMIN"] = admin.username
            return redirect(url_for("dashboard"))

        else:
            flash("Incorrect credentials.", "warning")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """View for logging out users."""
    session.pop("ADMIN", None)
    flash("You are now logged out.", "primary")

    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """View for displaying and creating Payments."""
    payments = Payment.query.all()
    form = PaymentForm()

    # Dynamically generate the select fields.
    form.employee.choices = [(employee.id, employee.name) for employee in Employee.query.all()]
    form.employer.choices = [(employer.id, employer.name) for employer in Employer.query.all()]

    if form.validate_on_submit():
        new_payment = Payment(
            employer_id=form.employer.data, employee_id=form.employee.data,
            amount=form.amount.data, payment_date=form.payment_date.data)

        # Add the amount to the employer's total amount paid.
        employer = Employer.query.filter_by(id=form.employer.data).first()
        employer.total_amount_paid += form.amount.data

        # Add the amount to the employee's total salary.
        employee = Employee.query.filter_by(id=form.employee.data).first()
        employee.total_salary += form.amount.data

        db.session.add(new_payment)
        db.session.commit()

        flash("Payment created.", "success")
        return redirect(url_for("dashboard"))

    return render_template("dashboard.html", payments=payments, form=form)


@app.route("/dashboard/payments/<int:payment_id>", methods=["GET", "POST"])
@login_required
def payment_permalink(payment_id):
    """View for displaying and updating a specific Payment."""
    payment = Payment.query.filter_by(id=payment_id).first()
    if payment is None:
        flash("No such entry found.", "warning")
        return redirect(url_for("dashboard"))

    form = PaymentForm()

    # Dynamically generate the select fields.
    form.employee.choices = [(employee.id, employee.name) for employee in Employee.query.all()]
    form.employer.choices = [(employer.id, employer.name) for employer in Employer.query.all()]

    if form.validate_on_submit():
        # Save the form data into the Payment object.
        payment.employer_id = form.employer.data
        payment.employee_id = form.employee.data
        payment.amount = form.amount.data
        payment.payment_date = form.payment_date.data

        db.session.add(payment)
        db.session.commit()

        flash("Payment updated.", "success")
        return redirect(url_for("dashboard"))

    return render_template("payment_permalink.html", payment=payment, form=form)


@app.route("/dashboard/payments/<int:payment_id>/delete")
@login_required
def delete_payment(payment_id):
    """View for deleting Payments."""
    payment = Payment.query.filter_by(id=payment_id).first()
    if payment is None:
        flash("No such entry found.", "warning")
        return redirect(url_for("dashboard"))

    db.session.delete(payment)
    db.session.commit()

    flash("Payment deleted", "danger")
    return redirect(url_for("dashboard"))


@app.route("/dashboard/employers/", methods=["GET", "POST"])
@login_required
def employers():
    """View for displaying and creating Employers."""
    employers = Employer.query.all()
    form = EmployerForm()

    if form.validate_on_submit():
        new_employer = Employer(name=form.name.data, total_amount_paid=form.total_amount_paid.data)
        db.session.add(new_employer)
        db.session.commit()

        flash("Employer created", "success")
        return redirect(url_for("employers"))

    print(form.errors)

    return render_template("employers.html", employers=employers, form=form)


@app.route("/dashboard/employers/<int:employer_id>", methods=["GET", "POST"])
@login_required
def employer_permalink(employer_id):
    """View for displaying and updating a specific Employer."""
    employer = Employer.query.filter_by(id=employer_id).first()

    if employer is None:
        flash("Employer not found.", "warning")
        return redirect(url_for("employers"))

    form = EmployerForm()
    if form.validate_on_submit():
        # Save the form data into the Employer object.
        employer.name = form.name.data
        employer.total_amount_paid = form.total_amount_paid.data

        db.session.add(employer)
        db.session.commit()

        flash("Employer info updated.", "success")
        return redirect(url_for("employers"))

    return render_template("employer_permalink.html", employer=employer, form=form)


@app.route("/dashboard/employers/<int:employer_id>/delete")
@login_required
def delete_employer(employer_id):
    """View for deleting Employers."""
    employer = Employer.query.filter_by(id=employer_id).first()

    if employer is None:
        flash("Employer not found.", "warning")
        return redirect(url_for("employers"))

    db.session.delete(employer)
    db.session.commit()

    flash("Employer deleted.", "danger")
    return redirect(url_for("employers"))


@app.route("/dashboard/employees/", methods=["GET", "POST"])
@login_required
def employees():
    """View for displaying and creating Employees."""
    employees = Employee.query.all()
    form = EmployeeForm()

    if form.validate_on_submit():
        new_employee = Employee(name=form.name.data, date_employed=form.date_employed.data)
        db.session.add(new_employee)
        db.session.commit()

        flash("Employee created.", "success")
        return redirect(url_for("employees"))

    return render_template("employees.html", employees=employees, form=form)


@app.route("/dashboard/employees/<int:employee_id>", methods=["GET", "POST"])
@login_required
def employee_permalink(employee_id):
    """View for displaying and updating a specific Employee."""
    employee = Employee.query.filter_by(id=employee_id).first()

    if employee is None:
        flash("Employee not found.", "warning")
        return redirect(url_for("employees"))

    form = EmployeeForm()
    if form.validate_on_submit():
        # Save form data into the Employee object.
        employee.name = form.name.data
        employee.date_employed = form.date_employed.data

        db.session.add(employee)
        db.session.commit()

        flash("Employee info updated.", "success")
        return redirect(url_for("employees"))

    return render_template("employee_permalink.html", employee=employee, form=form)


@app.route("/dashboard/employees/<int:employee_id>/delete")
@login_required
def delete_employee(employee_id):
    """View for deleting an Employee."""
    employee = Employee.query.filter_by(id=employee_id).first()

    if employee is None:
        flash("Employee not found.", "warning")
        return redirect(url_for("employees"))

    db.session.delete(employee)
    db.session.commit()

    flash("Employee deleted.", "danger")
    return redirect(url_for("employees"))
