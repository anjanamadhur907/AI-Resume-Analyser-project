import json

from google import genai
from google.genai import types

from src.config.config import settings
from src.schemas.ai_response import AIResponse


class AIService:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    async def analyze_resume(self, resume_text: str) -> AIResponse:

        prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the resume below.

Return ONLY valid JSON.

Do not write markdown.

Do not explain anything.

Return this exact JSON structure:

{{
"overall_score":90,
"ats_score":88,
"summary":"",
"strengths":[],
"weaknesses":[],
"recommendations":[],
"experience_level":"",
"education":"",
"skills":[]
}}

Resume:

{resume_text}
"""

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )

        data = json.loads(response.text)

        return AIResponse.model_validate(data)