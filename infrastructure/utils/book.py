from decimal import Decimal
from typing import Union

from sqlalchemy import func
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.elements import ColumnElement

from domain.dto.book import CreateBookDto, BookFilterDto, MoreAboutAuthorDto
from domain.entities.book import Author, Book
from infrastructure.models import AuthorORM, BookORM


def to_orm_author(author: Author) -> AuthorORM:
    """Data Mapper"""
    return AuthorORM(name=author.name)


def to_domain_author(author: AuthorORM) -> Author:
    """Data Mapper"""
    return Author(id=author.id, name=author.name)


def to_orm_book(book_dto: CreateBookDto, author: AuthorORM) -> BookORM:
    """Data Mapper"""
    return BookORM(
        title=book_dto.title,
        price=book_dto.price,
        quantity=book_dto.quantity,
        author=author
    )


def to_domain_book(book: BookORM) -> Book:
    """Data Mapper"""
    return Book(
        id=book.id,
        title=book.title,
        price=book.price,
        quantity=book.quantity,
        author=to_domain_author(book.author),
    )


def to_dto_more_about_author(obj: RowMapping) -> MoreAboutAuthorDto:
    """Data Mapper"""
    return MoreAboutAuthorDto(
        id=obj.id,
        name=obj.name,
        avg_price=obj.avg_price,
        quantity_books=obj.quantity_books,
    )


OneObj = Union[InstrumentedAttribute, ColumnElement]
ListObj = list[OneObj]


def valid_conditions(book_filter: BookFilterDto) -> tuple[ListObj, OneObj]:
    author_name: str = book_filter.author_name
    book_title: str = book_filter.book_title
    book_min_price: Decimal = book_filter.book_min_price
    book_max_price: Decimal = book_filter.book_max_price
    in_descending_order_price: bool | None = book_filter.in_descending_order_price

    conditions = []
    if author_name:
        conditions.append(AuthorORM.name.like(f"{author_name}%"))

    if book_title:
        conditions.append(BookORM.title.like(f"{book_title}%"))

    if book_min_price:
        conditions.append(BookORM.price >= book_min_price)

    if book_max_price:
        conditions.append(BookORM.price <= book_max_price)

    order_price = BookORM.id
    if in_descending_order_price == False:
        order_price = BookORM.price

    if in_descending_order_price:
        order_price = BookORM.price.desc()

    return conditions, order_price


def sort_by_grouped_field(sort: str) -> ColumnElement:
    if "avg-price" in sort:
        obj = func.avg(BookORM.price)

    elif "quantity-books" in sort:
        obj = func.count(BookORM.id)

    elif "id" in sort:
        obj = AuthorORM.id

    else:
        obj = AuthorORM.id

    if sort.find("-") == 0:
        obj = obj.desc()

    return obj
