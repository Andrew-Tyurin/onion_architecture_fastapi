from fastapi import APIRouter
from fastapi.responses import RedirectResponse, Response

from api.dependencies.auth_dependencies import GoogleUserData
from api.schemas.auth_schemas import AuthorizedGoogleOAuthSchema
from api.utils.auth.auth import google_oauth_redirect_uri
from api.utils.auth.auth import to_domain_oauth_google
from api.utils.jw_token import SingleTonCustomJWT
from applications.services.user_service import OAuthAccountsService
from infrastructure.db.session import AsyncSessionLocal
from infrastructure.repositories.user_repository_sa import SqlAlchemyOAuthAccountsRepository

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.get("/google", summary=f"Редирект на Google OAuth (не для Swagger UI)")
async def login_google() -> Response:
    """
    Запускает OAuth 2.0 flow: делает редирект пользователя на страницу входа Google.

    Открывать напрямую в браузере: <http://localhost:8000/api/v1/auth/google>

    Требуется настроенный OAuth клиент в console.cloud.google.com/
    (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI).

    После успешного входа Google перенаправит пользователя на REDIRECT_URI
    с параметром `code`.

    Так-же создаём CSRF токен и даём его google state=csrf, а тот должен будет вернуть его в REDIRECT_URI в state.
    """
    uri = google_oauth_redirect_uri()
    return RedirectResponse(url=uri, status_code=302)


@router.get("/google/callback")
async def google_callback(payload: GoogleUserData) -> AuthorizedGoogleOAuthSchema:
    """
    Это и есть REDIRECT_URI для google. Google аутентифицировал пользователя если валидный code.
    Наше приложение добавляет пользователя в DB и авторизовывает его выдавая свой access token для раздел books.

    Использовать этот endpoint напрямую нежелательно, сюда нас редиректит google
    """
    google_user = to_domain_oauth_google(payload)
    async with AsyncSessionLocal() as session:
        rep = SqlAlchemyOAuthAccountsRepository(session)
        service = OAuthAccountsService(rep)
        valid_google_user = await service.create_or_update_oauth_account(google_user)

    user_id = google_user.id
    access_token = SingleTonCustomJWT.encode_access_token(user_id)
    result = {
        "message": "Успешная авторизация через google",
        "access_token": access_token,
        "google_oauth": valid_google_user
    }
    return result
