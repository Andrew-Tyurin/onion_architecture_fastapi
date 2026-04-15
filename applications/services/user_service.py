from applications.repositories.user_repository import AbstractUserRepository, AbstractOAuthAccountsRepository
from domain.entities.user import User, OAuthAccounts


class UserService:
    def __init__(self, repo: AbstractUserRepository):
        self.repo = repo

    async def create_user(self, name: str, email: str) -> User:
        user = User(name=name, email=email)
        return await self.repo.add(user)

    async def get_user(self, user_id: int) -> User:
        return await self.repo.get_one(user_id)

    async def remove_user(self, user_id: int) -> None:
        await self.repo.delete(user_id)

    async def get_users(self) -> list[User]:
        return await self.repo.get_all()


class OAuthAccountsService:
    def __init__(self, repo: AbstractOAuthAccountsRepository):
        self.repo = repo

    async def create_or_update_oauth_account(self, user: OAuthAccounts) -> OAuthAccounts:
        return await self.repo.add_or_update(user)

    async def get_oauth_account(self, user_id: int) -> OAuthAccounts:
        return await self.repo.get_one(user_id)

    async def get_oauth_accounts(self) -> list[OAuthAccounts]:
        return await self.repo.get_all()
