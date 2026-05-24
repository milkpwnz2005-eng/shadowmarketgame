# Shadow Market Bot - Запуск на Windows

## Вариант 1: Docker (Рекомендуется для Windows)

### Требования
- Docker Desktop установлен

### Запуск с Docker

```bash
# Создать .env файл
echo BOT_TOKEN=your_token_here > .env
echo DATABASE_URL=postgresql+asyncpg://postgres:password@postgres:5432/shadow_market >> .env
echo REDIS_URL=redis://redis:6379 >> .env

# Запустить контейнеры
docker-compose up -d

# Проверить логи бота
docker-compose logs -f bot

# Остановить
docker-compose down
```

## Вариант 2: WSL (Windows Subsystem for Linux)

### Требования
- WSL2 установлен
- Ubuntu 22.04 LTS образ в WSL

### Установка

```bash
# 1. Открыть WSL терминал
wsl

# 2. Обновить пакеты
sudo apt update && sudo apt upgrade -y

# 3. Установить зависимости
sudo apt install python3-pip python3-venv redis-server postgresql postgresql-contrib -y

# 4. Запустить PostgreSQL
sudo service postgresql start

# 5. Запустить Redis
sudo service redis-server start

# 6. Перейти в директорию проекта
cd /path/to/shadow_market_bot

# 7. Создать БД
sudo -u postgres psql -c "CREATE DATABASE shadow_market;"

# 8. Создать virtual environment
python3 -m venv venv
source venv/bin/activate

# 9. Установить зависимости
pip install -r requirements.txt

# 10. Настроить .env
# Отредактировать .env файл с вашим BOT_TOKEN

# 11. Запустить бота
python bot.py
```

## Вариант 3: Native Windows Python (Не рекомендуется)

### Проблемы
- PostgreSQL и Redis нужно устанавливать отдельно
- asyncpg может требовать компиляции C расширений

### Если все же пытаетесь

```bash
# 1. Установить PostgreSQL
# https://www.postgresql.org/download/windows/

# 2. Установить Redis
# https://github.com/microsoftarchive/redis/releases (или использовать WSL)

# 3. В PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 4. Проверить соединение с БД
python -c "import asyncpg; print('asyncpg OK')"

# 5. Запустить бота
python bot.py
```

## Проверка установки

```bash
# Проверить, что бот может подключиться к БД
python

# В Python интерпретаторе:
import asyncio
from database.session import init_db, engine
asyncio.run(init_db())
# Должно вывести: "✅ База данных инициализирована"
```

## Рекомендуемый вариант для разработки

1. **На Windows**: Docker Desktop + docker-compose
2. **На Linux**: WSL2 с Ubuntu + native инструменты
3. **Для production**: Docker контейнеры

## Команды docker-compose

```bash
# Запустить в фоне
docker-compose up -d

# Просмотр логов
docker-compose logs -f bot
docker-compose logs -f postgres
docker-compose logs -f redis

# Перестроить образ
docker-compose up -d --build

# Остановить
docker-compose down

# Удалить все данные
docker-compose down -v

# Запустить команду в контейнере
docker-compose exec bot python -c "from database.session import init_db; import asyncio; asyncio.run(init_db())"
```

## Troubleshooting

### Ошибка: "postgres connection refused"
- Убедитесь, что PostgreSQL запущен: `sudo service postgresql status`
- Или используйте Docker: `docker-compose up -d postgres`

### Ошибка: "redis connection refused"
- Убедитесь, что Redis запущен: `sudo service redis-server status`
- Или используйте Docker: `docker-compose up -d redis`

### Ошибка при импорте asyncpg
- На Windows нужны Build Tools
- На WSL/Linux: `sudo apt install python3-dev libpq-dev`
- Или используйте Docker

### Медленное подключение к БД
- Используйте Docker для локальной разработки
- Проверьте параметры приватной сети
