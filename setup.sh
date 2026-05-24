#!/bin/bash
# Shadow Market Bot - Installation & Run Script

echo "🤖 Shadow Market Bot - ЭТАП 1 MVP"
echo "=================================="
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен"
    echo "Установите: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Проверка Redis
if ! command -v redis-cli &> /dev/null; then
    echo "⚠️  Redis не установлен"
    echo "Установите: sudo apt install redis-server"
fi

# Проверка PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL не установлен"
    echo "Установите: sudo apt install postgresql postgresql-contrib"
fi

echo "✅ Все зависимости проверены"
echo ""

# Создание вenv
if [ ! -d "venv" ]; then
    echo "📦 Создание virtual environment..."
    python3 -m venv venv
    echo "✅ venv создана"
fi

# Активация
source venv/bin/activate

# Установка зависимостей
echo "📥 Установка Python зависимостей..."
pip install -r requirements.txt --quiet

echo ""
echo "🚀 Для запуска бота выполните:"
echo "   source venv/bin/activate"
echo "   python bot.py"
echo ""
echo "📋 Перед запуском:"
echo "   1. Создайте БД: sudo -u postgres psql -c 'CREATE DATABASE shadow_market;'"
echo "   2. Настройте .env файл (BOT_TOKEN, DATABASE_URL, REDIS_URL)"
echo "   3. Убедитесь, что Redis запущен: sudo systemctl start redis-server"
echo "   4. PostgreSQL запущен: sudo systemctl start postgresql"
echo ""
