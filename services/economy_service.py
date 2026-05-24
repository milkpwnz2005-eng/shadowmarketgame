import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import Player
from config import WORK_MIN_INCOME, WORK_MAX_INCOME


class EconomyService:
    @staticmethod
    async def get_or_create_player(session: AsyncSession, player_id: int, username: str = None) -> Player:
        """Получить или создать игрока"""
        stmt = select(Player).where(Player.id == player_id)
        result = await session.execute(stmt)
        player = result.scalar_one_or_none()
        
        if not player:
            player = Player(id=player_id, username=username)
            session.add(player)
            await session.commit()
        
        return player
    
    @staticmethod
    async def work(session: AsyncSession, player_id: int) -> tuple[int, str]:
        """Граэвом дня рабодомы: выдача заработка"""
        stmt = select(Player).where(Player.id == player_id)
        result = await session.execute(stmt)
        player = result.scalar_one_or_none()
        
        if not player:
            raise ValueError("Игрок не найден")
        
        income = random.randint(WORK_MIN_INCOME, WORK_MAX_INCOME)
        player.hryvnia += income
        
        events = []
        
        # Понс бонус
        if random.random() < 0.1:  # 10% шанс
            bonus = random.randint(100, 500)
            player.hryvnia += bonus
            events.append(f"🎉 Бонус: +₴1000 + {bonus}")
        
        # Понс налогов
        if random.random() < 0.05:  # 5% шанс
            tax = income // 2
            player.hryvnia -= tax
            events.append(f"🔔 Налоговая: -{tax}")
        
        await session.commit()
        
        message = f"💵 Наработано: +₴{income}"
        if events:
            message += "\n" + "\n".join(events)
        
        return income, message
    
    @staticmethod
    async def get_balance(session: AsyncSession, player_id: int) -> dict:
        """Получить баланс игрока"""
        stmt = select(Player).where(Player.id == player_id)
        result = await session.execute(stmt)
        player = result.scalar_one_or_none()
        
        if not player:
            raise ValueError("Игрок не найден")
        
        return {
            "hryvnia": player.hryvnia,
            "dollars": player.dollars,
            "euros": player.euros,
            "reputation": player.reputation,
            "organization": player.organization,
        }
