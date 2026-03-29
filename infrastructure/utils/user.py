from domain.entities.user import User
from infrastructure.models import UserORM


def to_orm_user(user: User) -> UserORM:
    """Data Mapper"""
    return UserORM(name=user.name, age=user.age)


def to_domain_user(orm: UserORM) -> User:
    """Data Mapper"""
    return User(user_id=orm.id, name=orm.name, age=orm.age)
