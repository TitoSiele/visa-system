import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read the connection string from an environment variable instead of hardcoding
# credentials in source control. Set this in a .env file or your shell before
# starting the app, e.g.:
#   export DATABASE_URL="postgresql://postgres:yourpassword@localhost:5432/immigrationdb"
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:12345@localhost:5432/immigrationdb",  # fallback for local dev only
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()