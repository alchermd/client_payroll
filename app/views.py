from . import app
from .forms import LoginForm
from .models import Admin, Employee, Employer, Payment
from flask import flash, redirect, render_template, session, url_for
from functools import wraps
from passlib.hash import pbkdf2_sha256


def login_required(f):
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
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("ADMIN"):
            flash("You are currently logged in.", "info")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
@logout_required
def login():
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
    session.pop("ADMIN", None)
    flash("You are now logged out.", "primary")

    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    payments = Payment.query.all()

    return render_template("dashboard.html", payments=payments)
