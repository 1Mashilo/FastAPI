from typing import Optional
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    """Base schema for creating a post."""
    title: str
    content: str


class PostCreate(PostBase):
    """Schema for creating a post with an optional 'published' field."""
    published: bool = True


class UserOut(BaseModel):
    """Schema for representing user data in the output."""
    id: int
    email: EmailStr


    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    """Schema for representing post data in the response."""
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
    """Schema for creating a user."""
    email: EmailStr
    password: str


    def hash_password(self):
        """Hash the user's password using bcrypt."""
        self.password = bcrypt.hash(self.password, rounds=12)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for representing an access token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for representing token data."""
    id: Optional[str] = None


class VoteSchema(BaseModel):
    """Schema for representing a vote."""
    voted_post_id: int
    vote_direction: conint(ge=0, le=1)
