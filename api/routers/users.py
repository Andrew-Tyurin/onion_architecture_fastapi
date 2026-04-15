from fastapi import APIRouter, Path

from api.dependencies.user_dependencies import UserServiceDep, OAuthAccountsServiceDep, SubAdminToken, Int
from api.schemas.user_schemas import UserCreateSchema, UserReadSchema, OAuthAccountsReadSchema
from api.utils.user import user_get_attribute

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get("/{user_id}", response_model=UserReadSchema)
async def get_user(service: UserServiceDep, user_id: Int):
    user = await service.get_user(user_id)
    return user


@router.delete("/{user_id}", dependencies=[SubAdminToken])
async def delete_user(service: UserServiceDep, user_id: Int) -> dict:
    await service.remove_user(user_id)
    return {"deleted": f"объект {user_id=} удалён успешно"}


@router.get("", response_model=list[UserReadSchema])
async def get_users(service: UserServiceDep):
    user_list = await service.get_users()
    return user_list


@router.post("", response_model=UserReadSchema, status_code=201)
async def create_user(data: UserCreateSchema, service: UserServiceDep):
    name, age = user_get_attribute(data)
    user = await service.create_user(name, age)
    return user


@router.get("/oauth/all")
async def get_users_oauth(service: OAuthAccountsServiceDep) -> list[OAuthAccountsReadSchema]:
    users_oauth = await service.get_oauth_accounts()
    return users_oauth


@router.get("/oauth/{user_id}")
async def get_user_oauth(
        service: OAuthAccountsServiceDep,
        user_id: int = Path(ge=1)
) -> OAuthAccountsReadSchema:
    user_oauth = await service.get_oauth_account(user_id)
    return user_oauth
