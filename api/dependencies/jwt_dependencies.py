from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.utils.auth.settings_google import SettingsGoogleOAuth
from api.utils.jw_token import SingleTonCustomJWT

security = HTTPBearer(description=f"Получить токен: <{SettingsGoogleOAuth.GOOGLE_OAUTH}>")


async def custom_access_token(authorization: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = authorization.credentials
    return SingleTonCustomJWT.decode_access_token(token)


SubAccessToken = Depends(custom_access_token)
