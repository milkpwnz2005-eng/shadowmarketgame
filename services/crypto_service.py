import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import Player, CryptoWallet
from config import REDIS_URL
import json


class CryptoService:
    def __init__(self):
        self.redis_url = REDIS_URL
    
    async def get_redis(self):
        return await redis.from_url(self.redis_url)
    
    @staticmethod
    async def get_or_create_wallet(session: AsyncSession, player_id: int) -> CryptoWallet:
        """Получить или создать крипто-кошелек"""
        stmt = select(CryptoWallet).where(CryptoWallet.player_id == player_id)
        result = await session.execute(stmt)
        wallet = result.scalar_one_or_none()
        
        if not wallet:
            wallet = CryptoWallet(player_id=player_id)
            session.add(wallet)
            await session.commit()
        
        return wallet
    
    async def get_prices(self):
        """Получить цены криптов из Redis"""
        r = await self.get_redis()
        try:
            prices_json = await r.get("crypto_prices")
            if prices_json:
                return json.loads(prices_json)
            # Начальные цены
            return {
                "btc": 67000,
                "eth": 3500,
                "ton": 5.2,
                "shd": 0.0012,
            }
        finally:
            await r.close()
    
    async def buy_crypto(self, session: AsyncSession, player_id: int, coin: str, amount: float) -> tuple[bool, str]:
        """Купить криптовалюту"""
        prices = await self.get_prices()
        coin_lower = coin.lower()
        
        if coin_lower not in prices:
            return False, "Неверные коины"
        
        # Получаем игрока и кошелек
        stmt = select(Player).where(Player.id == player_id)
        result = await session.execute(stmt)
        player = result.scalar_one_or_none()
        
        wallet = await self.get_or_create_wallet(session, player_id)
        
        cost = prices[coin_lower] * amount
        
        if player.hryvnia < cost:
            return False, f"Недостаточно ₴: нужно {cost}, есть {player.hryvnia}"
        
        player.hryvnia -= int(cost)
        setattr(wallet, coin_lower, getattr(wallet, coin_lower) + amount)
        
        await session.commit()
        
        return True, f"📄 Куплено {amount} {coin.upper()} за ₴{int(cost)}"
    
    async def sell_crypto(self, session: AsyncSession, player_id: int, coin: str, amount: float) -> tuple[bool, str]:
        """Продать криптовалюту"""
        prices = await self.get_prices()
        coin_lower = coin.lower()
        
        if coin_lower not in prices:
            return False, "Неверные коины"
        
        wallet = await self.get_or_create_wallet(session, player_id)
        player_stmt = select(Player).where(Player.id == player_id)
        player_result = await session.execute(player_stmt)
        player = player_result.scalar_one_or_none()
        
        balance = getattr(wallet, coin_lower)
        
        if balance < amount:
            return False, f"Недостаточно {coin.upper()}: нужно {amount}, есть {balance}"
        
        income = int(prices[coin_lower] * amount)
        player.hryvnia += income
        setattr(wallet, coin_lower, balance - amount)
        
        await session.commit()
        
        return True, f"📄 Продано {amount} {coin.upper()} на ₴{income}"
