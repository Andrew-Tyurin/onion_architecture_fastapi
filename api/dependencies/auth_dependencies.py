from typing import Annotated

import aiohttp
import jwt
from fastapi import HTTPException, Query, Depends
from jwt.algorithms import RSAAlgorithm, AllowedRSAKeys
from jwt.exceptions import InvalidTokenError

from api.schemas.auth_schemas import GoogleOAuthParseSchema
from api.utils.auth.settings_google import SettingsGoogleOAuth


async def get_aiohttp_session() -> aiohttp.ClientSession:
    async with aiohttp.ClientSession() as sessions:
        yield sessions


AiohttpSession = Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)]


async def google_user_data(session: AiohttpSession, code: Annotated[str, Query()]) -> GoogleOAuthParseSchema:
    """
    Принимает `code` от Google и обменивает его на токены.

    Отправляет запрос в API Google, получает:
    - access_token
    - id_token (содержит данные пользователя)

    `code` одноразовый — повторно использовать нельзя.

    В параметр "body_response" возвращаются токены Google и id_token, id_token(Open id connect)
    декодируем, перед этим получив валидный публичный ключ для jwt.decode, получаем payload
    после этот payload парсится через pydentic.
    """
    def jwt_decode(id_token: str, key: AllowedRSAKeys) -> dict:
        try:
            payload = jwt.decode(
                id_token,
                key,
                algorithms=["RS256"],
                audience=SettingsGoogleOAuth.CLIENT_ID,
                issuer=SettingsGoogleOAuth.ACCOUNTS,
            )
        except InvalidTokenError as e:
            raise HTTPException(status_code=400, detail=f'не удалось прочитать jwt, InvalidTokenError = {e}')
        return payload

    async def get_public_key(id_token: str) -> AllowedRSAKeys:
        headers = jwt.get_unverified_header(id_token)

        async with session.get(url=SettingsGoogleOAuth.CERTS_PUBLIC_KEYS) as get_certs:
            certs = await get_certs.json()  # получаем публичные ключи

        for cert in certs["keys"]:
            if cert["kid"] == headers['kid']:  # нужен подходящий ключ
                return RSAAlgorithm.from_jwk(cert)
        raise HTTPException(status_code=400, detail='Публичный ключ для jwt от google не найден/не валидный')

    async def assemble_payload() -> dict:
        params = {
            "client_id": SettingsGoogleOAuth.CLIENT_ID,
            "client_secret": SettingsGoogleOAuth.CLIENT_SECRET,
            "redirect_uri": SettingsGoogleOAuth.REDIRECT_URI,
            "code": code,
            "grant_type": "authorization_code",
        }
        async with session.post(url=SettingsGoogleOAuth.GET_TOKENS, json=params) as get_body:
            body_response = await get_body.json()

        if 500 > get_body.status >= 400:
            raise HTTPException(status_code=400, detail=body_response)

        id_token = body_response.get("id_token")
        key = await get_public_key(id_token)
        return jwt_decode(id_token, key)

    result_payload = await assemble_payload()
    return GoogleOAuthParseSchema(**result_payload)


GoogleUserData = Annotated[GoogleOAuthParseSchema, Depends(google_user_data)]
