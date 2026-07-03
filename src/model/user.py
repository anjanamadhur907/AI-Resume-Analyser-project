from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC
from sqlalchemy import DateTime
from src.db.dbConfig import Base


class User(Base):
    __tablename__ = 'user'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False)
    email:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password:Mapped[str] = mapped_column(String(100), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=True
    )
    resumes:Mapped[list["Resume"]] = relationship("Resume", back_populates="user",cascade="all, delete-orphan")