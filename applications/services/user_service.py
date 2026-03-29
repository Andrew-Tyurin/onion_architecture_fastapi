from applications.repositories.user_repository import AbstractUserRepository
from domain.entities.user import User


class UserService:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def create_user(self, name: str, age: int) -> User:
        user = User(name=name, age=age)
        return await self.repo.add(user)

    async def get_user(self, user_id: int) -> User:
        return await self.repo.get_one(user_id)

    async def get_users(self) -> list[User]:
        return await self.repo.get_all()
