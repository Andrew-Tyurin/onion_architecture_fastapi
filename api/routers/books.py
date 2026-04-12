from typing import Annotated

from fastapi import APIRouter, Query, Depends

from api.dependencies.book_dependencies import AuthorServiceDep, BookServiceDep, Int, custom_access_token
from api.schemas.book_schemas import (
    CreateAuthorSchema,
    ReadAuthorSchema,
    ReadBookSchema,
    BookFilterSchema,
    ReadMoreAboutAuthorsSchema,
    CreateBookSchema
)
from api.utils.book import GroupFields
from domain.dto.book import BookFilterDto, CreateBookDto

router = APIRouter(
    prefix="/api/v1/books",
    tags=["Books"],
    dependencies=[Depends(custom_access_token)],
)


@router.get("/authors", response_model=list[ReadAuthorSchema])
async def get_authors(service: AuthorServiceDep) -> list[ReadAuthorSchema]:
    return await service.get_authors()


@router.post("/authors", response_model=ReadAuthorSchema, status_code=201)
async def create_author(author: CreateAuthorSchema, service: AuthorServiceDep) -> ReadAuthorSchema:
    return await service.create_author(name=author.name)


@router.delete("/authors/{author_id}")
async def remove_author(author_id: Int, service: AuthorServiceDep) -> dict:
    await service.remove_author(author_id)
    return {"deleted": f"объект {author_id=} удалён успешно"}


@router.get("", response_model=list[ReadBookSchema])
async def get_books(
        filters: Annotated[BookFilterSchema, Query()],
        service: BookServiceDep,
) -> list[ReadBookSchema]:
    filters_dict = filters.model_dump(exclude_unset=True)
    filters_dto = BookFilterDto(**filters_dict)
    return await service.get_books(filters_dto)


@router.get("/{book_id}", response_model=ReadBookSchema)
async def get_book(book_id: Int, service: BookServiceDep) -> ReadBookSchema:
    return await service.get_book(book_id)


@router.get("/more/authors", response_model=list[ReadMoreAboutAuthorsSchema])
async def get_authors_info(sort: GroupFields, service: BookServiceDep) -> list[ReadMoreAboutAuthorsSchema]:
    return await service.get_authors_info(sort)


@router.post("", response_model=ReadBookSchema, status_code=201)
async def create_book(book: CreateBookSchema, service: BookServiceDep) -> ReadBookSchema:
    book_dict = book.model_dump()
    book_dto = CreateBookDto(**book_dict)
    return await service.create_book(book_dto)


@router.delete("/{book_id}")
async def remove_book(book_id: Int, service: BookServiceDep) -> dict:
    await service.remove_book(book_id)
    return {"deleted": f"объект {book_id=} удалён успешно"}
