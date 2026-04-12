from typing import Annotated

from fastapi import Depends, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.dependencies.base_session import SessionDep
from api.utils.auth.settings_google import SettingsGoogleOAuth
from api.utils.jw_token import SingleTonCustomJWT
from applications.services.book_service import BookService, AuthorService
from infrastructure.repositories.book_repository_sa import SqlAlchemyAuthorRepository, SqlAlchemyBookRepository


async def get_service_author(session: SessionDep) -> AuthorService:
    repo = SqlAlchemyAuthorRepository(session)
    return AuthorService(repo)


async def get_service_book(session: SessionDep) -> BookService:
    repo = SqlAlchemyBookRepository(session)
    return BookService(repo)


security = HTTPBearer(description=f"Получить токен: <{SettingsGoogleOAuth.GOOGLE_OAUTH}>")


async def custom_access_token(authorization: HTTPAuthorizationCredentials = Depends(security)):
    token = authorization.credentials
    SingleTonCustomJWT.decode_access_token(token)


AuthorServiceDep = Annotated[AuthorService, Depends(get_service_author)]
BookServiceDep = Annotated[BookService, Depends(get_service_book)]
Int = Annotated[int, Path(ge=1)]
