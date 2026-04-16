import os

from dotenv import load_dotenv
from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

database_url = os.getenv("DATABASE_URL")
name_dbms = os.getenv("NAME_DBMS", default="sqlite")

if name_dbms == "sqlite":
    engine = create_async_engine(
        database_url,
    )

    async_engine = create_async_engine(
        database_url,
        echo=True,
        connect_args={"check_same_thread": False},
    )


    @event.listens_for(async_engine.sync_engine, "connect")
    def enable_sqlite_fk(dbapi_connection, connection_record):
        """
        В SQLite внешние ключи по умолчанию выключены. Нужно включить:
        PRAGMA foreign_keys = ON, В SQLAlchemy обычно делают, как в этой функции
        """
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


elif name_dbms == "postgresql":
    engine = create_async_engine(
        database_url,
    )

    async_engine = create_async_engine(
        database_url,
        echo=True,
        pool_size=4,
        max_overflow=2,
    )

else:
    raise Exception("Корректно укажите в .env NAME_DBMS")

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)
