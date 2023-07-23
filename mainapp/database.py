from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config

async def start_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

engine = create_async_engine(config.SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)