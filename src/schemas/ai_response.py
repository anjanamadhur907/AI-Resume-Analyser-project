from pydantic import BaseModel


class AIResponse(BaseModel):
    overall_score: float
    ats_score: float
    summary: str
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]
    experience_level: str
    education: str
    skills: list[str]