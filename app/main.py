from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = False  

# Database connection setup
try:
    conn = psycopg2.connect(
        host='localhost',
        database='FastAPI',
        user='postgres',
        password='Mashilo@95',
        cursor_factory=RealDictCursor
    )
    cursor = conn.cursor()
    print("Database connection was successful!")
except Exception as error:
    print(f"Error connecting to the database: {error}")

@app.get("/")
def root():
    """
    Retrieve a welcome message for the root endpoint.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    """
    Retrieve a list of all posts.

    Returns:
        dict: A dictionary containing the list of posts.
    """
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """
    Create a new post.

    Args:
        post (Post): The data for the new post.

    Returns:
        dict: A dictionary containing the newly created post.
    """
    cursor.execute(
        "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
        (post.title, post.content, post.published)
    )
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")
def get_post(id: int):
    """
    Retrieve details of a specific post by ID.

    Args:
        id (int): The ID of the post to retrieve.

    Returns:
        dict: A dictionary containing the details of the specified post.
    """
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found"
        )

    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """
    Delete a post by ID.

    Args:
        id (int): The ID of the post to delete.

    Returns:
        Response: An HTTP response indicating the success of the operation.
    """
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """
    Update a post by ID.

    Args:
        id (int): The ID of the post to update.
        post (Post): The updated data for the post.

    Returns:
        dict: A dictionary containing the updated post.
    """
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    existing_post = cursor.fetchone()

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} does not exist"
        )

    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
        (post.title, post.content, post.published, id)
    )
    updated_post = cursor.fetchone()
    conn.commit()

    return {"post_updated": updated_post}
