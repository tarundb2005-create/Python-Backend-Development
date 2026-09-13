from app.database import Base , engine
from sqlalchemy import Column , Integer , String

Base.metadata.create_all(bind = engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer , primary_key = True)
    name = Column(String)
    email = Column(String)

