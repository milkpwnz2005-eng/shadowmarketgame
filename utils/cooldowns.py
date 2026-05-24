from datetime import datetime, timedelta
import redis.asyncio as redis
from config import REDIS_URL


class CooldownManager:
    @staticmethod
    async def is_on_cooldown(player_id: int, action: str, cooldown_seconds: int) -> bool:
        """Проверить, находится ли экшн на кулдауне"""
        r = await redis.from_url(REDIS_URL)
        try:
            key = f"cooldown:{action}:{player_id}"
            result = await r.get(key)
            return result is not None
        finally:
            await r.close()
    
    @staticmethod
    async def set_cooldown(player_id: int, action: str, cooldown_seconds: int) -> None:
        """Установить кулдаун для акции"""
        r = await redis.from_url(REDIS_URL)
        try:
            key = f"cooldown:{action}:{player_id}"
            await r.setex(key, cooldown_seconds, "1")
        finally:
            await r.close()
    
    @staticmethod
    async def get_remaining_cooldown(player_id: int, action: str) -> int:
        """Получить оставшееся время кулдауна (в секундах)"""
        r = await redis.from_url(REDIS_URL)
        try:
            key = f"cooldown:{action}:{player_id}"
            ttl = await r.ttl(key)
            return max(0, ttl)
        finally:
            await r.close()
