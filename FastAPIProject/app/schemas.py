from typing import Optional
from passlib.hash import bcrypt
hash_rounds = 12
from pydantic import BaseModel, EmailStr,conint

from typing import Dict

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    published: bool = True


class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True 

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    owner_id: int
    owner: Optional[UserOut]
    likes: int  

    class Config:
     from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    def hash_password(self):
        self.password = bcrypt.hash(self.password, rounds=hash_rounds)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None 

class VoteSchema(BaseModel): 
    voted_post_id: int
    vote_direction: conint(ge=0, le=1) 
