from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.model import Analysis
from src.model.resume import Resume

class DashboardRepository:

    def __init__(self, session):
        self.session = session

    async def get_all_resume(self, user_id: int):
        stmt = (
            select(Resume)
            .where(Resume.user_id == user_id)
            .order_by(Resume.id.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_resume(self, resume_id: int):
        stmt = (
            select(Resume)
            .options(
                selectinload(Resume.analysis)
                .selectinload(Analysis.skills)
            )
            .where(Resume.id == resume_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()