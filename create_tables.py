# создать/удалить таблицы в бд, можно добавить moc данные

import asyncio
import json

import infrastructure.models  # noqa: F401
from infrastructure.db.base import Base
from infrastructure.db.session import async_engine, AsyncSessionLocal
from infrastructure.models import BookORM, AuthorORM


async def async_create_table(drop_table: bool):
    async with async_engine.begin() as conn:
        if drop_table:
            await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


def insert_data():
    async def async_insert_data(authors: list[dict], books: list[dict]):
        async with AsyncSessionLocal() as session:
            for author in authors:
                session.add(AuthorORM(**author))
            await session.commit()

            for book in books:
                session.add(BookORM(**book))
            await session.commit()

    def open_authors():
        with open('moc_data/authors.json', 'r') as f:
            return json.load(f)

    def open_books():
        with open('moc_data/books.json', 'r') as f:
            return json.load(f)

    asyncio.run(async_insert_data(
        authors=open_authors(),
        books=open_books())
    )


if __name__ == "__main__":
    is_drop_table = True if input("Отформатировать таблицы ( y/n ): ") == "y" else False
    asyncio.run(async_create_table(drop_table=is_drop_table))

    if is_drop_table:
        is_insert_data = True if input("Заполнить таблицы moc данными ( y/n ): ") == "y" else False

        if is_insert_data:
            insert_data()
            print('Данные добавлены')
