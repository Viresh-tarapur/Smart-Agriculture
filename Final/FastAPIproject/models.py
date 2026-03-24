from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email_address = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    def check_password_correction(self, attempted_password):
        # In a real app, use hashing. Keeping plain text as per original Flask project for now.
        return self.password_hash == attempted_password

class BinStatus(Base):
    __tablename__ = "bin_status"

    id = Column(Integer, primary_key=True, index=True)
    bin_name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # empty, half-filled, full

class BinLocation(Base):
    __tablename__ = "bin_location"

    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
