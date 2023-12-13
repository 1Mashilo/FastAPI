# schemas.py
from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    published: bool = True

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
      from_attributes = True
