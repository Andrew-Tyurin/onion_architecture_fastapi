import asyncio

import pytest
from fastapi.testclient import TestClient

from api.utils.jw_token import SingleTonCustomJWT
from infrastructure.db.base import Base
from infrastructure.db.session import async_engine, AsyncSessionLocal, database_url
from infrastructure.models import BookORM, AuthorORM
from main import app
from tests.integration_tests.data.authors import add_authors
from tests.integration_tests.data.books import add_books


@pytest.fixture(scope="session", autouse=True)
def setting_test_db():
    """
    При запуске pytest основная DB подменяется, на тестовую DB указанную в .test.env
    В этом помогает pytest-dotenv, а в pytest.ini нужно указать какой именно файл .env
    использовать при pytest на текущий момент это .test.env.
    "assert 'test_db.db' in database_url" выдаст исключение если не использовать 'test_db.db'
    указанная в test.env, после чего форматируем тест-DB и создаём таблиц заново и заполняем
    данными. ВАЖНО тесты корректно работают при запуске всех тестов сразу т.к на момент
    выполнения всех тестов используется одна DB, а запуск конкретных тестов может дать
    непредсказуемый результат.
    """
    assert 'test_db.db' in database_url

    async def operations_on_db() -> None:
        async def async_create_table() -> None:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

        async def async_drop_table() -> None:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

        async def async_insert_data() -> None:
            async with AsyncSessionLocal() as session:
                for author in add_authors:
                    session.add(AuthorORM(**author))
                await session.commit()

                for book in add_books:
                    session.add(BookORM(**book))
                await session.commit()

        async_engine.echo = False
        await async_drop_table()
        await async_create_table()
        await async_insert_data()

    asyncio.run(operations_on_db())


@pytest.fixture(name='client', scope="session")
def client_fixture():
    access_token = SingleTonCustomJWT.encode_access_token(user_id=1)
    client = TestClient(app)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client
