from decimal import Decimal

from sqlalchemy import DECIMAL, ForeignKey, String, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.base import Base
from constants.book_constants import (
    AUTHOR_NAME_LENGTH,
    BOOK_TITLE_LENGTH,
    BOOK_QUANTITY_MIN,
    BOOK_PRICE_MIN,
)

class AuthorORM(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(AUTHOR_NAME_LENGTH), index=True, nullable=False)
    books: Mapped[list["BookORM"]] = relationship(back_populates="author", passive_deletes=True)


class BookORM(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(BOOK_TITLE_LENGTH), nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False,
    )
    author: Mapped[AuthorORM] = relationship(back_populates='books')
    __table_args__ = (
        CheckConstraint(f"quantity >= {BOOK_QUANTITY_MIN}", name="book_quantity"),
        CheckConstraint(f"price >= {BOOK_PRICE_MIN}", name="book_price"),
    )
