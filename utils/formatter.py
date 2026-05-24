def format_balance(hryvnia: int, dollars: int = 0, euros: int = 0) -> str:
    """Форматировать баланс"""
    msg = f"₴{hryvnia:,}"
    if dollars > 0:
        msg += f" | ${dollars:,}"
    if euros > 0:
        msg += f" | €{euros:,}"
    return msg


def format_profile(username: str, org: str, role: str, reputation: int, wanted: int) -> str:
    """Форматировать профиль игрока"""
    return (
        f"<b>👤 {username}</b>\n\n"
        f"<b>👁 Организация:</b> {org.upper()}\n"
        f"<b>🎉 Роль:</b> {role}\n\n"
        f"<b>⭐ Репутация:</b> {reputation}\n"
        f"<b>🚨 Выскеан:</b> {wanted}"
    )
