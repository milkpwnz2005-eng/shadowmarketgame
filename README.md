# Shadow Market Bot 🕵️

Telegram bot для игры в подземный рынок. ЭТАП 1 MVP.

## Установка (Ubuntu/WSL)

```bash
sudo apt update
sudo apt install python3-pip python3-venv redis-server postgresql -y
```

## Создание проекта

```bash
mkdir shadow_market_bot
cd shadow_market_bot
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или для Windows:
# venv\Scripts\activate
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Конфигурация БД

### PostgreSQL

```bash
sudo -u postgres psql
CREATE DATABASE shadow_market;
```

### .env файл

```
BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/shadow_market
REDIS_URL=redis://localhost:6379
```

## Запуск

```bash
python bot.py
```

## Команды

### Основные
- `/start` - Начать игру и получить 1000₴
- `/profile` - Показать профиль
- `/balance` - Показать баланс
- `/help` - Справка

### Экономика
- `/work` - Работать (⏱ cooldown 10 минут)

### Крипто
- `/crypto` - Меню крипторынка
- `/buy [coin] [amount]` - Купить крипто
- `/sell [coin] [amount]` - Продать крипто

### Организации
- `/org` - Меню организаций
- `/org join [name]` - Присоединиться
- `/org leave` - Оставить организацию

## Структура проекта

```
shadow_market_bot/
├── bot.py                 # Основной файл бота
├── config.py              # Конфигурация
├── .env                   # Переменные окружения
│
├── database/
│   ├── models.py          # SQLAlchemy модели
│   ├── session.py         # Управление БД сессией
│   ├── middleware.py      # Middleware для инъекции БД
│   └── init_db.py         # Инициализация БД
│
├── handlers/
│   ├── start.py           # /start команда
│   ├── profile.py         # /profile команда
│   ├── balance.py         # /balance команда
│   ├── economy.py         # /work команда
│   ├── crypto.py          # /crypto, /buy, /sell
│   ├── organizations.py   # /org команды
│   └── help.py            # /help команда
│
├── services/
│   ├── economy_service.py # Бизнес-логика экономики
│   ├── crypto_service.py  # Крипторынок
│   ├── org_service.py     # Организации
│   └── raid_service.py    # Рейды (ЭТАП 2)
│
├── keyboards/
│   └── inline.py          # Inline кнопки
│
├── utils/
│   ├── formatter.py       # Форматирование текста
│   └── cooldowns.py       # Управление cooldown через Redis
│
└── requirements.txt       # Зависимости
```

## Технический стек

- **Framework**: aiogram 3.4
- **БД**: PostgreSQL + SQLAlchemy
- **Кеширование**: Redis
- **Асинхронность**: asyncio/asyncpg

## ЭТАП 1 (Реализовано)

✅ Регистрация (/start)  
✅ Профиль (/profile)  
✅ Баланс (/balance)  
✅ Работа (/work) + cooldown  
✅ Крипторынок (/crypto, /buy, /sell)  
✅ Организации (/org join, /org leave)  
✅ База данных PostgreSQL  

## ЭТАП 2 (Планируется)

⏳ Система рангов в организациях  
⏳ Рейды на организации  
⏳ Аресты  
⏳ PvP атаки  

## ЭТАП 3 (Будущее)

🔮 Глобальная экономика  
🔮 Новости и события  
🔮 Офшоры  
🔮 Аукционы  

## Образец игры

1. Игрок начинает с `/start` и получает 1000₴
2. Каждые 10 минут может использовать `/work` для заработка 200-1200₴
3. На крипторынке может покупать/продавать криптовалюты
4. Может присоединиться к организации через `/org join [name]`

## Развертывание

Для продакшена используйте:
- Nginx как reverse proxy
- systemd для автоматического запуска
- PM2 для управления процессами
