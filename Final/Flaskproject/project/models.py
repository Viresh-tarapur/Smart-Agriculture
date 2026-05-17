from project import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    # Load and return the user from the database based on the user ID
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    def __repr__(self):
        return f'User(username={self.username}, email_address={self.email_address})'

    def check_password_correction(self, attempted_password):
        # Compare the provided password with the stored password (plain text comparison)
        return self.password_hash == attempted_password
    
    def get_id(self):
        return str(self.id)

class BinStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bin_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # empty, half-filled, full

    def __repr__(self):
        return f'BinStatus(bin_name={self.bin_name}, status={self.status})'

class BinLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'BinLocation(location_name={self.location_name}, latitude={self.latitude}, longitude={self.longitude})'
