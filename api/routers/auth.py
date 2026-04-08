from fastapi import APIRouter
from fastapi.responses import RedirectResponse, Response

from api.dependencies.auth_dependencies import GoogleUserData
from api.schemas.auth_schemas import GoogleUserSchema
from api.utils.auth.auth import google_oauth_redirect_uri

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.get("/google", summary="Редирект на Google OAuth (не для Swagger UI)")
async def login_google() -> Response:
    """
    Запускает OAuth 2.0 flow: делает редирект пользователя на страницу входа Google.

    Открывать напрямую в браузере:
    <http://localhost:8000/api/v1/auth/google>

    Требуется настроенный OAuth клиент в console.cloud.google.com/
    (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI).

    После успешного входа Google перенаправит пользователя на REDIRECT_URI
    с параметром `code`.
    """
    uri = google_oauth_redirect_uri()
    return RedirectResponse(url=uri, status_code=302)


@router.get("/google/callback")
async def google_callback(payload: GoogleUserData) -> GoogleUserSchema:
    """
    Callback-эндпоинт: в зависимости "GoogleUserData" который принимает `code` от Google
    и обменивает его на токены.

    Отправляет запрос в API Google, получает:
    - access_token
    - refresh_token
    - id_token (содержит данные пользователя)

    `code` одноразовый — повторно использовать нельзя.

    В параметр "body_response" возвращаются токены Google и id_token, id_token(Open id connect)
    декодируем и получаем payload его нам и возвращает зависимость GoogleUserData. В реальном
    приложении здесь создаётся/находится пользователь и выдаётся собственный JWT.
    """
    required_user_data = GoogleUserSchema(**payload)
    return required_user_data
