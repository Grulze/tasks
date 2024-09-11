from asyncio import run
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

async_eng = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/taskdb', echo=False)

session = async_sessionmaker(async_eng, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class TaskDB(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[str]
    executor: Mapped[str] = mapped_column(default='Global', index=True)
    description: Mapped[str]
    time_limit: Mapped[int] = mapped_column(default=24)
    completed: Mapped[bool] = mapped_column(default=False)
    time_create: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


def __create_table():
    """
    Create all tables.
    """
    async def start():
        async with async_eng.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print('Tables was created.')

    run(start())
