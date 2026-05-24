from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import Player
from utils.formatter import format_profile

router = Router()


@router.message(Command("profile"))
async def cmd_profile(message: types.Message, session: AsyncSession):
    """Команда /profile - показать профиль"""
    stmt = select(Player).where(Player.id == message.from_user.id)
    result = await session.execute(stmt)
    player = result.scalar_one_or_none()
    
    if not player:
        await message.answer("❌ Вы не зарегистрированы. Используйте /start")
        return
    
    profile_text = format_profile(
        player.username or "Unknown",
        player.organization,
        player.role,
        player.reputation,
        player.wanted
    )
    
    await message.answer(profile_text)
