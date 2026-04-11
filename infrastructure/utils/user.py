from domain.entities.user import User, OAuthAccounts
from infrastructure.models import UserORM, OAuthAccountsORM


def to_orm_user(user: User) -> UserORM:
    """Data Mapper"""
    return UserORM(name=user.name, email=user.email)


def to_domain_user(orm: UserORM) -> User:
    """Data Mapper"""
    return User(id=orm.id, name=orm.name, email=orm.email)


def to_orm_oauth_account(oauth_account: OAuthAccounts, user: UserORM) -> OAuthAccountsORM:
    """Data Mapper"""
    return OAuthAccountsORM(
        provider=oauth_account.provider,
        provider_user_id=oauth_account.provider_user_id,
        user=user
    )


def to_domain_oauth_account(oauth_account: OAuthAccountsORM) -> OAuthAccounts:
    """Data Mapper"""
    return OAuthAccounts(
        id=oauth_account.id,
        provider=oauth_account.provider,
        provider_user_id=oauth_account.provider_user_id,
        user=to_domain_user(oauth_account.user)
    )
