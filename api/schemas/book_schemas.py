from decimal import Decimal

from pydantic import BaseModel, Field, field_validator, ConfigDict

from api.utils.book import empty_string, invalid_string, round_decimal
from constants.book_constants import (
    AUTHOR_NAME_LENGTH,
    BOOK_TITLE_LENGTH,
    BOOK_QUANTITY_MIN,
    BOOK_PRICE_MIN,
    BOOK_PRICE_MAX,
    BOOK_OFFSET,
    BOOK_LIMIT,
)


####### Author #######

class BaseAuthorSchema(BaseModel):
    name: str = Field(min_length=1, max_length=AUTHOR_NAME_LENGTH)

    model_config = ConfigDict(from_attributes=True)


    @field_validator('name')
    @classmethod
    def validate_name(cls, value, info) -> str:
        field_name = info.field_name
        value = value.strip()

        if not value:
            raise ValueError(empty_string(field_name))

        if not value.isalpha():
            raise ValueError(invalid_string(field_name, value))

        return value.title()


class ReadAuthorSchema(BaseAuthorSchema):
    id: int = Field(ge=1)


class CreateAuthorSchema(BaseAuthorSchema):
    pass


####### Book #######

class BaseBookSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CreateBookSchema(BaseBookSchema):
    title: str = Field(min_length=1, max_length=BOOK_TITLE_LENGTH)
    price: Decimal = Field(ge=BOOK_PRICE_MIN, le=BOOK_PRICE_MAX, default=0.01)
    quantity: int = Field(ge=BOOK_QUANTITY_MIN, default=1)
    author_id: int = Field(ge=1)

    @field_validator("title", "price")
    @classmethod
    def validate_fields(cls, value, info):
        field_name = info.field_name

        if field_name == 'price':
            value = round_decimal(value)

        elif field_name == 'title':
            value = value.strip()
            if not value:
                raise ValueError(empty_string(field_name))

        return value


class ReadBookSchema(BaseBookSchema):
    id: int
    title: str
    price: Decimal = Field(json_schema_extra={"examples": [0.01]})
    quantity: int
    author: ReadAuthorSchema


class ReadMoreAboutAuthorsSchema(BaseBookSchema):
    id: int
    name: str
    avg_price: int | None
    quantity_books: int


class BookFilterSchema(BaseBookSchema):
    offset: int = Field(ge=BOOK_OFFSET, default=BOOK_OFFSET)
    limit: int = Field(ge=1, le=BOOK_LIMIT, default=BOOK_LIMIT)
    author_name: str | None = Field(min_length=1, max_length=AUTHOR_NAME_LENGTH, default=None)
    book_title: str | None = Field(min_length=1, max_length=BOOK_TITLE_LENGTH, default=None)
    book_min_price: Decimal | None = Field(ge=BOOK_PRICE_MIN, le=int(BOOK_PRICE_MAX), default=None)
    book_max_price: Decimal | None = Field(ge=BOOK_PRICE_MIN, le=int(BOOK_PRICE_MAX), default=None)
    in_descending_order_price: bool | None = None

    @field_validator(
        "author_name",
        "book_title",
        "book_min_price",
        "book_max_price",
    )
    @classmethod
    def validate_fields(cls, value, info):
        field_name = info.field_name

        if field_name in ("book_min_price", "book_max_price",):
            value = round_decimal(value)

        if field_name in ("author_name", "book_title",):
            value = value.strip()
            if not value:
                raise ValueError(empty_string(field_name))

        if field_name == 'author_name':

            if not value.isalpha():
                raise ValueError(invalid_string(field_name, value))

            value = value.title()

        return value
