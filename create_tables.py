# создать/удалить таблицы в бд, можно добавить moc данные

import asyncio
import json

import infrastructure.models  # noqa: F401
from infrastructure.db.base import Base
from infrastructure.db.session import async_engine, AsyncSessionLocal
from infrastructure.models import BookORM, AuthorORM


async def async_create_table(drop_table: bool, insert_data: bool) -> None:
    async with async_engine.begin() as conn:
        if drop_table:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_authors():
        with open('moc_data/authors.json', 'r') as f:
            return json.load(f)

    def open_books():
        with open('moc_data/books.json', 'r') as f:
            return json.load(f)

    if insert_data:
        authors = open_authors()
        books = open_books()

        async with AsyncSessionLocal() as session:
            for author in authors:
                session.add(AuthorORM(**author))
            await session.commit()

            for book in books:
                session.add(BookORM(**book))
            await session.commit()


if __name__ == "__main__":
    is_drop_table = True if input("Отформатировать таблицы ( y/n ): ") == "y" else False
    is_insert_data = True if input("Заполнить таблицы moc данными ( y/n ): ") == "y" else False
    asyncio.run(async_create_table(drop_table=is_drop_table, insert_data=is_insert_data))
