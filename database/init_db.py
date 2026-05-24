"""
Инициализация и управление базой данных
"""
import logging

logger = logging.getLogger(__name__)


async def create_tables():
    """Создать все таблицы"""
    from database.session import engine
    from database.models import Base
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ Таблицы созданы/обновлены")
