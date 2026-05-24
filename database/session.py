from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """Получить асинхронную сессию БД"""
    async with async_session() as session:
        yield session


async def init_db():
    """Инициализировать базу данных"""
    async with engine.begin() as conn:
        from database.models import Base
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ База данных инициализирована")
