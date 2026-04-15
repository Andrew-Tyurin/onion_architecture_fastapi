import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException
from jwt.exceptions import InvalidTokenError

load_dotenv()


class CustomJWT:
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 5
    ALGORITHM: str = "HS256"

    @property
    def raise_token_exception(self) -> HTTPException:
        return HTTPException(
            status_code=401,
            detail="access-token протух или не действительный",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def encode_access_token(self, user_id: int) -> str:
        """Если user_id == 0 предполагается, что это админ"""
        user = f"user_{user_id}"
        expires_delta = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        issued_at = datetime.now(timezone.utc)
        expire = issued_at + expires_delta
        data = {"sub": user, "exp": expire, "iat": issued_at}
        return jwt.encode(data, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def decode_access_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            sub = payload.get("sub")
            if sub is None:
                raise self.raise_token_exception
        except InvalidTokenError:
            raise self.raise_token_exception

        return sub


SingleTonCustomJWT = CustomJWT()
