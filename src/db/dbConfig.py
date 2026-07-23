from dotenv import load_dotenv
import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

db_url = os.getenv("DB_URL")

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(db_url, echo=True)

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass