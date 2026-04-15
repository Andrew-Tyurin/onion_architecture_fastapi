from abc import ABC, abstractmethod

from domain.entities.user import User, OAuthAccounts


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_one(self, user_id: int) -> User: ...

    @abstractmethod
    async def delete(self, user_id: int) -> None: ...

    @abstractmethod
    async def get_all(self) -> list[User]: ...

    @abstractmethod
    async def add(self, user: User) -> User: ...


class AbstractOAuthAccountsRepository(ABC):
    @abstractmethod
    async def get_one(self, user_id: int) -> OAuthAccounts: ...

    @abstractmethod
    async def get_all(self) -> list[OAuthAccounts]: ...

    @abstractmethod
    async def add_or_update(self, user: OAuthAccounts) -> OAuthAccounts: ...
