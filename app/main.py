from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.security import (
    hash_password,
    verify_password,
    create_access_token)
from app.database import Base, engine, get_db
from app.models import User
from fastapi import Header
from app.security import decode_access_token


app = FastAPI()

posts = []

Base.metadata.create_all(bind=engine)


class Post(BaseModel):
    title: str
    content: str


class UserCreate(BaseModel):
    name: str
    email: str

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

from fastapi import FastAPI, Depends, HTTPException, Header

from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

app = FastAPI()


def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme"
            )

        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return int(user_id)

    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


# Your endpoints come AFTER this
@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user)
):
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to access this user"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

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

    return use
@app.delete("/users/{user_id}")
def delete_user(
    user_id = int ,
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code = 404 , detail = "User not found")
    db.delete(user)
    db.commit()
    return {"message" : "User Deleted Successfully"}



@app.post("/register", status_code=201)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }


@app.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if user is None or not user.hashed_password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(user.id)

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }