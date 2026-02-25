from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.schemas import AccountResponse
from app.models.database import User, Account
from app.routes.auth import get_current_user

router = APIRouter(prefix="/account", tags=["Account"])


@router.get("/info", response_model=AccountResponse)
async def get_account_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get account information"""
    # Get user's primary account (first account)
    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id).limit(1)
    )
    account = result.scalars().first()
    
    if not account:
        # Create default account if not exists
        account = Account(
            user_id=current_user.id,
            balance=10000.0,  # Demo balance
            equity=10000.0,
            free_margin=10000.0,
        )
        db.add(account)
        await db.commit()
        await db.refresh(account)
    
    return account


@router.post("/update")
async def update_account(
    balance: float,
    equity: float,
    free_margin: float,
    margin_used: float,
    margin_level: float,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update account information (called by MT5 connector)"""
    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id).limit(1)
    )
    account = result.scalars().first()
    
    if account:
        account.balance = balance
        account.equity = equity
        account.free_margin = free_margin
        account.margin_used = margin_used
        account.margin_level = margin_level
        await db.commit()
        await db.refresh(account)
    
    return {"message": "Account updated"}
