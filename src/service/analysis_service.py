from src.model.analysis import Analysis
from src.repository.analysis_repository import AnalysisRepository
from src.service.skill_service import SkillService


class AnalysisService:

    def __init__(self, session):
        self.analysis_repo = AnalysisRepository(session)
        self.skill_service = SkillService(session)

    async def save_analysis(
            self,
            resume_id: int,
            ai_response: dict
    ):
        analysis = Analysis(
            resume_id=resume_id,
            overall_score=ai_response["overall_score"],
            ats_score=ai_response["ats_score"],
            summary=ai_response["summary"],
            strength="\n".join(ai_response["strengths"]),
            weakness="\n".join(ai_response["weaknesses"]),
            recommendation="\n".join(ai_response["recommendations"]),
            experience_level=ai_response["experience_level"],
            education=ai_response["education"]
        )
        analysis = await self.analysis_repo.save_analysis(
            analysis
        )
        await self.skill_service.save_skills(
            analysis.id,
            ai_response["skills"]
        )
        return analysis