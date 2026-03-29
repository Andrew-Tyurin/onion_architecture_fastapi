from fastapi import APIRouter, Path

from api.dependencies.user_dependencies import UserServiceDep
from api.schemas.user_schemas import UserCreateSchema, UserReadSchema
from api.utils.user import user_get_attribute

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserReadSchema)
async def get_user(service: UserServiceDep, user_id: int = Path(ge=1)):
    user = await service.get_user(user_id)
    return user


@router.get("", response_model=list[UserReadSchema])
async def get_users(service: UserServiceDep):
    user_list = await service.get_users()
    return user_list


@router.post("", response_model=UserReadSchema, status_code=201)
async def create_user(data: UserCreateSchema, service: UserServiceDep):
    name, age = user_get_attribute(data)
    user = await service.create_user(name, age)
    return user
