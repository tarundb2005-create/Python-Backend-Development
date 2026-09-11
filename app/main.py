from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()

posts = []

class Post(BaseModel):
    title : str
    content : str

@app.get("/")
def root():
    return {"message" : "Here are the Posts"}

@app.get("/posts")
def get_posts(limit : int = 10 , skip : int = 0):
    return posts[skip:skip + limit]

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    return {
            "post_id" : post_id
    }

@app.post("/posts")
def get_posts(post : Post):
    posts.append(post : Post)
    return post

@app.put("/posts/{post_id}")
def update_posts(post_id : int , post : Post):
    for p in posts:
        if p["id"] == post_id:
            p["itle"] = post.title,
            p["content"] = post.content
            return p
    raise HTTPException(
        status_code = 404,
        detail= "Post not found"
    )