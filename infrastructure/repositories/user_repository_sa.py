from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from applications.repositories.user_repository import AbstractUserRepository, AbstractOAuthAccountsRepository
from domain.entities.user import User, OAuthAccounts
from infrastructure.models import UserORM, OAuthAccountsORM
from infrastructure.utils.base_utils import is_obj
from infrastructure.utils.user import to_domain_user, to_orm_user, to_orm_oauth_account, to_domain_oauth_account


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, user_id: int) -> User:
        orm_user = await self.session.get(UserORM, user_id)
        is_obj(orm_user, f"{user_id=}")
        return to_domain_user(orm_user)

    async def delete(self, user_id: int) -> None:
        orm_user = await self.session.get(UserORM, user_id)
        is_obj(orm_user, f"{user_id=}")
        await self.session.delete(orm_user)
        await self.session.commit()

    async def get_all(self) -> list[User]:
        orm_users = await self.session.scalars(select(UserORM))
        return [to_domain_user(orm_user) for orm_user in orm_users.all()]

    async def add(self, user: User) -> User:
        orm_user = to_orm_user(user)
        self.session.add(orm_user)
        await self.session.commit()
        await self.session.refresh(orm_user)
        return to_domain_user(orm_user)


class SqlAlchemyOAuthAccountsRepository(AbstractOAuthAccountsRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_one(self, user_id: int) -> OAuthAccounts:
        stm = await self._session.scalars(
            select(OAuthAccountsORM)
            .options(joinedload(OAuthAccountsORM.user))
            .where(OAuthAccountsORM.id == user_id)
        )
        orm_user = stm.one_or_none()
        is_obj(orm_user, f"{user_id=}")
        return to_domain_oauth_account(orm_user)

    async def get_all(self) -> list[OAuthAccounts]:
        stm = await self._session.scalars(
            select(OAuthAccountsORM)
            .options(joinedload(OAuthAccountsORM.user))
        )
        orm_users = stm.all()
        return [to_domain_oauth_account(orm_user) for orm_user in orm_users]

    async def add_or_update(self, user: OAuthAccounts) -> OAuthAccounts:
        existing = await self._session.scalars(
            select(OAuthAccountsORM)
            .join(OAuthAccountsORM.user)
            .options(joinedload(OAuthAccountsORM.user))
            .where(
                OAuthAccountsORM.provider == user.provider,
                OAuthAccountsORM.provider_user_id == user.provider_user_id,
            )
        )
        existing: OAuthAccountsORM | None = existing.one_or_none()
        if existing:
            existing.user.name = user.user.name
            existing.user.email = user.user.email
            orm_oauth_account = existing

        else:
            orm_user = to_orm_user(user.user)
            orm_oauth_account = to_orm_oauth_account(user, orm_user)
            self._session.add(orm_oauth_account)

        await self._session.commit()
        return to_domain_oauth_account(orm_oauth_account)
