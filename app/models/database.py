from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    exness_login = Column(String, unique=True, nullable=True)
    exness_api_key = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    trades = relationship("Trade", back_populates="user", cascade="all, delete-orphan")
    signals = relationship("Signal", back_populates="user", cascade="all, delete-orphan")


class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    balance = Column(Float, default=0.0)
    equity = Column(Float, default=0.0)
    free_margin = Column(Float, default=0.0)
    margin_used = Column(Float, default=0.0)
    margin_level = Column(Float, default=0.0)
    open_trades_count = Column(Integer, default=0)
    daily_profit = Column(Float, default=0.0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="accounts")


class TradeDirection(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class TradeStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"


class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, default="XAUUSD")
    direction = Column(Enum(TradeDirection), nullable=False)
    status = Column(Enum(TradeStatus), default=TradeStatus.OPEN)
    entry_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=True)
    exit_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    pnl = Column(Float, default=0.0)
    pnl_percentage = Column(Float, default=0.0)
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    close_reason = Column(String, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="trades")


class SignalType(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class Signal(Base):
    __tablename__ = "signals"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    symbol = Column(String, default="XAUUSD")
    signal_type = Column(Enum(SignalType), nullable=False)
    confidence = Column(Float, nullable=False)  # 0-100
    entry_price = Column(Float, nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    indicators_data = Column(Text, nullable=True)  # JSON string
    is_valid = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="signals")
