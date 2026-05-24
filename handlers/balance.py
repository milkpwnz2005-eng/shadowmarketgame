from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from services.economy_service import EconomyService

router = Router()


@router.message(Command("balance"))
async def cmd_balance(message: types.Message, session: AsyncSession):
    """Команда /balance - показать баланс"""
    try:
        balance = await EconomyService.get_balance(session, message.from_user.id)
        
        balance_text = (
            f"<b>💰 Ваш баланс:</b>\n\n"
            f"₴ <code>{balance['hryvnia']:,}</code>\n"
            f"$ <code>{balance['dollars']:,}</code>\n"
            f"€ <code>{balance['euros']:,}</code>\n\n"
            f"<b>⭐ Репутация:</b> {balance['reputation']}\n"
            f"<b>🏢 Организация:</b> {balance['organization'].upper()}"
        )
        
        await message.answer(balance_text)
    except ValueError as e:
        await message.answer(f"❌ {e}")
