from pydantic import BaseModel, Field, ConfigDict, EmailStr


####### User #######

class UserBaseSchema(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr = Field(max_length=120)

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserBaseSchema):
    pass


class UserReadSchema(UserBaseSchema):
    id: int


####### OAuthAccounts #######

class OAuthAccountsReadSchema(BaseModel):
    id: int
    provider: str
    provider_user_id: str
    user: UserReadSchema
