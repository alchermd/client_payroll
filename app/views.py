from . import app
from .forms import LoginForm
from .models import Admin
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


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()

        if pbkdf2_sha256.verify(form.password.data, admin.password):
            session["ADMIN"] = admin.username
            return redirect(url_for("dashboard"))

        else:
            flash("Incorrect credentials.", "warning")
            return redirect(url_for("login"))

    return render_template("login.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return "welcome to dashboard!"
