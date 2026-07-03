from src.model.skill import Skill
from src.repository.skill_repository import SkillRepository


class SkillService:

    def __init__(self, session):
        self.skill_repo = SkillRepository(session)

    async def save_skills(
            self,
            analysis_id: int,
            skills: list[str]
    ):
        for skill_name in skills:
            skill = Skill(
                analysis_id=analysis_id,
                skill_name=skill_name,
                found=True
            )
            await self.skill_repo.save_skill(skill)