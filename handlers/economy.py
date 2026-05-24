from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from services.economy_service import EconomyService
from utils.cooldowns import CooldownManager
from config import WORK_COOLDOWN

router = Router()


@router.message(Command("work"))
async def cmd_work(message: types.Message, session: AsyncSession):
    """Команда /work - работа"""
    player_id = message.from_user.id
    
    # Проверка cooldown
    is_cooldown = await CooldownManager.is_on_cooldown(player_id, "work", WORK_COOLDOWN)
    if is_cooldown:
        remaining = await CooldownManager.get_remaining_cooldown(player_id, "work")
        minutes = remaining // 60
        seconds = remaining % 60
        await message.answer(f"⏳ Вы уже работали. Попробуйте через {minutes}м {seconds}с")
        return
    
    try:
        income, message_text = await EconomyService.work(session, player_id)
        await CooldownManager.set_cooldown(player_id, "work", WORK_COOLDOWN)
        await message.answer(message_text)
    except ValueError as e:
        await message.answer(f"❌ {e}")
