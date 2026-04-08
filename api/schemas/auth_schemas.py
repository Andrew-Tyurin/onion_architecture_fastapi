from pydantic import BaseModel, EmailStr


class GoogleUserSchema(BaseModel):
    name: str
    email: EmailStr
    sub: str


class ReadGoogleUserSchema:
    id: int
    name: str
    email: EmailStr
    sub: str
