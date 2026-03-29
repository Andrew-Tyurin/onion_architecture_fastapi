from dataclasses import dataclass
from decimal import Decimal

from constants.book_constants import BOOK_OFFSET, BOOK_LIMIT


@dataclass
class BookFilterDto:
    offset: int = BOOK_OFFSET
    limit: int = BOOK_LIMIT
    author_name: str | None = None
    book_title: str | None = None
    book_min_price: Decimal | None = None
    book_max_price: Decimal | None = None
    in_descending_order_price: bool | None = None


@dataclass
class CreateBookDto:
    title: str
    price: Decimal
    quantity: int
    author_id: int


@dataclass
class MoreAboutAuthorDto:
    id: int
    name: str
    avg_price: int | None
    quantity_books: int
