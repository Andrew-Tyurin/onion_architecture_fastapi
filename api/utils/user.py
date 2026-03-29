from api.schemas.user_schemas import UserBaseSchema


def user_get_attribute(data: UserBaseSchema) -> tuple:
    attr_tuple = tuple(data.model_dump().values())
    return attr_tuple
