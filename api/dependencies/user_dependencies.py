from typing import Annotated

from fastapi import Depends

from api.dependencies.base_session import SessionDep
from applications.services.user_service import UserService
from infrastructure.repositories.user_repository_sa import SqlAlchemyUserRepository


async def get_service_user(session: SessionDep) -> UserService:
    repo = SqlAlchemyUserRepository(session)
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_service_user)]
