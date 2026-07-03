from src.exception.resource_not_found_exception import ResourceNotFoundException
from src.model import User
from src.repository.user_repository import UserRepository
from src.utils.password import verify_password


class UserService:
    def __init__(self, session):
        self.user_repo = UserRepository(session)

    async def create_user(self, user:User):
        return await self.user_repo.create_user(user)

    async def authentication(self, user:User):
        db_user = await self.user_repo.find_by_email(user.email)
        if not db_user:
            raise ResourceNotFoundException("Resource not found")
        status = verify_password(db_user.password, user.password)
        return status

    async def find_by_email(self, email: str):
        return await self.user_repo.find_by_email(email)