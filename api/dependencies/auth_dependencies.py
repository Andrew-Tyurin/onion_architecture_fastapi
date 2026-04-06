from typing import Annotated

import aiohttp
from fastapi import HTTPException, Query, Depends

from api.utils.auth.settings_google import SettingsGoogleOAuth


async def get_aiohttp_session() -> aiohttp.ClientSession:
    async with aiohttp.ClientSession() as sessions:
        yield sessions


AiohttpSession = Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)]


async def query_google(
        session: AiohttpSession,
        code: Annotated[str, Query()],
) -> dict:
    params = {
        "client_id": SettingsGoogleOAuth.CLIENT_ID,
        "client_secret": SettingsGoogleOAuth.CLIENT_SECRET,
        "redirect_uri": SettingsGoogleOAuth.REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code",
    }
    url_token = SettingsGoogleOAuth.GET_TOKENS
    async with session.post(url=url_token, json=params) as response:
        body_response = await response.json()

    if 500 > response.status >= 400:
        raise HTTPException(status_code=400, detail=body_response)

    return {"body_response": body_response, "session": session}


QueryGoogle = Annotated[dict, Depends(query_google)]
