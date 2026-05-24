# Shadow Market Bot - API и Архитектура

## 🏗️ Архитектура

```
Command -> Handler -> Service -> Database
   |
   └-> Middleware (инъекция БД сессии)
```

## 📚 Services API

### EconomyService

```python
# Получить или создать игрока
await EconomyService.get_or_create_player(session, player_id, username)

# Работать (получить заработок)
income, message = await EconomyService.work(session, player_id)

# Получить баланс
balance = await EconomyService.get_balance(session, player_id)
# Returns: {hryvnia, dollars, euros, reputation, organization}
```

### CryptoService

```python
crypto_service = CryptoService()

# Получить кошелек
wallet = await CryptoService.get_or_create_wallet(session, player_id)

# Получить цены из Redis
prices = await crypto_service.get_prices()
# Returns: {btc: 67000, eth: 3500, ton: 5.2, shd: 0.0012}

# Купить крипто
success, message = await crypto_service.buy_crypto(session, player_id, "btc", 0.01)

# Продать крипто
success, message = await crypto_service.sell_crypto(session, player_id, "eth", 1.5)
```

### OrgService

```python
# Присоединиться к организации
success, message = await OrgService.join_org(session, player_id, "police")

# Оставить организацию
success, message = await OrgService.leave_org(session, player_id)
```

### CooldownManager

```python
from utils.cooldowns import CooldownManager

# Проверить на cooldown
is_on_cooldown = await CooldownManager.is_on_cooldown(player_id, "work", cooldown_seconds)

# Установить cooldown
await CooldownManager.set_cooldown(player_id, "work", 600)  # 10 минут

# Получить оставшееся время (в секундах)
remaining = await CooldownManager.get_remaining_cooldown(player_id, "work")
```

## 🗄️ Database Models

### Player
```python
id: BIGINT PRIMARY KEY          # Telegram User ID
username: STRING                 # Telegram username
hryvnia: BIGINT (1000)          # Валюта ₴
dollars: BIGINT (0)             # Валюта $
euros: BIGINT (0)               # Валюта €
reputation: INTEGER (100)       # Репутация
wanted: INTEGER (0)             # Разыскиваемость (в будущем)
organization: STRING ("civilian")  # Организация
role: STRING ("player")         # Роль
created_at: TIMESTAMP           # Дата создания
```

### CryptoWallet
```python
player_id: BIGINT PRIMARY KEY    # Владелец
btc: DECIMAL(18,8)              # Bitcoin
eth: DECIMAL(18,8)              # Ethereum
ton: DECIMAL(18,8)              # Toncoin
shd: DECIMAL(18,8)              # Shadow (внутренняя валюта)
```

### Business
```python
id: SERIAL PRIMARY KEY
owner_id: BIGINT                # Владелец
business_type: STRING           # Тип бизнеса
income: BIGINT                  # Доход
risk: INTEGER                   # Риск (%)
```

## 📝 Handlers Структура

Каждый обработчик получает:
- `message: types.Message` - объект сообщения Telegram
- `session: AsyncSession` - сессия БД (инъецируется middleware)

```python
@router.message(Command("start"))
async def cmd_start(message: types.Message, session: AsyncSession):
    # session доступна благодаря middleware
    player = await EconomyService.get_or_create_player(session, message.from_user.id)
```

## 🔄 Жизненный цикл сообщения

1. **Dispatcher** получает сообщение от Telegram
2. **DBSessionMiddleware** создает сессию БД и добавляет в `data["session"]`
3. **Router** находит подходящий обработчик по фильтру (CommandStart, etc)
4. **Handler** вызывается с message и данными (включая session)
5. **Service** выполняет бизнес-логику
6. **Database** выполняет транзакции
7. **Response** отправляется пользователю

## 🔑 Ключевые конфиги (config.py)

```python
# Экономика
STARTING_BALANCE = 1000         # Стартовый баланс
REPUTATION_START = 100          # Начальная репутация
WORK_MIN_INCOME = 200           # Минимум за работу
WORK_MAX_INCOME = 1200          # Максимум за работу
WORK_COOLDOWN = 10 * 60         # 10 минут

# Крипто
CRYPTO_UPDATE_INTERVAL = 30 * 60  # Обновление цен каждые 30 минут
BTC_CHANGE_RANGE = (-5, 7)      # BTC может упасть на 5% или вырасти на 7%
ETH_CHANGE_RANGE = (-8, 10)     # ETH может упасть на 8% или вырасти на 10%
```

## 🚀 Расширение для ЭТАПА 2

### Новый Service: RaidService

```python
class RaidService:
    @staticmethod
    async def start_raid(session: AsyncSession, raider_org: str, target_org: str):
        """Начать рейд"""
        pass
    
    @staticmethod
    async def arrest(session: AsyncSession, police_player_id: int, target_player_id: int):
        """Арестовать игрока"""
        pass
```

### Новый Handler

```python
@router.message(Command("raid"))
async def cmd_raid(message: types.Message, session: AsyncSession):
    """Начать рейд"""
    pass
```

## 📊 Примеры использования

### Пример 1: Получить баланс игрока

```python
from sqlalchemy.ext.asyncio import AsyncSession
from services.economy_service import EconomyService

async def get_player_balance(session: AsyncSession, player_id: int):
    balance = await EconomyService.get_balance(session, player_id)
    return f"Баланс: {balance['hryvnia']}₴"
```

### Пример 2: Купить крипто

```python
from services.crypto_service import CryptoService

crypto = CryptoService()
success, msg = await crypto.buy_crypto(session, player_id, "btc", 0.5)
if success:
    await message.answer(msg)
```

### Пример 3: Проверить cooldown перед работой

```python
from utils.cooldowns import CooldownManager
from config import WORK_COOLDOWN

is_cooldown = await CooldownManager.is_on_cooldown(player_id, "work", WORK_COOLDOWN)
if is_cooldown:
    remaining = await CooldownManager.get_remaining_cooldown(player_id, "work")
    await message.answer(f"Подождите {remaining}с")
```

## ⚡ Performance Notes

- **Redis**: Используется для cooldown (не забыть `sudo systemctl start redis-server`)
- **Database Queries**: Используется asyncpg для асинхронных запросов
- **Connection Pool**: SQLAlchemy автоматически управляет пулом соединений
- **Middleware**: Инъекция БД предотвращает создание новых сессий в каждом обработчике

## 🐛 Отладка

Включить логирование:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Проверить соединение с БД:

```python
async def check_db():
    from database.session import engine
    async with engine.begin() as conn:
        result = await conn.execute("SELECT 1")
        print(result.scalar())
```
