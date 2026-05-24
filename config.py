import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Экономика
STARTING_BALANCE = 1000
REPUTATION_START = 100
WANTED_START = 0

# Работа
WORK_MIN_INCOME = 200
WORK_MAX_INCOME = 1200
WORK_COOLDOWN = 10 * 60  # 10 минут

# Крипто
CRYPTO_UPDATE_INTERVAL = 30 * 60  # 30 минут
BTC_CHANGE_RANGE = (-5, 7)
ETH_CHANGE_RANGE = (-8, 10)
