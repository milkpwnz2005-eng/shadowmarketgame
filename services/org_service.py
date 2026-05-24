from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import Player


class OrgService:
    @staticmethod
    async def join_org(session: AsyncSession, player_id: int, org_name: str) -> tuple[bool, str]:
        """Присоединиться к организации"""
        VALID_ORGS = ["civilian", "police", "mafia", "business", "hacker"]
        
        if org_name not in VALID_ORGS:
            return False, f"Незнакомая организация: {org_name}"
        
        stmt = select(Player).where(Player.id == player_id)
        result = await session.execute(stmt)
        player = result.scalar_one_or_none()
        
        if not player:
            return False, "Игрок не найден"
        
        if player.organization == org_name:
            return False, f"???? Вы уже в организации {org_name}"
        
        player.organization = org_name
        player.role = "member"
        await session.commit()
        
        return True, f"???? Вы присоединились к ORGS {org_name.upper()}"
    
    @staticmethod
    async def leave_org(session: AsyncSession, player_id: int) -> tuple[bool, str]:
        """Оставить организацию"""
        stmt = select(Player).where(Player.id == player_id)
        result = await session.execute(stmt)
        player = result.scalar_one_or_none()
        
        if not player:
            return False, "Игрок не найден"
        
        if player.organization == "civilian":
            return False, "Вы уже гражданин"
        
        old_org = player.organization
        player.organization = "civilian"
        player.role = "player"
        await session.commit()
        
        return True, f"🚪 Вы покинули {old_org.upper()}"
