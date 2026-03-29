from abc import ABC, abstractmethod

from domain.dto.book import CreateBookDto, BookFilterDto, MoreAboutAuthorDto
from domain.entities.book import Book, Author


class AbstractAuthorRepository(ABC):
    @abstractmethod
    async def get_all(self) -> list[Author]: ...

    @abstractmethod
    async def add(self, author: Author) -> Author: ...

    @abstractmethod
    async def delete(self, author_id: int) -> None: ...


class AbstractBookRepository(ABC):
    @abstractmethod
    async def get_one(self, book_id: int) -> Book: ...

    @abstractmethod
    async def get_list(self, filters: BookFilterDto) -> list[Book]: ...

    @abstractmethod
    async def get_group(self, sort: str | None) -> list[MoreAboutAuthorDto]: ...

    @abstractmethod
    async def add(self, book: CreateBookDto) -> Book: ...

    @abstractmethod
    async def delete(self, book_id: int) -> None: ...
