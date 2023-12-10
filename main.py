from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    

@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return{"data": "This is your posts"}

@app.post("/createpost")
def createpost(post: Post):
    print(post)
    print(post.dict())
    return {"data": "post"}