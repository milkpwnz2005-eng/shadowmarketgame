from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Команда /help - справка"""
    help_text = (
        "<b>🕶 Shadow Market Bot</b>\n\n"
        "<b>Основные команды:</b>\n"
        "/start - Регистрация и начало игры\n"
        "/profile - Показать профиль\n"
        "/balance - Показать баланс\n"
        "/work - Работать и заработать\n"
        "/crypto - Крипторынок\n"
        "/org - Организации\n\n"
        "<b>ЭТАП 1 (MVP)</b>\n"
        "Сейчас доступны только базовые команды для заработка и крипторынка.\n\n"
        "<b>ЭТАП 2 (Скоро)</b>\n"
        "Организации, атаки, рейды, аресты\n\n"
        "<b>ЭТАП 3 (Будущее)</b>\n"
        "Глобальная экономика, новости, события, офшоры, аукционы"
    )
    
    await message.answer(help_text)
