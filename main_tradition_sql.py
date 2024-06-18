import time
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg
from psycopg.rows import dict_row


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


try:
    conn = psycopg.connect(host='localhost', dbname='insta', user='postgres',
                           password='PostGRESisCo0L', row_factory=dict_row)

    cursor = conn.cursor()
    print('Database connection was successfull!')
except Exception as error:
    print('Connecting to database failed')
    print("Error: ", error)

# Psycopg2

# while True:

#     try:
#         conn = psycopg2.connect(host='localhost', dbname='insta', user='postgres',
#                                 password='PostGRESisCo0L', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull!')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print("Error: ", error)
#         time.sleep(2)


my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "favorite foods",
        "content": "i like pizza",
        "id": 2
    }
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Welcome to my API"}


@app.get("/posts")
def get_posts():
    # Psycopg2
    # cursor.execute("""SELECT * FROM posts;""")
    # posts = cursor.fetchall()

    posts = cursor.execute("SELECT * FROM posts").fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def def_post(id: int):
    post = cursor.execute(
        """SELECT * FROM posts where id = %s""", (id,)).fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return {"post_detail": post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    new_post = cursor.execute("INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *",
                              (post.title, post.content, post.published)).fetchone()
    conn.commit()
    return {'data': new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    deleted_post = cursor.execute(
        "DELETE FROM posts where id = %s RETURNING *", (id,)).fetchone()

    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put(path='/posts/{id}')
def update_post(id: int, post: Post):
    updated_post = cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                                  (post.title, post.content, post.published, id)).fetchone()

    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    return {'data': updated_post}
