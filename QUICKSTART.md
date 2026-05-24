# Shadow Market Bot - 🚀 Быстрый Старт

## За 5 минут до запуска

### Шаг 1: Получить Bot Token (2 минуты)

1. Откройте Telegram и найти бота `@BotFather`
2. Отправить `/newbot`
3. Следовать инструкциям (назвать бота, выбрать username)
4. Скопировать полученный токен

### Шаг 2: Выбрать способ запуска

#### ⚡ Самый быстрый способ: Docker

```bash
# 1. Установить Docker Desktop
# https://www.docker.com/products/docker-desktop

# 2. Клонировать/распаковать проект
cd shadow_market_bot

# 3. Создать .env
echo BOT_TOKEN=your_token_here > .env

# 4. Запустить!
docker-compose up -d

# 5. Посмотреть логи
docker-compose logs -f bot
```

**Всё! Бот запущен!** 🎉

---

#### 🐧 На Ubuntu/WSL

```bash
# 1. Установить зависимости
sudo apt update
sudo apt install python3-pip python3-venv redis-server postgresql -y

# 2. Запустить сервисы
sudo service postgresql start
sudo service redis-server start

# 3. Создать БД
sudo -u postgres psql -c "CREATE DATABASE shadow_market;"

# 4. Клонировать проект
cd shadow_market_bot

# 5. Создать venv
python3 -m venv venv
source venv/bin/activate

# 6. Установить зависимости
pip install -r requirements.txt

# 7. Создать .env
echo "BOT_TOKEN=your_token_here" > .env

# 8. Запустить бота
python bot.py
```

---

## Проверить, что работает

```bash
# В Telegram найти вашего бота и отправить:
/start

# Должны получить:
# "Добро пожаловать в Shadow Market 🕵️
#  Вы получили:
#  💵 1000₴
#  ⭐ Репутация: 100"
```

## Команды для игры

| Команда | Описание |
|---------|----------|
| `/start` | 🕵️ Начать игру |
| `/profile` | 👤 Профиль |
| `/balance` | 💵 Баланс |
| `/work` | ⚙️ Работать (заработок 200-1200₴) |
| `/crypto` | 📈 Крипторынок |
| `/buy btc 0.01` | 📥 Купить крипто |
| `/sell eth 1` | 📤 Продать крипто |
| `/org` | 🏢 Организации |
| `/org join police` | 🔌 Присоединиться |
| `/org leave` | ❌ Уйти из организации |
| `/help` | ❓ Справка |

## Структура проекта

```
shadow_market_bot/
├── bot.py              ← Запуск отсюда
├── config.py           ← Конфигурация
├── .env                ← Токены (создать)
├── requirements.txt    ← Зависимости
│
├── handlers/           ← Команды бота
├── services/           ← Бизнес-логика
├── database/           ← БД моделей
├── keyboards/          ← Кнопки
└── utils/              ← Утилиты
```

## Если что-то не работает

### Проблема: "ModuleNotFoundError"
```bash
# Убедитесь, что активирована venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows PowerShell

# Установите зависимости
pip install -r requirements.txt
```

### Проблема: "Connection refused"
```bash
# Проверьте PostgreSQL
sudo service postgresql status

# Или используйте Docker
docker-compose up -d postgres redis
```

### Проблема: "BOT_TOKEN not found"
```bash
# Создайте .env файл
echo "BOT_TOKEN=your_token_here" > .env
# Замените your_token_here на реальный токен от @BotFather
```

## Что дальше?

- 📖 Читай [README.md](README.md) для подробной документации
- 🔧 Смотри [API.md](API.md) для расширения функциональности
- 🪟 На Windows? Соответственно [WINDOWS_SETUP.md](WINDOWS_SETUP.md)

## Поддерживаемые платформы

- ✅ Ubuntu 20.04+ / Debian
- ✅ WSL2 + Ubuntu
- ✅ macOS (с установленными PostgreSQL и Redis)
- ✅ Docker (рекомендуется для Windows)

---

**Готово! Ваш бот запущен и готов к работе!** 🚀
