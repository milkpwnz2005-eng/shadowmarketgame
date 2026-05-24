from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu() -> InlineKeyboardMarkup:
    """Основное меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="profile"),
            InlineKeyboardButton(text="💵 Баланс", callback_data="balance"),
        ],
        [
            InlineKeyboardButton(text="⚙ Работа", callback_data="work"),
            InlineKeyboardButton(text="📈 Крипто", callback_data="crypto"),
        ],
        [
            InlineKeyboardButton(text="🏢 Организация", callback_data="org"),
            InlineKeyboardButton(text="❓ Помощь", callback_data="help"),
        ],
    ])


def get_org_menu() -> InlineKeyboardMarkup:
    """Меню организаций"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔌 Полиция", callback_data="org_police"),
            InlineKeyboardButton(text="🔨 Мафия", callback_data="org_mafia"),
        ],
        [
            InlineKeyboardButton(text="💼 Бизнес", callback_data="org_business"),
            InlineKeyboardButton(text="💨 Хакеры", callback_data="org_hacker"),
        ],
        [
            InlineKeyboardButton(text="❌ Оставить", callback_data="org_leave"),
            InlineKeyboardButton(text="◀ Назад", callback_data="org_back"),
        ],
    ])


def get_crypto_menu() -> InlineKeyboardMarkup:
    """Меню крипто"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔵 BTC", callback_data="crypto_btc"),
            InlineKeyboardButton(text="🔴 ETH", callback_data="crypto_eth"),
        ],
        [
            InlineKeyboardButton(text="🔘 TON", callback_data="crypto_ton"),
            InlineKeyboardButton(text="🛠 SHD", callback_data="crypto_shd"),
        ],
        [
            InlineKeyboardButton(text="◀ Назад", callback_data="crypto_back"),
        ],
    ])
