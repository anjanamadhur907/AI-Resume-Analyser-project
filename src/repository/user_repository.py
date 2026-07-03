from sqlalchemy import select

from src.model import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def create_user(self,user:User):
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def find_by_email(self,email:str):
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
