from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from sqlalchemy import Column, Integer, String

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = engine
)

Base = declarative_base()




