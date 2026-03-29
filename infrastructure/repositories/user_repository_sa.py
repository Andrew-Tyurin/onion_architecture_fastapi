from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from applications.repositories.user_repository import AbstractUserRepository
from domain.entities.user import User
from infrastructure.models import UserORM
from infrastructure.utils.user import to_domain_user, to_orm_user
from infrastructure.utils.base_utils import is_obj


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, user_id: int) -> User:
        orm_user = await self.session.get(UserORM, user_id)
        is_obj(orm_user, user_id)
        return to_domain_user(orm_user)

    async def get_all(self) -> list[User]:
        orm_users = await self.session.scalars(select(UserORM))
        return [to_domain_user(orm_user) for orm_user in orm_users.all()]

    async def add(self, user: User) -> User:
        orm_user = to_orm_user(user)
        self.session.add(orm_user)
        await self.session.commit()
        await self.session.refresh(orm_user)
        return to_domain_user(orm_user)
