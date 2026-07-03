from src.repository.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, session):
        self.dashboard_repo = DashboardRepository(session)

    async def get_dashboard(self, user_id: int):
        return await self.dashboard_repo.get_all_resume(user_id)

    async def get_resume_analysis(self, resume_id: int):
        return await self.dashboard_repo.get_resume(resume_id)