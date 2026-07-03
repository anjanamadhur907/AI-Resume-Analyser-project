from sqlalchemy import Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.dbConfig import Base

class Skill(Base):
    __tablename__ = 'skill'
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    analysis_id:Mapped[int] = mapped_column(ForeignKey("analysis.id"))
    skill_name:Mapped[str] = mapped_column(String(100))
    found:Mapped[bool] = mapped_column(Boolean)

    analysis:Mapped["Analysis"] = relationship("Analysis", back_populates="skills")