from . import app
from .forms import LoginForm
from flask import redirect, render_template, url_for


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Login!")
        return redirect(url_for("login"))

    return render_template("login.html", form=form)
