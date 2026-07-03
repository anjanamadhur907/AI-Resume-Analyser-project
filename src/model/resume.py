from sqlalchemy import Integer, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.dbConfig import Base

class Resume(Base):
    __tablename__ = "resume"
    id:Mapped[str] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[str] = mapped_column(ForeignKey("user.id"), nullable=False)
    file_name:Mapped[str] = mapped_column(String(200), nullable=False)
    file_path:Mapped[str] = mapped_column(String(300), nullable=False)
    resume_text:Mapped[Text] = mapped_column(Text, nullable=True)
    stored_file_name = mapped_column(String(255), nullable=False)

    user:Mapped["User"] = relationship("User",back_populates="resumes")
    analysis:Mapped["Analysis"] = relationship("Analysis",back_populates="resume",cascade="all, delete-orphan")