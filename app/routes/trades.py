from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from app.core.database import get_db
from app.models.schemas import TradeResponse, TradeHistoryResponse, TradeCreate
from app.models.database import User, Trade, TradeStatus
from app.routes.auth import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/trades", tags=["Trades"])


@router.get("/active", response_model=list[TradeResponse])
async def get_active_trades(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all active trades"""
    result = await db.execute(
        select(Trade).where(
            and_(
                Trade.user_id == current_user.id,
                Trade.status == TradeStatus.OPEN
            )
        ).order_by(desc(Trade.opened_at))
    )
    return result.scalars().all()


@router.get("/history", response_model=TradeHistoryResponse)
async def get_trade_history(
    current_user: User = Depends(get_current_user),
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db)
):
    """Get trade history"""
    date_from = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(Trade).where(
            and_(
                Trade.user_id == current_user.id,
                Trade.closed_at >= date_from
            )
        ).order_by(desc(Trade.closed_at))
    )
    trades = result.scalars().all()
    
    if not trades:
        return TradeHistoryResponse(
            total_trades=0,
            winning_trades=0,
            losing_trades=0,
            win_rate=0.0,
            average_profit=0.0,
            max_profit=0.0,
            max_loss=0.0,
            trades=[]
        )
    
    # Calculate statistics
    total_trades = len(trades)
    winning_trades = sum(1 for t in trades if t.pnl > 0)
    losing_trades = sum(1 for t in trades if t.pnl <= 0)
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
    average_profit = sum(t.pnl for t in trades) / total_trades if total_trades > 0 else 0.0
    max_profit = max((t.pnl for t in trades), default=0.0)
    max_loss = min((t.pnl for t in trades), default=0.0)
    
    return TradeHistoryResponse(
        total_trades=total_trades,
        winning_trades=winning_trades,
        losing_trades=losing_trades,
        win_rate=round(win_rate, 2),
        average_profit=round(average_profit, 2),
        max_profit=round(max_profit, 2),
        max_loss=round(max_loss, 2),
        trades=trades
    )


@router.post("/open", response_model=TradeResponse)
async def open_trade(
    trade: TradeCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Open new trade"""
    new_trade = Trade(
        user_id=current_user.id,
        **trade.dict()
    )
    db.add(new_trade)
    await db.commit()
    await db.refresh(new_trade)
    
    return new_trade


@router.post("/close/{trade_id}")
async def close_trade(
    trade_id: int,
    exit_price: float,
    close_reason: str = "manual",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Close a trade"""
    result = await db.execute(
        select(Trade).where(
            and_(
                Trade.id == trade_id,
                Trade.user_id == current_user.id
            )
        )
    )
    trade = result.scalars().first()
    
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    # Calculate P&L
    if trade.direction.value == "buy":
        pnl = (exit_price - trade.entry_price) * trade.volume
    else:
        pnl = (trade.entry_price - exit_price) * trade.volume
    
    pnl_percentage = (pnl / (trade.entry_price * trade.volume) * 100) if trade.entry_price > 0 else 0.0
    
    # Update trade
    trade.status = TradeStatus.CLOSED
    trade.exit_price = exit_price
    trade.pnl = pnl
    trade.pnl_percentage = pnl_percentage
    trade.closed_at = datetime.utcnow()
    trade.close_reason = close_reason
    
    await db.commit()
    
    return {"message": "Trade closed", "pnl": pnl}


@router.put("/update/{trade_id}")
async def update_trade(
    trade_id: int,
    current_price: float = None,
    stop_loss: float = None,
    take_profit: float = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update trade details"""
    result = await db.execute(
        select(Trade).where(
            and_(
                Trade.id == trade_id,
                Trade.user_id == current_user.id
            )
        )
    )
    trade = result.scalars().first()
    
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    
    if current_price is not None:
        trade.current_price = current_price
        # Update P&L
        if trade.direction.value == "buy":
            trade.pnl = (current_price - trade.entry_price) * trade.volume
        else:
            trade.pnl = (trade.entry_price - current_price) * trade.volume
    
    if stop_loss is not None:
        trade.stop_loss = stop_loss
    
    if take_profit is not None:
        trade.take_profit = take_profit
    
    await db.commit()
    
    return {"message": "Trade updated"}
