import urllib.parse as urlparse

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from api.dependencies.auth_dependencies import QueryGoogle
from api.utils.auth.auth import verify_google_id_token
from api.utils.auth.settings import Settings

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.get("/google", summary="Редирект на Google OAuth (не для Swagger UI)")
async def login_google():
    """
    Запускает OAuth 2.0 flow: делает редирект пользователя на страницу входа Google.

    Открывать напрямую в браузере:
    <http://localhost:8000/api/v1/auth/google>

    Требуется настроенный OAuth клиент в console.cloud.google.com/
    (CLIENT_ID, CLIENT_SECRET, REDIRECT_URI).

    После успешного входа Google перенаправит пользователя на REDIRECT_URI
    с параметром `code`.
    """
    params = {
        "client_id": Settings.GOOGLE_CLIENT_ID,
        "redirect_uri": Settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    url_encode = urlparse.urlencode(params)
    url = f"https://accounts.google.com/o/oauth2/v2/auth?{url_encode}"
    return RedirectResponse(url=url, status_code=302)


@router.get("/google/callback")
async def google_callback(objects_dict: QueryGoogle):
    """
    Callback-эндпоинт: в зависимости "query_google" который принимает `code` от Google
    и обменивает его на токены.

    Отправляет запрос в API Google, получает:
    - access_token
    - refresh_token
    - id_token (содержит данные пользователя)

    `code` одноразовый — повторно использовать нельзя.

    В параметр "body_response" возвращаются токены Google и id_token,
    id_token декодируем в "verify_google_id_token" и получаем payload.
    В реальном приложении здесь создаётся/находится пользователь и
    выдаётся собственный JWT.
    """
    body_response = objects_dict["body_response"]
    session = objects_dict["session"]
    id_token = body_response.get("id_token")
    id_token_payload = await verify_google_id_token(id_token, session)

    result = {
        "access_token": body_response.get("access_token"),
        "refresh_token": body_response.get("refresh_token"),
        "token_type": body_response.get("token_type"),
        "id_token_payload": id_token_payload,
    }
    return result
