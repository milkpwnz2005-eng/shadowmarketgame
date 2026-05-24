from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from services.org_service import OrgService
from keyboards.inline import get_org_menu

router = Router()


@router.message(Command("org"))
async def cmd_org_main(message: types.Message, session: AsyncSession):
    """Команда /org - меню организаций и выполнение команд"""
    args = message.text.split()
    
    # /org join [name]
    if len(args) >= 3 and args[1] == "join":
        org_name = args[2].lower()
        success, result = await OrgService.join_org(session, message.from_user.id, org_name)
        await message.answer(result)
        return
    
    # /org leave
    if len(args) >= 2 and args[1] == "leave":
        success, result = await OrgService.leave_org(session, message.from_user.id)
        await message.answer(result)
        return
    
    # /org (меню)
    org_text = (
        "<b>🏢 Организации</b>\n\n"
        "Присоединитесь к одной из организаций или используйте:\n\n"
        "/org join [name] - присоединиться\n"
        "/org leave - уйти\n\n"
        "<b>Доступные организации:</b>\n"
        "🔌 <b>police</b> - правоохранители\n"
        "🔨 <b>mafia</b> - преступники\n"
        "💼 <b>business</b> - бизнесмены\n"
        "💨 <b>hacker</b> - хакеры"
    )
    
    await message.answer(org_text, reply_markup=get_org_menu())
