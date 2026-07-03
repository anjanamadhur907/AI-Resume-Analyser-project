import os
import shutil
import uuid

from fastapi import UploadFile

from src.exception.resource_not_found_exception import ResourceNotFoundException
from src.model.resume import Resume
from src.repository.resume_repository import ResumeRepository
from src.service.pdf_service import PDFService
from src.service.ai_service import AIService
from src.service.analysis_service import AnalysisService

class ResumeService:

    def __init__(self, session):
        self.resume_repo = ResumeRepository(session)
        self.ai_service = AIService()
        self.analysis_service = AnalysisService(session)

    async def upload_resume(self, file: UploadFile, user_id: int):

        # Validate extension
        extension = os.path.splitext(file.filename)[1].lower()

        if extension != ".pdf":
            raise Exception("Only PDF files are allowed.")

        # Create uploads folder if it doesn't exist
        upload_folder = "src/uploads"
        os.makedirs(upload_folder, exist_ok=True)

        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{extension}"

        file_location = os.path.join(upload_folder, unique_filename)

        # Save file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Create Resume object
        resume = Resume(
            user_id=user_id,
            file_name=file.filename,
            stored_file_name=unique_filename,
            file_path=file_location,
            resume_text=None
        )
        resume = await self.resume_repo.save_resume(resume)
        resume_text = PDFService.extract_text(file_location)
        resume.resume_text = resume_text
        resume = await self.resume_repo.update_resume(resume)
        analysis = await self.ai_service.analyze_resume(
            resume.resume_text
        )
        await self.analysis_service.save_analysis(
            resume.id,
            analysis.model_dump()
        )
        return resume

    async def delete_resume(self, resume_id: int):

        resume = await self.resume_repo.find_by_id(
            resume_id
        )

        if not resume:
            raise ResourceNotFoundException(
                "Resume not found"
            )

        await self.resume_repo.delete_resume(
            resume
        )
