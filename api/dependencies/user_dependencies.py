from typing import Annotated

from fastapi import Depends

from api.dependencies.base_session import SessionDep
from applications.services.user_service import UserService, OAuthAccountsService
from infrastructure.repositories.user_repository_sa import SqlAlchemyUserRepository, SqlAlchemyOAuthAccountsRepository


async def get_service_user(session: SessionDep) -> UserService:
    repo = SqlAlchemyUserRepository(session)
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_service_user)]


def build_oauth_service(session) -> OAuthAccountsService:
    repo = SqlAlchemyOAuthAccountsRepository(session)
    return OAuthAccountsService(repo)


async def get_service_oauth_accounts(session: SessionDep) -> OAuthAccountsService:
    return build_oauth_service(session)


OAuthAccountsServiceDep = Annotated[OAuthAccountsService, Depends(get_service_oauth_accounts)]
