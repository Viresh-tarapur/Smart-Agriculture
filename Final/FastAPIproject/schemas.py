from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email_address: EmailStr

class UserCreate(UserBase):
    password1: str
    password2: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class BinStatusBase(BaseModel):
    bin_name: str
    status: str

class BinStatus(BinStatusBase):
    id: int

    class Config:
        from_attributes = True

class BinLocationBase(BaseModel):
    location_name: str
    latitude: float
    longitude: float

class BinLocation(BinLocationBase):
    id: int

    class Config:
        from_attributes = True
