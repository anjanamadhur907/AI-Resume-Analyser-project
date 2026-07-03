from sqlalchemy import select

from src.model.analysis import Analysis


class AnalysisRepository:
    def __init__(self, session):
        self.session = session

    async def save_analysis(self, analysis: Analysis):
        self.session.add(analysis)
        await self.session.flush()
        await self.session.refresh(analysis)
        return analysis

    async def get_analysis_by_resume(self, resume_id: int):
        stmt = select(Analysis).where(
            Analysis.resume_id == resume_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_analysis(self, analysis: Analysis):
        self.session.add(analysis)
        await self.session.flush()
        await self.session.refresh(analysis)
        return analysis