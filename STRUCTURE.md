# Shadow Market Bot - Структура и Обзор

## 📊 Организация кода

```
shadow_market_bot/
│
├── 📄 QUICKSTART.md          ← НАЧНИТЕ ЗДЕСЬ! 🚀
├── 📄 README.md              ← Полная документация
├── 📄 API.md                 ← Архитектура и API
├── 📄 WINDOWS_SETUP.md       ← Инструкции для Windows
│
├── 🐍 bot.py                 ← ГЛАВНЫЙ ФАЙЛ (запуск)
├── ⚙️ config.py              ← Глобальная конфигурация
├── 📋 .env                   ← Переменные окружения (создать)
│
├── requirements.txt          ← Python зависимости (pip install)
├── Dockerfile                ← Для Docker запуска
├── docker-compose.yml        ← Docker контейнеры (PostgreSQL + Redis)
│
├── 📁 database/              ← Слой БД
│   ├── __init__.py
│   ├── models.py            ← SQLAlchemy модели (Player, CryptoWallet, Business)
│   ├── session.py           ← управление сессией (async + pooling)
│   ├── middleware.py        ← Инъекция БД в хендлеры
│   └── init_db.py           ← Миграции и инициализация
│
├── 📁 handlers/              ← Обработчики команд (/start, /work, etc)
│   ├── __init__.py
│   ├── start.py             ← /start (регистрация)
│   ├── profile.py           ← /profile (профиль)
│   ├── balance.py           ← /balance (баланс)
│   ├── help.py              ← /help (справка)
│   ├── economy.py           ← /work (заработок + cooldown)
│   ├── crypto.py            ← /crypto, /buy, /sell
│   └── organizations.py     ← /org join, /org leave
│
├── 📁 services/              ← Бизнес-логика (separoлучи от БД)
│   ├── __init__.py
│   ├── economy_service.py   ← Экономика (работа, баланс)
│   ├── crypto_service.py    ← Крипторынок (цены, сделки) + Redis
│   ├── org_service.py       ← Организации (присоединение)
│   └── raid_service.py      ← Рейды (ЭТАП 2)
│
├── 📁 keyboards/             ← UI кнопки
│   ├── __init__.py
│   └── inline.py            ← Inline кнопки для всех меню
│
├── 📁 utils/                 ← Утилиты
│   ├── __init__.py
│   ├── formatter.py         ← Форматирование текста
│   └── cooldowns.py         ← Cooldown через Redis
│
└── .gitignore               ← Исключить из Git
```

## 🎯 Поток выполнения команды

```
Пользователь отправляет /work
    ↓
Telegram API → Dispatcher (aiogram)
    ↓
DBSessionMiddleware добавляет session в context
    ↓
Router находит @router.message(Command("work"))
    ↓
Обработчик cmd_work получает: message, session
    ↓
Проверка cooldown через Redis (CooldownManager)
    ↓
EconomyService.work() выполняет логику
    ↓
Изменяет Player в PostgreSQL через SQLAlchemy
    ↓
Устанавливает cooldown в Redis
    ↓
Возвращает сообщение пользователю
```

## 🔧 Технологии

| Компонент | Технология | Версия |
|-----------|-----------|--------|
| **API** | aiogram | 3.4.0 |
| **БД** | PostgreSQL + asyncpg | 15, 0.29 |
| **ORM** | SQLAlchemy | 2.0.23 |
| **Кеш** | Redis | 7.0 |
| **Async** | asyncio | builtin |
| **Config** | python-dotenv | 1.0.0 |

## 📈 Масштабирование

### ЭТАП 1 (Текущий MVP) ✅
- Регистрация
- Профиль и баланс  
- Работа с cooldown
- Крипторынок
- Организации

### ЭТАП 2 (Планируется)
- Система рангов в организациях
- Рейды между организациями
- Аресты полицией
- PvP механики

### ЭТАП 3 (Далекое будущее)
- Глобальная экономика между игроками
- Новости и события
- Скрытые офшоры
- Аукционы

## ⚡ Performance Оптимизации

✅ **Асинхронность**: Все операции async  
✅ **Connection Pooling**: SQLAlchemy само управляет пулом  
✅ **Redis Кеш**: Cooldown хранится в памяти, не в БД  
✅ **Middleware**: Инъекция БД сессии для всех обработчиков  
✅ **DECIMAL для крипто**: Точные вычисления без округлений  

## 🧪 Тестирование

### Проверить подключение БД
```python
python -c "from database.session import init_db; import asyncio; asyncio.run(init_db())"
```

### Проверить импорты
```python
python -c "from services import economy_service; from handlers import start; print('OK')"
```

## 📝 Кодовые соглашения

- **Переменные**: `snake_case`
- **Функции**: `async def handler_name()`
- **Классы**: `PascalCase (Service)`
- **Константы**: `UPPER_CASE`
- **Документация**: docstrings для функций

## 🔐 Безопасность

- 🚨 **BOT_TOKEN** в `.env` (не коммитим!)
- 🔒 **Database пароль** в DATABASE_URL
- 🛡️ **SQL Injections** невозможны (SQLAlchemy ORM)
- ⏰ **Cooldown** защищает от спама
- 🔄 **Асинхронность** предотвращает race conditions

## 📦 Развертывание

### Локально
```bash
docker-compose up -d
```

### На сервер
```bash
# Построить образ
docker build -t shadow-market-bot .

# Запустить контейнер
docker run -d --name bot \
  -e BOT_TOKEN=xxx \
  -e DATABASE_URL=postgresql://... \
  -e REDIS_URL=redis://... \
  shadow-market-bot
```

## 🆘 Контакты

Вопросы? Ошибки? Идеи?
- 📖 Читайте [API.md](API.md) для расширений
- 🐛 Проверьте [WINDOWS_SETUP.md](WINDOWS_SETUP.md) для проблем на Windows

---

**Проект готов для ЭТАПА 1 MVP! 🚀**
