from sqlalchemy import (
    BigInteger, Integer, String, Text, DateTime, DECIMAL,
    ForeignKey, func
)
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import datetime

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)

    # Валюты
    hryvnia: Mapped[int] = mapped_column(BigInteger, default=1000)
    dollars: Mapped[int] = mapped_column(BigInteger, default=0)
    euros: Mapped[int] = mapped_column(BigInteger, default=0)

    # Репутация и статус
    reputation: Mapped[int] = mapped_column(Integer, default=100)
    wanted: Mapped[int] = mapped_column(Integer, default=0)

    # Организация и роль
    organization: Mapped[str] = mapped_column(String(255), default="civilian")
    role: Mapped[str] = mapped_column(String(255), default="player")

    # Коррупция
    corruption: Mapped[int] = mapped_column(Integer, default=0)

    # Время создания
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Player {self.id} ({self.username})>"


class CryptoWallet(Base):
    __tablename__ = "crypto_wallets"

    player_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    btc: Mapped[float] = mapped_column(DECIMAL(18, 8), default=0)
    eth: Mapped[float] = mapped_column(DECIMAL(18, 8), default=0)
    ton: Mapped[float] = mapped_column(DECIMAL(18, 8), default=0)
    shd: Mapped[float] = mapped_column(DECIMAL(18, 8), default=0)

    def __repr__(self):
        return f"<CryptoWallet {self.player_id}>"


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    owner_id: Mapped[int] = mapped_column(BigInteger)
    business_type: Mapped[str] = mapped_column(String(255))

    income: Mapped[int] = mapped_column(BigInteger)
    risk: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"<Business {self.id} - {self.business_type}>"
