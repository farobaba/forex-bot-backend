from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum


# ============ Auth Schemas ============
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    exness_login: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True


# ============ Account Schemas ============
class AccountResponse(BaseModel):
    id: int
    balance: float
    equity: float
    free_margin: float
    margin_used: float
    margin_level: float
    open_trades_count: int
    daily_profit: float
    last_updated: datetime
    
    class Config:
        from_attributes = True


# ============ Trade Schemas ============
class TradeDirection(str, Enum):
    BUY = "buy"
    SELL = "sell"


class TradeStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"


class TradeCreate(BaseModel):
    symbol: str
    direction: TradeDirection
    entry_price: float
    stop_loss: float
    take_profit: float
    volume: float


class TradeResponse(BaseModel):
    id: int
    symbol: str
    direction: TradeDirection
    status: TradeStatus
    entry_price: float
    current_price: Optional[float]
    exit_price: Optional[float]
    stop_loss: float
    take_profit: float
    volume: float
    pnl: float
    pnl_percentage: float
    opened_at: datetime
    closed_at: Optional[datetime]
    close_reason: Optional[str]
    
    class Config:
        from_attributes = True


class TradeHistoryResponse(BaseModel):
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    average_profit: float
    max_profit: float
    max_loss: float
    trades: List[TradeResponse]


# ============ Signal Schemas ============
class SignalType(str, Enum):
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


class SignalCreate(BaseModel):
    signal_type: SignalType
    confidence: float
    entry_price: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]


class SignalResponse(BaseModel):
    id: int
    symbol: str
    signal_type: SignalType
    confidence: float
    entry_price: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]
    is_valid: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class SignalFeedResponse(BaseModel):
    latest_signal: Optional[SignalResponse]
    valid_signals_count: int
    signals: List[SignalResponse]


# ============ Settings Schemas ============
class SettingsUpdate(BaseModel):
    trading_enabled: bool
    risk_per_trade: float
    max_daily_loss: float
    max_drawdown: float


class SettingsResponse(BaseModel):
    trading_enabled: bool
    risk_per_trade: float
    max_daily_loss: float
    max_drawdown: float


# ============ Analytics Schemas ============
class AnalyticsMetrics(BaseModel):
    total_profit: float
    monthly_profit: float
    win_rate: float
    profit_factor: float
    max_consecutive_wins: int
    max_consecutive_losses: int
    average_trade_duration: float  # in hours
