import asyncio
import random
import logging
import aiosqlite

from aiogram import Bot, Dispatcher
from aiogram.types import Message, BotCommand
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime

# =========================
# НАСТРОЙКИ
# =========================

BOT_TOKEN = "8667594467:AAGYXAeHIcEnUHfw7EUcOckkPKqh3-xAeag"

DB_NAME = "shadow_market.db"

# Limits
HACK_LIMIT = 50000

# =========================
# ЛОГИ
# =========================

logging.basicConfig(level=logging.INFO)

# =========================
# БОТ
# =========================

bot = Bot(token=BOT_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

# =========================
# КРИПТОРЫНОК
# =========================

crypto_prices = {
    "btc": 100000,
    "eth": 8000,
    "ton": 150,
    "shd": 25
}

# =========================
# БАЗА ДАННЫХ
# =========================

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,

            hryvnia INTEGER DEFAULT 1000,
            dollars INTEGER DEFAULT 0,
            euros INTEGER DEFAULT 0,

            reputation INTEGER DEFAULT 100,
            wanted TEXT DEFAULT 'Нет',

            organization TEXT DEFAULT 'Мирный',
            role TEXT DEFAULT 'Игрок',

            corruption INTEGER DEFAULT 0,
            is_arrested INTEGER DEFAULT 0,
            bail INTEGER DEFAULT 0,
            court_cases INTEGER DEFAULT 0,
            tax_alert_sent INTEGER DEFAULT 0,

            btc REAL DEFAULT 0,
            eth REAL DEFAULT 0,
            ton REAL DEFAULT 0,
            shd REAL DEFAULT 0
        )
        """)

        # Ensure businesses table exists (simple schema for aiosqlite compatibility)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            owner_id INTEGER,
            business_name TEXT,
            income INTEGER,
            risk INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS court_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT,
            organization TEXT,
            reason TEXT,
            status TEXT
        )
        """)

        # Try to add missing columns for existing DBs
        for column_sql in [
            "ALTER TABLE players ADD COLUMN corruption INTEGER DEFAULT 0",
            "ALTER TABLE players ADD COLUMN is_arrested INTEGER DEFAULT 0",
            "ALTER TABLE players ADD COLUMN bail INTEGER DEFAULT 0",
            "ALTER TABLE players ADD COLUMN court_cases INTEGER DEFAULT 0",
            "ALTER TABLE players ADD COLUMN tax_alert_sent INTEGER DEFAULT 0"
        ]:
            try:
                await db.execute(column_sql)
            except Exception:
                pass

        await db.commit()

async def create_player(user_id, username):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        INSERT OR IGNORE INTO players
        (user_id, username)
        VALUES (?, ?)
        """, (user_id, username))

        await db.commit()

async def get_player(user_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT * FROM players
        WHERE user_id = ?
        """, (user_id,))

        return await cursor.fetchone()

async def add_money(user_id, amount):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        UPDATE players
        SET hryvnia = hryvnia + ?
        WHERE user_id = ?
        """, (amount, user_id))

        await db.commit()

async def set_org(user_id, org):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        UPDATE players
        SET organization = ?
        WHERE user_id = ?
        """, (org, user_id))

        await db.commit()

async def buy_crypto(user_id, coin, amount):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            f"UPDATE players SET {coin} = {coin} + ? WHERE user_id = ?",
            (amount, user_id)
        )

        await db.commit()

# =========================
# КРИПТА LOOP
# =========================

async def crypto_loop():

    while True:

        for coin in crypto_prices:

            change = random.randint(-500, 1000)

            crypto_prices[coin] += change

            if crypto_prices[coin] < 1:
                crypto_prices[coin] = 1

        await asyncio.sleep(1800)

# =========================
# START
# =========================

@dp.message(Command("start"))
async def start_cmd(message: Message):

    user = message.from_user

    await create_player(
        user.id,
        user.username or "NoUsername"
    )

    await message.answer(
        f"""
🔥 Добро пожаловать в SHADOW MARKET

👤 Игрок: @{user.username}

💴 Вы получили стартовый капитал:
₴1000

📖 Используйте:
/help
"""
    )

# =========================
# PROFILE

@dp.message(Command("profile"))
async def profile_cmd(message: Message):

    player = await get_player(message.from_user.id)

    if not player:
        return await message.answer("❌ Напишите /start")

    text = f"""
👤 ПРОФИЛЬ

🆔 ID: {player[0]}
👤 Username: @{player[1]}

💴 Гривна: ₴{player[2]}
💵 Доллары: ${player[3]}
💶 Евро: €{player[4]}

⭐ Репутация: {player[5]}
🚔 Розыск: {player[6]}

🏢 Организация: {player[7]}
    🎭 Роль: {player[9]}

📈 КРИПТА

BTC: {player[13]}
ETH: {player[14]}
TON: {player[15]}
SHD: {player[16]}
"""

    await message.answer(text)

# =========================
# BALANCE
# =========================

@dp.message(Command("balance"))
async def balance_cmd(message: Message):

    player = await get_player(message.from_user.id)

    if not player:
        return await message.answer("❌ Напишите /start")

    await message.answer(
        f"""
💰 БАЛАНС

₴{player[2]}
${player[3]}
€{player[4]}
"""
    )

# =========================
# WORK
# =========================

@dp.message(Command("work"))
async def work_cmd(message: Message):

    amount = random.randint(200, 1500)

    await add_money(message.from_user.id, amount)

    works = [
        "Вы перепродали крипту",
        "Вы сделали теневую сделку",
        "Вы продали информацию",
        "Вы открыли ларёк",
        "Вы получили взятку",
        "Вы разгрузили контрабанду"
    ]

    choice = random.choice(works)

    # give feedback
    await message.answer(
        f"""
💼 {choice}

💴 +₴{amount}
"""
    )

    # corruption triggers
    if choice == "Вы получили взятку":

        incr = random.randint(5, 20)

        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("""
            UPDATE players
            SET corruption = corruption + ?
            WHERE organization = 'Полиция'
            """, (incr,))
            await db.commit()

        # notify NABU about possible corruption
        await notify_nabu("Обнаружена возможная коррупция в полиции")

    # If a police member got a large payday, increase their corruption
    player = await get_player(message.from_user.id)
    try:
        org = player[7]
    except Exception:
        org = None

    if org == 'Полиция' and amount > 2000:

        incr = random.randint(5, 20)

        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("""
            UPDATE players
            SET corruption = corruption + ?
            WHERE user_id = ?
            """, (incr, message.from_user.id))
            await db.commit()

        # notify NABU
        await notify_nabu("Обнаружена возможная коррупция в полиции")

# =========================
# CRYPTO
# =========================

@dp.message(Command("crypto"))
async def crypto_cmd(message: Message):

    await message.answer(
        f"""
📈 КРИПТОРЫНОК

BTC — ₴{crypto_prices['btc']}
ETH — ₴{crypto_prices['eth']}
TON — ₴{crypto_prices['ton']}
SHD — ₴{crypto_prices['shd']}
"""
    )

# =========================
# BUY
# =========================

@dp.message(Command("buy"))
async def buy_cmd(message: Message):

    args = message.text.split()

    if len(args) != 3:
        return await message.answer(
            "Пример:\n/buy btc 1"
        )

    coin = args[1].lower()

    try:
        amount = float(args[2])
    except:
        return await message.answer("❌ Неверное количество")

    if coin not in crypto_prices:
        return await message.answer("❌ Монета не найдена")

    await buy_crypto(
        message.from_user.id,
        coin,
        amount
    )

    await message.answer(
        f"""
✅ Покупка успешна

🪙 Куплено:
{amount} {coin.upper()}
"""
    )


# =========================
# SELL

@dp.message(Command("sell"))
async def sell_cmd(message: Message):

    args = message.text.split()

    if len(args) != 3:
        return await message.answer(
            "Пример:\n/sell btc 1"
        )

    coin = args[1].lower()

    try:
        amount = float(args[2])
    except:
        return await message.answer(
            "❌ Неверное количество"
        )

    if coin not in crypto_prices:
        return await message.answer(
            "❌ Монета не найдена"
        )

    player = await get_player(message.from_user.id)

    crypto_indexes = {
        "btc": 13,
        "eth": 14,
        "ton": 15,
        "shd": 16
    }

    current_crypto = player[
        crypto_indexes[coin]
    ]

    if current_crypto < amount:
        return await message.answer(
            "❌ Недостаточно крипты"
        )

    price = crypto_prices[coin] * amount

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            f"""
            UPDATE players
            SET {coin} = {coin} - ?,
                hryvnia = hryvnia + ?
            WHERE user_id = ?
            """,
            (
                amount,
                int(price),
                message.from_user.id
            )
        )

        await db.commit()

    await message.answer(
        f"""
💸 ПРОДАЖА КРИПТЫ

🪙 Продано:
{amount} {coin.upper()}

💴 Получено:
₴{int(price)}
"""
    )


# =========================
# REPORTS / FEEDBACK

@dp.message(Command("report"))
async def report_cmd(message: Message):

    text = message.text.replace("/report ", "")

    if not text:
        return await message.answer(
            "Пример:\n/report баг с криптой"
        )

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    username = (
        f"@{message.from_user.username}"
        if message.from_user.username
        else "Без username"
    )

    await bot.send_message(
        ADMIN_ID,
        f"""
📨 НОВЫЙ REPORT

👤 Игрок:
{username}

🆔 ID:
{message.from_user.id}

📅 Дата:
{now}

📝 Текст:
{text}
"""
    )

    await message.answer(
        "✅ Репорт отправлен"
    )


# =========================
# EXCHANGE

@dp.message(Command("exchange"))
async def exchange_cmd(message: Message):

    args = message.text.split()

    if len(args) != 3:
        return await message.answer(
            """
💱 ОБМЕННИК

Покупка:
 /exchange usd 1000
 /exchange eur 2000

Продажа:
 /exchange uahusd 100
 /exchange uaheur 50
"""
        )

    action = args[1].lower()

    try:
        amount = int(args[2])
    except:
        return await message.answer("❌ Неверная сумма")

    player = await get_player(message.from_user.id)

    rates = {
        "usd": 41,
        "eur": 46
    }

    async with aiosqlite.connect(DB_NAME) as db:

        # =========================
        # ПОКУПКА USD
        # =========================

        if action == "usd":

            if player[2] < amount:
                return await message.answer(
                    "❌ Недостаточно гривны"
                )

            result = amount // rates["usd"]

            await db.execute("""
            UPDATE players
            SET hryvnia = hryvnia - ?,
                dollars = dollars + ?
            WHERE user_id = ?
            """, (
                amount,
                result,
                message.from_user.id
            ))

            await db.commit()

            return await message.answer(
                f"""
💱 ОБМЕН

💴 -₴{amount}
💵 +${result}
"""
            )

        # =========================
        # ПОКУПКА EUR
        # =========================

        elif action == "eur":

            if player[2] < amount:
                return await message.answer(
                    "❌ Недостаточно гривны"
                )

            result = amount // rates["eur"]

            await db.execute("""
            UPDATE players
            SET hryvnia = hryvnia - ?,
                euros = euros + ?
            WHERE user_id = ?
            """, (
                amount,
                result,
                message.from_user.id
            ))

            await db.commit()

            return await message.answer(
                f"""
💱 ОБМЕН

💴 -₴{amount}
💶 +€{result}
"""
            )

        # =========================
        # ПРОДАЖА USD
        # =========================

        elif action == "uahusd":

            if player[3] < amount:
                return await message.answer(
                    "❌ Недостаточно долларов"
                )

            result = amount * rates["usd"]

            await db.execute("""
            UPDATE players
            SET dollars = dollars - ?,
                hryvnia = hryvnia + ?
            WHERE user_id = ?
            """, (
                amount,
                result,
                message.from_user.id
            ))

            await db.commit()

            return await message.answer(
                f"""
💱 ОБМЕН

💵 -${amount}
💴 +₴{result}
"""
            )

        # =========================
        # ПРОДАЖА EUR
        # =========================

        elif action == "uaheur":

            if player[4] < amount:
                return await message.answer(
                    "❌ Недостаточно евро"
                )

            result = amount * rates["eur"]

            await db.execute("""
            UPDATE players
            SET euros = euros - ?,
                hryvnia = hryvnia + ?
            WHERE user_id = ?
            """, (
                amount,
                result,
                message.from_user.id
            ))

            await db.commit()

            return await message.answer(
                f"""
💱 ОБМЕН

💶 -€{amount}
💴 +₴{result}
"""
            )

        else:

            return await message.answer(
                "❌ Неизвестная операция"
            )


# =========================
# BUSINESSES
# =========================

@dp.message(Command("buybiz"))
async def buybiz_cmd(message: Message):

    args = message.text.split()

    if len(args) < 2:
        return await message.answer("""
🏢 БИЗНЕСЫ

/buybiz stall
/buybiz casino
/buybiz bank
""")

    biz_types = {
        "stall": {
            "name": "Ларёк",
            "price": 5000,
            "income": 500
        },
        "casino": {
            "name": "Казино",
            "price": 50000,
            "income": 5000
        },
        "bank": {
            "name": "Банк",
            "price": 250000,
            "income": 15000
        }
    }

    biz = args[1].lower()

    if biz not in biz_types:
        return await message.answer("❌ Бизнес не найден")

    player = await get_player(message.from_user.id)

    if player[2] < biz_types[biz]["price"]:
        return await message.answer("❌ Недостаточно денег")

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        UPDATE players
        SET hryvnia = hryvnia - ?
        WHERE user_id = ?
        """, (
            biz_types[biz]["price"],
            message.from_user.id
        ))

        await db.execute("""
        INSERT INTO businesses
        (owner_id, business_name, income, risk)
        VALUES (?, ?, ?, ?)
        """, (
            message.from_user.id,
            biz_types[biz]["name"],
            biz_types[biz]["income"],
            random.randint(1, 100)
        ))

        await db.commit()

    await message.answer(
        f"""
✅ Вы купили бизнес:

🏢 {biz_types[biz]["name"]}

💰 Доход:
₴{biz_types[biz]["income"]}/час
"""
    )


@dp.message(Command("mybiz"))
async def mybiz_cmd(message: Message):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT id, business_name, income, risk
        FROM businesses
        WHERE owner_id = ?
        """, (message.from_user.id,))

        rows = await cursor.fetchall()

    if not rows:
        return await message.answer("У вас нет бизнесов")

    text = "🏢 Ваши бизнесы:\n\n"
    for r in rows:
        text += f"ID: {r[0]} — {r[1]} | Доход: ₴{r[2]}/час | Риск: {r[3]}\n"

    await message.answer(text)


async def business_income_loop():

    while True:

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute("""
            SELECT owner_id, income
            FROM businesses
            """)

            businesses = await cursor.fetchall()

            for biz in businesses:

                await db.execute("""
                UPDATE players
                SET hryvnia = hryvnia + ?
                WHERE user_id = ?
                """, (
                    biz[1],
                    biz[0]
                ))

            await db.commit()

        await asyncio.sleep(3600)


async def npc_business_loop():

    while True:

        async with aiosqlite.connect(DB_NAME) as db:

            cursor = await db.execute("""
            SELECT owner_id, business_name
            FROM businesses
            """)

            businesses = await cursor.fetchall()

            for biz in businesses:

                visitors = random.randint(1, 20)
                income = visitors * random.randint(50, 500)

                await db.execute("""
                UPDATE players
                SET hryvnia = hryvnia + ?
                WHERE user_id = ?
                """, (
                    income,
                    biz[0]
                ))

            await db.commit()

        await asyncio.sleep(1800)


# =========================
# ENFORCEMENT

@dp.message(Command("taxfine"))
async def taxfine_cmd(message: Message):

    sender = await get_player(message.from_user.id)

    if sender[7] != "Налоговая":
        return await message.answer(
            "❌ Только Налоговая"
        )

    args = message.text.split()

    if len(args) != 3:
        return await message.answer(
            "/taxfine @user сумма"
        )

    target_username = args[1].replace("@", "")

    amount = int(args[2])

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id, hryvnia
        FROM players
        WHERE username = ?
        """, (target_username,))

        target = await cursor.fetchone()

        if not target:
            return await message.answer(
                "❌ Игрок не найден"
            )

        await db.execute("""
        UPDATE players
        SET hryvnia = hryvnia - ?
        WHERE user_id = ?
        """, (
            amount,
            target[0]
        ))

        await db.commit()

    await message.answer(
        f"""
💰 НАЛОГОВЫЙ ШТРАФ

👤 @{target_username}
💴 -₴{amount}
"""
    )


@dp.message(Command("fine"))
async def fine_cmd(message: Message):

    sender = await get_player(message.from_user.id)

    if sender[7] != "Полиция":
        return await message.answer(
            "❌ Только полиция"
        )

    args = message.text.split()

    if len(args) != 3:
        return await message.answer(
            "/fine @user сумма"
        )

    username = args[1].replace("@", "")

    amount = int(args[2])

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id
        FROM players
        WHERE username = ?
        """, (username,))

        target = await cursor.fetchone()

        if not target:
            return await message.answer(
                "❌ Игрок не найден"
            )

        await db.execute("""
        UPDATE players
        SET hryvnia = hryvnia - ?
        WHERE user_id = ?
        """, (
            amount,
            target[0]
        ))

        await db.commit()

    await message.answer(
        f"""
🚔 ПОЛИЦЕЙСКИЙ ШТРАФ

👤 @{username}
💴 -₴{amount}
"""
    )


@dp.message(Command("arrest"))
async def arrest_cmd(message: Message):

    sender = await get_player(message.from_user.id)

    if sender[7] not in ["Полиция", "СБУ"]:
        return await message.answer(
            "❌ Нет доступа"
        )

    args = message.text.split()

    if len(args) != 3:
        return await message.answer(
            "/arrest @user залог"
        )

    username = args[1].replace("@", "")

    bail = int(args[2])

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id
        FROM players
        WHERE username = ?
        """, (username,))

        target = await cursor.fetchone()

        if not target:
            return await message.answer(
                "❌ Игрок не найден"
            )

        await db.execute("""
        UPDATE players
        SET is_arrested = 1,
            bail = ?
        WHERE user_id = ?
        """, (
            bail,
            target[0]
        ))

        await db.commit()

    await message.answer(
        f"""
⛓ АРЕСТ

👤 @{username}

💰 Залог:
₴{bail}
"""
    )


@dp.message(Command("bail"))
async def bail_cmd(message: Message):

    player = await get_player(message.from_user.id)

    if player[10] == 0:
        return await message.answer(
            "❌ Вы не арестованы"
        )

    bail_amount = player[11]

    if player[2] < bail_amount:
        return await message.answer(
            "❌ Недостаточно денег"
        )

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        UPDATE players
        SET hryvnia = hryvnia - ?,
            is_arrested = 0,
            bail = 0
        WHERE user_id = ?
        """, (
            bail_amount,
            message.from_user.id
        ))

        await db.commit()

    await message.answer(
        f"""
✅ Вы вышли под залог

💴 -₴{bail_amount}
"""
    )


@dp.message(Command("court"))
async def court_cmd(message: Message):

    sender = await get_player(message.from_user.id)

    if sender[7] not in ["Полиция", "Налоговая", "СБУ"]:
        return await message.answer(
            "❌ Нет доступа"
        )

    args = message.text.split()

    if len(args) < 3:
        return await message.answer(
            "/court @user причина"
        )

    username = args[1]

    reason = " ".join(args[2:])

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id
        FROM players
        WHERE organization = 'Суд'
        """)

        judges = await cursor.fetchall()

    for judge in judges:

        try:
            await bot.send_message(
                judge[0],
                f"""
⚖️ НОВОЕ ДЕЛО

👤 {username}

📄 Причина:
{reason}
"""
            )
        except:
            pass

    await message.answer(
        "⚖️ Дело передано в суд"
    )

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        INSERT INTO court_cases
        (username, organization, reason, status)
        VALUES (?, ?, ?, ?)
        """, (
            username,
            sender[7],
            reason,
            "OPEN"
        ))

        await db.commit()


# =========================
# JUDGE

@dp.message(Command("cases"))
async def cases_cmd(message: Message):

    player = await get_player(message.from_user.id)

    if player[7] != "Суд":
        return await message.answer(
            "❌ Только Суд"
        )

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT id, username, organization, reason
        FROM court_cases
        WHERE status = 'OPEN'
        """)

        cases = await cursor.fetchall()

    if not cases:
        return await message.answer(
            "📂 Дел нет"
        )

    text = "⚖️ АКТИВНЫЕ ДЕЛА\n\n"

    for case in cases:
        text += f"""
🆔 #{case[0]}
👤 {case[1]}
🏢 {case[2]}
📄 {case[3]}

"""

    await message.answer(text)


@dp.message(Command("archive"))
async def archive_cmd(message: Message):

    player = await get_player(message.from_user.id)

    if player[7] != "Суд":
        return await message.answer(
            "❌ Только Суд"
        )

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT id, username, reason
        FROM court_cases
        WHERE status = 'CLOSED'
        """)

        cases = await cursor.fetchall()

    text = "📁 АРХИВ ДЕЛ\n\n"

    for case in cases:
        text += f"""
⚖️ #{case[0]}
👤 {case[1]}
📄 {case[2]}

"""

    await message.answer(text)


@dp.message(Command("raid"))
async def raid_cmd(message: Message):

    player = await get_player(message.from_user.id)

    if player[7] not in ["НАБУ", "СБУ"]:
        return await message.answer(
            "❌ Нет доступа"
        )

    args = message.text.split()

    if len(args) != 2:
        return await message.answer(
            "/raid @user"
        )

    username = args[1].replace("@", "")

    success = random.randint(1, 100)

    if success >= 50:

        stolen = random.randint(5000, 50000)

        await message.answer(
            f"""
🚨 РЕЙД УСПЕШЕН

👤 @{username}

💴 Изъято:
₴{stolen}
"""
        )

    else:

        await message.answer(
            "❌ Рейд провалился"
        )


@dp.message(Command("wanted"))
async def wanted_cmd(message: Message):

    player = await get_player(message.from_user.id)

    status = player[6]

    await message.answer(
        f"🚔 Розыск: {status}"
    )


ADMIN_ID = 490527114


@dp.message(Command("addmoney"))
async def addmoney_cmd(message: Message):

    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()

    # Reply mode: /addmoney 50000 as a reply to user's message
    if message.reply_to_message:

        if len(args) != 2:
            return await message.answer(
                "Пример:\n/addmoney 50000 (ответ на сообщение игрока)"
            )

        try:
            amount = int(args[1])
        except:
            return await message.answer("❌ Неверная сумма")

        target_id = message.reply_to_message.from_user.id

    else:

        if len(args) != 3:
            return await message.answer(
                "/addmoney @user 50000"
            )

        target = args[1].replace("@", "")

        try:
            amount = int(args[2])
        except:
            return await message.answer("❌ Неверная сумма")

        async with aiosqlite.connect(DB_NAME) as db:

            # support lookup by username OR user_id
            lookup_param = None
            try:
                lookup_param = int(target)
            except:
                lookup_param = target

            cursor = await db.execute("""
            SELECT user_id
            FROM players
            WHERE username = ? OR user_id = ?
            """, (target, lookup_param))

            user = await cursor.fetchone()

            if not user:
                return await message.answer(
                    "❌ Игрок не найден"
                )

            target_id = user[0]

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        UPDATE players
        SET hryvnia = hryvnia + ?
        WHERE user_id = ?
        """, (
            amount,
            target_id
        ))

        await db.commit()

    await message.answer(
        f"✅ Выдано ₴{amount}"
    )


@dp.message(Command("addcrypto"))
async def addcrypto_cmd(message: Message):

    if message.from_user.id != ADMIN_ID:
        return
    args = message.text.split()

    # Reply mode: /addcrypto btc 5 (reply to user)
    if message.reply_to_message:

        if len(args) != 3:
            return await message.answer(
                "Пример:\n/addcrypto btc 5 (ответ на сообщение игрока)"
            )

        coin = args[1].lower()
        try:
            amount = float(args[2])
        except:
            return await message.answer("❌ Неверное количество")

        target_id = message.reply_to_message.from_user.id

    else:

        if len(args) != 4:
            return await message.answer(
                "/addcrypto @user btc 5"
            )

        target = args[1].replace("@", "")
        coin = args[2].lower()

        try:
            amount = float(args[3])
        except:
            return await message.answer("❌ Неверное количество")

        async with aiosqlite.connect(DB_NAME) as db:

            lookup_param = None
            try:
                lookup_param = int(target)
            except:
                lookup_param = target

            cursor = await db.execute("""
            SELECT user_id
            FROM players
            WHERE username = ? OR user_id = ?
            """, (target, lookup_param))

            user = await cursor.fetchone()

            if not user:
                return await message.answer(
                    "❌ Игрок не найден"
                )

            target_id = user[0]

    # validate coin
    if coin not in ["btc", "eth", "ton", "shd"]:
        return await message.answer("❌ Монета не найдена")

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            f"UPDATE players SET {coin} = {coin} + ? WHERE user_id = ?",
            (
                amount,
                target_id
            )
        )

        await db.commit()

    await message.answer(
        f"✅ Выдано {amount} {coin.upper()}"
    )


@dp.message(Command("setrole"))
async def setrole_cmd(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    args = message.text.split()

    role = " ".join(args[1:])

    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
        UPDATE players
        SET role = ?
        WHERE user_id = ?
        """, (
            role,
            ADMIN_ID
        ))

        await db.commit()

    await message.answer(
        f"✅ Роль изменена: {role}"
    )


@dp.message(Command("news"))
async def news_cmd(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = message.text.replace("/news ", "")

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id FROM players
        """)

        users = await cursor.fetchall()

    for user in users:

        try:
            await bot.send_message(
                user[0],
                f"""
📰 НОВОСТИ SHADOW MARKET

{text}
"""
            )
        except:
            pass

    await message.answer(
        "✅ Новость опубликована"
    )


# =========================
# NOTIFICATIONS
# =========================

async def notify_nabu(text):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id
        FROM players
        WHERE organization = 'НАБУ'
        """)

        users = await cursor.fetchall()

    for user in users:

        try:
            await bot.send_message(
                user[0],
                f"🚨 НАБУ ALERT\n\n{text}"
            )
        except:
            pass


async def notify_tax(organization, username, reason, amount):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id
        FROM players
        WHERE organization = 'Налоговая'
        """)

        users = await cursor.fetchall()

    text = f"""
🚨 НАЛОГОВАЯ ALERT

🏢 Организация:
{organization}

👤 Игрок:
@{username}

📄 Нарушение:
{reason}

💴 Сумма:
₴{amount}
"""

    for user in users:

        try:
            await bot.send_message(
                user[0],
                text
            )
        except:
            pass


async def notify_tax_simple(text):

    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute("""
        SELECT user_id
        FROM players
        WHERE organization = 'Налоговая'
        """)

        users = await cursor.fetchall()

    for user in users:

        try:
            await bot.send_message(
                user[0],
                f"💰 НАЛОГОВАЯ ALERT\n\n{text}"
            )
        except:
            pass


# =========================
# HACK (example) — uses HACK_LIMIT
# =========================

@dp.message(Command("hack"))
async def hack_cmd(message: Message):

    # simple example: attempt to hack and gain money
    hacked_money = random.randint(1000, 100000)

    await add_money(message.from_user.id, hacked_money)

    player = await get_player(message.from_user.id)

    await message.answer(f"Вы получили теневые деньги: ₴{hacked_money}")

    if player[2] >= 500000:

        await notify_tax(
            "Хактивисты",
            player[1] or "NoUsername",
            "Подозрительно большой доход",
            player[2]
        )

# =========================
# ORG
# =========================

@dp.message(Command("org"))
async def org_cmd(message: Message):

    args = message.text.split()

    if len(args) < 2:

        return await message.answer("""
🏢 ОРГАНИЗАЦИИ

/org police
/org sbu
/org nabu
/org tax
/org hackers
/org judge
""")

    orgs = {
        "police": "Полиция",
        "sbu": "СБУ",
        "nabu": "НАБУ",
        "tax": "Налоговая",
        "hackers": "Хактивисты",
        "judge": "Суд"
    }

    org = args[1].lower()

    if org not in orgs:
        return await message.answer("❌ Организация не найдена")

    await set_org(
        message.from_user.id,
        orgs[org]
    )

    await message.answer(
        f"""
✅ Вы вступили в организацию:

🏢 {orgs[org]}
"""
    )

# =========================
# HELP
# =========================

@dp.message(Command("help"))
async def help_cmd(message: Message):

    text = """
📖 SHADOW MARKET HELP

👤 ОСНОВНЫЕ

/start — начать игру
/profile — профиль
/balance — баланс
/work — заработать

/report текст

💻 КРИПТА

/crypto — рынок
/buy btc 1 — купить
/exchange usd 1000 — обменять гривну

🏢 ОРГАНИЗАЦИИ

/org police
/org sbu
/org nabu
/org tax
/org hackers
/org judge

🏢 БИЗНЕСЫ

/buybiz — купить бизнес
/mybiz — показать мои бизнесы

⚖️ ПРАВОПОРЯДОК

/taxfine @user сумма — штраф Налоговой
/fine @user сумма — штраф Полиции
/arrest @user залог — посадить под арест
/bail — выйти под залог
/court @user причина — отправить дело в суд
/cases — активные дела
/archive — архив дел
/wanted — статус розыска

🛡️ НАБУ/СБУ

/raid @user — рейд

👑 АДМИН

/addmoney @user сумма
/addcrypto @user coin сумма
/setrole роль
/news текст


"""

    await message.answer(text)

# =========================
# MAIN
# =========================

async def main():

    await init_db()

    commands = [
        BotCommand(command="start", description="Начать игру"),
        BotCommand(command="profile", description="Профиль"),
        BotCommand(command="balance", description="Баланс"),
        BotCommand(command="work", description="Работать"),
        BotCommand(command="crypto", description="Крипта"),
        BotCommand(command="buy", description="Купить крипту"),
        BotCommand(command="exchange", description="Обмен валют"),
        BotCommand(command="org", description="Организации"),
        BotCommand(command="taxfine", description="Штраф Налоговой"),
        BotCommand(command="fine", description="Штраф Полиции"),
        BotCommand(command="arrest", description="Арестовать игрока"),
        BotCommand(command="bail", description="Выйти под залог"),
        BotCommand(command="court", description="Передать дело в суд"),
        BotCommand(command="help", description="Справка"),
        BotCommand(command="buybiz", description="Купить бизнес"),
        BotCommand(command="mybiz", description="Мои бизнесы"),
        BotCommand(command="raid", description="Рейд НАБУ/СБУ"),
        BotCommand(command="cases", description="Активные дела"),
        BotCommand(command="archive", description="Архив дел"),
        BotCommand(command="wanted", description="Статус розыска"),
        BotCommand(command="addmoney", description="Выдать деньги (админ)"),
        BotCommand(command="addcrypto", description="Выдать крипту (админ)"),
        BotCommand(command="setrole", description="Изменить роль (админ)"),
        BotCommand(command="news", description="Разослать новости (админ)"),
        BotCommand(command="hack", description="Выполнить взлом (пример)")
    ]

    await bot.set_my_commands(commands)

    asyncio.create_task(crypto_loop())
    asyncio.create_task(business_income_loop())
    asyncio.create_task(npc_business_loop())

    print("🚀 BOT STARTED")

    await dp.start_polling(bot)

# =========================
# START BOT
# =========================

if __name__ == "__main__":
    asyncio.run(main())