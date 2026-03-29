from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Author:
    name: str
    id: int | None = None


@dataclass
class Book:
    title: str
    price: Decimal
    quantity: int
    author: Author
    id: int | None = None
