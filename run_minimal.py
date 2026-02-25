"""
Minimal startup script - use this if you have issues with full setup
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create app
app = FastAPI(
    title="Exness AI Trading Bot API",
    version="1.0.0",
    description="AI-Powered Trading Bot API"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic routes
@app.get("/")
async def root():
    return {
        "message": "Exness AI Trading Bot API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# Auth endpoints (mock)
@app.post("/auth/register")
async def register(email: str, password: str, exness_login: str):
    return {
        "success": True,
        "message": "User registered (mock)",
        "user_id": 1
    }

@app.post("/auth/login")
async def login(email: str, password: str):
    return {
        "access_token": "mock_token_12345",
        "token_type": "bearer",
        "expires_in": 1800
    }

@app.get("/account/info")
async def get_account():
    return {
        "id": 1,
        "balance": 10000.0,
        "equity": 10500.0,
        "free_margin": 9500.0,
        "margin_used": 500.0,
        "margin_level": 2100.0,
        "open_trades_count": 0,
        "daily_profit": 500.0
    }

@app.get("/trades/active")
async def get_active_trades():
    return {
        "trades": []
    }

@app.get("/signals/latest")
async def get_latest_signal():
    return {
        "id": 1,
        "symbol": "XAUUSD",
        "signal_type": "BUY",
        "confidence": 75,
        "entry_price": 2050.50,
        "stop_loss": 2040.50,
        "take_profit": 2070.50,
        "is_valid": True
    }

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("Exness AI Trading Bot API")
    print("=" * 60)
    print()
    print("Starting server on http://localhost:8000")
    print()
    print("API Docs: http://localhost:8000/docs")
    print("ReDoc:    http://localhost:8000/redoc")
    print("Health:   http://localhost:8000/health")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
