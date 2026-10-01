from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import User


app = FastAPI()

posts = []

Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    content: str


class UserCreate(BaseModel):
    name: str
    email: str


@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users")
def get_users(db : Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{user_id}")
def get_user(user_id : int , db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code = 404 ,detail = "User Not Found")
    return user

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_data.name
    user.email = user_data.email

    db.commit()
    db.refresh(user)

    return user
