from sqlalchemy import select

from src.model.skill import Skill


class SkillRepository:

    def __init__(self, session):
        self.session = session

    async def save_skill(self, skill: Skill):
        self.session.add(skill)
        await self.session.flush()
        await self.session.refresh(skill)
        return skill

    async def get_skills_by_analysis(self, analysis_id: int):
        stmt = select(Skill).where(
            Skill.analysis_id == analysis_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()