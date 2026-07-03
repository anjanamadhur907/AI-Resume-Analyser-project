from sqlalchemy import select

from src.model.resume import Resume

class ResumeRepository:

    def __init__(self, session):
        self.session = session

    async def save_resume(self, resume: Resume):
        self.session.add(resume)
        await self.session.flush()
        await self.session.refresh(resume)
        return resume

    #this will save extracted text
    async def update_resume(self, resume: Resume):
        self.session.add(resume)
        await self.session.flush()
        await self.session.refresh(resume)
        return resume

    async def find_by_id(self, resume_id: int):
        stmt = select(Resume).where(
            Resume.id == resume_id
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def delete_resume(self, resume: Resume):
        await self.session.delete(resume)

        await self.session.flush()