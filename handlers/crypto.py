from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from services.crypto_service import CryptoService
from keyboards.inline import get_crypto_menu

router = Router()
crypto_service = CryptoService()


@router.message(Command("crypto"))
async def cmd_crypto(message: types.Message):
    """Команда /crypto - крипторынок"""
    crypto_text = (
        "<b>📈 Крипторынок</b>\n\n"
        "Выберите криптовалюту для просмотра цены:\n\n"
        "🔵 BTC - Bitcoin\n"
        "🔴 ETH - Ethereum\n"
        "🔘 TON - Toncoin\n"
        "🛠 SHD - Shadow (внутренняя валюта)\n\n"
        "<i>/buy [coin] [amount]</i> - купить\n"
        "<i>/sell [coin] [amount]</i> - продать"
    )
    
    await message.answer(crypto_text, reply_markup=get_crypto_menu())


@router.message(Command("buy"))
async def cmd_buy(message: types.Message, session: AsyncSession):
    """Команда /buy - купить крипто"""
    try:
        args = message.text.split()
        if len(args) < 3:
            await message.answer("💬 Использование: /buy [coin] [amount]\nПример: /buy btc 0.01")
            return
        
        coin = args[1]
        try:
            amount = float(args[2])
        except ValueError:
            await message.answer("❌ Неверное количество")
            return
        
        success, result = await crypto_service.buy_crypto(session, message.from_user.id, coin, amount)
        await message.answer(result)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")


@router.message(Command("sell"))
async def cmd_sell(message: types.Message, session: AsyncSession):
    """Команда /sell - продать крипто"""
    try:
        args = message.text.split()
        if len(args) < 3:
            await message.answer("💬 Использование: /sell [coin] [amount]\nПример: /sell btc 0.01")
            return
        
        coin = args[1]
        try:
            amount = float(args[2])
        except ValueError:
            await message.answer("❌ Неверное количество")
            return
        
        success, result = await crypto_service.sell_crypto(session, message.from_user.id, coin, amount)
        await message.answer(result)
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")
