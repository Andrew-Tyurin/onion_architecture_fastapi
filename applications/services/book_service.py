from applications.repositories.book_repository import AbstractAuthorRepository, AbstractBookRepository
from domain.dto.book import CreateBookDto, BookFilterDto, MoreAboutAuthorDto
from domain.entities.book import Book, Author


class AuthorService:
    def __init__(self, repo: AbstractAuthorRepository):
        self._repo = repo

    async def create_author(self, name: str) -> Author:
        author = Author(name=name)
        return await self._repo.add(author)

    async def get_authors(self) -> list[Author]:
        return await self._repo.get_all()

    async def remove_author(self, author_id: int) -> None:
        await self._repo.delete(author_id)


class BookService:
    def __init__(self, repo: AbstractBookRepository):
        self._repo = repo

    async def create_book(self, book: CreateBookDto) -> Book:
        return await self._repo.add(book)

    async def get_book(self, book_id: int) -> Book:
        return await self._repo.get_one(book_id)

    async def get_books(self, filters: BookFilterDto) -> list[Book]:
        return await self._repo.get_list(filters)

    async def get_authors_info(self, sort: str) -> list[MoreAboutAuthorDto]:
        return await self._repo.get_group(sort)

    async def remove_book(self, book_id: int) -> None:
        await self._repo.delete(book_id)
