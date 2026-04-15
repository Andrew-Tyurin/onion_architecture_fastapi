from pydantic import BaseModel, EmailStr, Field


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
    access_token: str
    google_oauth: GoogleOAuthSchema


class AdminTokenSchema(BaseModel):
    access_token: str


class AdminPasswordSchema(BaseModel):
    password: str = Field(min_length=3, max_length=120)
