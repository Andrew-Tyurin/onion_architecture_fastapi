from pydantic import BaseModel, Field, ConfigDict


class UserBaseSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=14, le=120)

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserBaseSchema):
    pass


class UserReadSchema(UserBaseSchema):
    id: int
