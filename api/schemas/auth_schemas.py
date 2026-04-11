from pydantic import BaseModel, EmailStr


class GoogleOAuthParseSchema(BaseModel):
    name: str
    email: EmailStr
    sub: str


class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr


class GoogleOAuthSchema(BaseModel):
    id: int
    provider: str
    provider_user_id: str
    user: UserSchema


class AuthorizedGoogleOAuthSchema(BaseModel):
    message: str
    token: str
    google_oauth: GoogleOAuthSchema
