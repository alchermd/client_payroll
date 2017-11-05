from . import app, db
from .models import Admin
from passlib.hash import pbkdf2_sha256


@app.cli.command("createsuperuser")
def create_super_user():
    """Create a super user (admin) account."""
    username = None
    password = None

    while username is None or Admin.query.filter_by(username=username).first():
        username = input("Enter desired username: ")

    while password is None or len(password) < 5:
        password = input("Enter desired password (at least 5 characters): ")

    # Save a hahsed version of the password.
    new_admin = Admin(username=username, password=pbkdf2_sha256.hash(password))
    db.session.add(new_admin)
    db.session.commit()

    print("Super user created!")
