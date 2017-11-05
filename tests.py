import unittest
from app import app
from app.models import db, Admin
from passlib.hash import pbkdf2_sha256


class ClientPayrollTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_new_account_can_be_verified(self):
        # Create a dummy admin account.
        username = "dummy"
        password = "dummy"
        self.dummy_admin = Admin(username=username, password=pbkdf2_sha256.hash(password))
        db.session.add(self.dummy_admin)
        db.session.commit()

        # Execute a query and verify the admin data.
        admin = Admin.query.filter_by(username=username).first()
        self.assertTrue(pbkdf2_sha256.verify(password, admin.password), "Account cannot be verified.")

    def tearDown(self):
        db.session.delete(self.dummy_admin)
        db.session.commit()


if __name__ == "__main__":
    unittest.main()
