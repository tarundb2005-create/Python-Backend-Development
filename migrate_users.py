
from sqlalchemy import inspect, text
from app.database import engine

columns = inspect(engine).get_columns("users")
column_names = [column["name"] for column in columns]

if "hashed_password" not in column_names:
    with engine.begin() as conn:
        conn.execute(
            text("ALTER TABLE users ADD COLUMN hashed_password VARCHAR")
        )
    print("Migration successful")
else:
    print("Column already exists")
