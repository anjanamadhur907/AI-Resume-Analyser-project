from sqlalchemy import Integer, ForeignKey, Numeric, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.dbConfig import Base

class Analysis(Base):
    __tablename__ = 'analysis'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    resume_id:Mapped[int] = mapped_column(ForeignKey("resume.id"), unique=True)
    overall_score:Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    ats_score:Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    summary:Mapped[Text] = mapped_column(Text, nullable=False)
    strength:Mapped[Text] = mapped_column(Text)
    weakness:Mapped[Text] = mapped_column(Text)
    recommendation:Mapped[Text] = mapped_column(Text, nullable=False)
    experience_level:Mapped[str] = mapped_column(String(100))
    education:Mapped[Text] = mapped_column(Text)

    resume:Mapped["Resume"] = relationship("Resume", back_populates="analysis")

    skills:Mapped[list["Skill"]] = relationship("Skill", back_populates="analysis",cascade="all, delete-orphan")
