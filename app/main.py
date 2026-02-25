from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import get_settings
from app.core.database import init_db, close_db
from app.routes import auth, account, trades, signals

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting up FastAPI application")
    await init_db()
    
    yield
    
    # Shutdown
    logger.info("Shutting down FastAPI application")
    await close_db()


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="AI-Powered Trading Bot API",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(account.router)
app.include_router(trades.router)
app.include_router(signals.router)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Exness AI Trading Bot API",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.API_VERSION,
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level="info",
    )
