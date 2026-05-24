from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession
from services.economy_service import EconomyService
from keyboards.inline import get_main_menu
from utils.formatter import format_balance

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession):
    """Команда /start - регистрация новичка"""
    player = await EconomyService.get_or_create_player(
        session, message.from_user.id, message.from_user.username
    )
    
    start_text = (
        f"<b>Добро пожаловать в Shadow Market 🕶</b>\n\n"
        f"Вы получили:\n"
        f"💵 {format_balance(1000)}\n"
        f"⭐ Репутация: 100\n\n"
        f"<i>Стартовая роль: Гражданин (Civilian)</i>\n"
        f"<i>Организация: None</i>\n\n"
        f"Выберите действие:"
    )
    
    await message.answer(start_text, reply_markup=get_main_menu())
