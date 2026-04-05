import jwt
from fastapi import HTTPException
from jwt.algorithms import RSAAlgorithm, AllowedRSAKeys
from jwt.exceptions import InvalidTokenError

from api.dependencies.auth_dependencies import AiohttpSession
from api.utils.auth.settings import Settings

async def get_public_key(id_token: str, session: AiohttpSession) -> AllowedRSAKeys:
    """
    PyJWT не умеет работать напрямую с JWK(dict)
    Он ожидает: PEM-формат ключа(строка) Нужно:
    преобразовать JWK → в PEM ключ, используя RSAAlgorithm
    get_unverified_header - достать служебную информацию (alg, kid),
    чтобы понять, как проверять токен.
    """

    headers = jwt.get_unverified_header(id_token)
    kid = headers['kid']

    url_certs = "https://www.googleapis.com/oauth2/v3/certs"
    async with session.get(url=url_certs) as response:
        certs = await response.json()  # получаем публичные ключи

    for key in certs["keys"]:
        if key["kid"] == kid:
            return RSAAlgorithm.from_jwk(key)

    raise HTTPException(status_code=400, detail='Публичный ключ для jwt от google не найден')


async def verify_google_id_token(id_token: str, session: AiohttpSession) -> dict:
    key = await get_public_key(id_token, session)
    try:
        id_token_payload = jwt.decode(
            id_token,
            key,
            algorithms=["RS256"],
            audience=Settings.GOOGLE_CLIENT_ID,
            issuer="https://accounts.google.com",
        )
    except InvalidTokenError as e:
        raise HTTPException(status_code=400, detail=f'не удалось прочитать jwt, InvalidTokenError = {e}')

    return id_token_payload
