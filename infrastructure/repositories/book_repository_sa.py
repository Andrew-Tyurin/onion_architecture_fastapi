from sqlalchemy import select, Integer, cast, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from applications.repositories.book_repository import AbstractAuthorRepository, AbstractBookRepository
from domain.dto.book import CreateBookDto, BookFilterDto, MoreAboutAuthorDto
from domain.entities.book import Author, Book
from infrastructure.models.book_orm import AuthorORM, BookORM
from infrastructure.utils.base_utils import is_obj
from infrastructure.utils.book import (
    to_orm_book,
    to_orm_author,
    to_domain_book,
    to_domain_author,
    valid_conditions,
    sort_by_grouped_field,
    to_dto_more_about_author
)


class SqlAlchemyAuthorRepository(AbstractAuthorRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Author]:
        orm_authors = await self._session.scalars(select(AuthorORM).order_by(AuthorORM.id))
        return [to_domain_author(orm_author) for orm_author in orm_authors.all()]

    async def add(self, author: Author) -> Author:
        orm_author = to_orm_author(author)
        self._session.add(orm_author)
        await self._session.commit()
        return to_domain_author(orm_author)

    async def delete(self, author_id: int) -> None:
        orm_author = await self._session.get(AuthorORM, author_id)
        is_obj(orm_author, f"{author_id=}")
        await self._session.delete(orm_author)
        await self._session.commit()


class SqlAlchemyBookRepository(AbstractBookRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_one(self, book_id: int) -> Book:
        result = await self._session.scalars(
            select(BookORM)
            .options(joinedload(BookORM.author))
            .where(BookORM.id == book_id)
        )
        orm_book = result.one_or_none()
        is_obj(orm_book, f"{book_id=}")
        return to_domain_book(orm_book)

    async def get_list(self, filters: BookFilterDto) -> list[Book]:
        conditions, order_by = valid_conditions(filters)
        stm = (
            select(BookORM)
            .outerjoin(BookORM.author)
            .options(joinedload(BookORM.author))
            .order_by(order_by)
            .offset(filters.offset)
            .limit(filters.limit)
        )

        if conditions:
            stm = stm.where(*conditions)

        orm_books = await self._session.scalars(stm)
        return [to_domain_book(orm_book) for orm_book in orm_books.all()]

    async def get_group(self, sort: str) -> list[MoreAboutAuthorDto]:
        order_by = sort_by_grouped_field(sort)
        stm = (
            select(
                AuthorORM.id,
                AuthorORM.name,
                cast(func.avg(BookORM.price), Integer).label("avg_price"),
                func.count(BookORM.id).label("quantity_books"),
            )
            .outerjoin(AuthorORM.books)
            .group_by(AuthorORM.id, AuthorORM.name)
            .order_by(order_by)
        )
        core_authors = await self._session.execute(stm)
        return [to_dto_more_about_author(author) for author in core_authors.all()]

    async def add(self, dto_book: CreateBookDto) -> Book:
        orm_author = await self._session.get(AuthorORM, dto_book.author_id)
        is_obj(orm_author, f"author_id={dto_book.author_id}")
        orm_book = to_orm_book(dto_book, orm_author)
        self._session.add(orm_book)
        await self._session.commit()
        return to_domain_book(orm_book)

    async def delete(self, book_id: int) -> None:
        orm_book = await self._session.get(BookORM, book_id)
        is_obj(orm_book, f"{book_id=}")
        await self._session.delete(orm_book)
        await self._session.commit()
