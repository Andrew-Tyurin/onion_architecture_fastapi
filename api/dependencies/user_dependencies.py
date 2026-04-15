from typing import Annotated

from fastapi import Depends, HTTPException, Path

from api.dependencies.base_session import SessionDep
from api.dependencies.jwt_dependencies import SubAccessToken
from applications.services.user_service import UserService, OAuthAccountsService
from infrastructure.repositories.user_repository_sa import SqlAlchemyUserRepository, SqlAlchemyOAuthAccountsRepository

Int = Annotated[int, Path(ge=1)]


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


async def get_sub_token(sub: Annotated[str, SubAccessToken]) -> None:
    if sub != "user_0":
        raise HTTPException(status_code=400, detail='Не достаточно прав')


SubAdminToken = Depends(get_sub_token)
