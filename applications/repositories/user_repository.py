from abc import ABC, abstractmethod

from domain.entities.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def get_one(self, user_id: int) -> User: ...

    @abstractmethod
    async def get_all(self) -> list[User]: ...

    @abstractmethod
    async def add(self, user: User) -> User: ...
