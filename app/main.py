from fastapi import FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool

@app.get("/")
def root():
    """
    Retrieve a welcome message for the root endpoint.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    """
    Retrieve a list of all posts.

    Returns:
        dict: A dictionary containing the list of posts.
    """
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    """
    Create a new post.

    Args:
        post (Post): The data for the new post.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the newly created post.
    """
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {"data": db_post}

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    """
    Retrieve details of a specific post by ID.

    Args:
        id (int): The ID of the post to retrieve.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the details of the specified post.
    """
    db_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    return {"post_detail": db_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    """
    Delete a post by ID.

    Args:
        id (int): The ID of the post to delete.
        db (Session): The database session.

    Returns:
        Response: An HTTP response indicating the success of the operation.
    """
    db_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    db.delete(db_post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    """
    Update a post by ID.

    Args:
        id (int): The ID of the post to update.
        post (Post): The updated data for the post.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the updated post.
    """
    db_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    for key, value in post.dict().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)

    return {"post_updated": db_post}
