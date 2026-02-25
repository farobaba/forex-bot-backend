from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.models.schemas import SignalResponse, SignalFeedResponse
from app.models.database import User, Signal
from app.routes.auth import get_current_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/signals", tags=["Signals"])


@router.get("/latest", response_model=SignalResponse)
async def get_latest_signal(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get latest signal"""
    result = await db.execute(
        select(Signal).where(Signal.user_id == current_user.id).order_by(desc(Signal.created_at)).limit(1)
    )
    signal = result.scalars().first()
    
    if not signal:
        return None
    
    return signal


@router.get("/feed", response_model=SignalFeedResponse)
async def get_signal_feed(
    current_user: User = Depends(get_current_user),
    hours: int = 24,
    db: AsyncSession = Depends(get_db)
):
    """Get signal feed from last N hours"""
    date_from = datetime.utcnow() - timedelta(hours=hours)
    
    result = await db.execute(
        select(Signal).where(
            Signal.user_id == current_user.id,
            Signal.created_at >= date_from
        ).order_by(desc(Signal.created_at))
    )
    signals = result.scalars().all()
    
    latest_signal = signals[0] if signals else None
    valid_signals_count = sum(1 for s in signals if s.is_valid)
    
    return SignalFeedResponse(
        latest_signal=latest_signal,
        valid_signals_count=valid_signals_count,
        signals=signals
    )


@router.get("/history", response_model=list[SignalResponse])
async def get_signal_history(
    current_user: User = Depends(get_current_user),
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get signal history"""
    result = await db.execute(
        select(Signal).where(Signal.user_id == current_user.id).order_by(desc(Signal.created_at)).limit(limit)
    )
    return result.scalars().all()
