# schemas.py
from passlib.hash import bcrypt
hash_rounds = 12
from pydantic import BaseModel, EmailStr
from typing import Dict
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    published: bool = True

class PostResponse(BaseModel):
    title: str
    content: str
    published: bool = True
    class Config:
     from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    def hash_password(self):
        self.password = bcrypt.hash(self.password, rounds=hash_rounds)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
     arbitrary_types_allowed = True