from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=14, le=120)

    class Config:
        from_attributes = True


class UserCreateSchema(UserBaseSchema):
    pass


class UserReadSchema(UserBaseSchema):
    id: int
