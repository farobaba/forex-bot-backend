# Python Backend for Exness AI Trading Bot

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- PostgreSQL database
- Exness trading account (demo or live)

### Installation

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Initialize database**
```bash
# The database is initialized automatically on app startup
```

### Running the Server

```bash
python app/main.py
```

Or with uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- ReDoc Documentation: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/logout` - Logout user
- `GET /auth/me` - Get current user info

### Account
- `GET /account/info` - Get account information
- `POST /account/update` - Update account info

### Trades
- `GET /trades/active` - Get active trades
- `GET /trades/history` - Get trade history
- `POST /trades/open` - Open new trade
- `POST /trades/close/{trade_id}` - Close trade
- `PUT /trades/update/{trade_id}` - Update trade

### Signals
- `GET /signals/latest` - Get latest signal
- `GET /signals/feed` - Get signal feed
- `GET /signals/history` - Get signal history

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── database.py        # Database connection
│   ├── models/
│   │   ├── database.py        # SQLAlchemy models
│   │   └── schemas.py         # Pydantic schemas
│   ├── routes/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── account.py         # Account endpoints
│   │   ├── trades.py          # Trades endpoints
│   │   └── signals.py         # Signals endpoints
│   ├── services/
│   │   ├── mt5_connector.py   # MT5 WebSocket connector
│   │   └── signal_generator.py # AI signal generator
│   └── main.py                # FastAPI application
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## Database Models

### User
- id, email, hashed_password, exness_login, exness_api_key, is_active, created_at, last_login

### Account
- id, user_id, balance, equity, free_margin, margin_used, margin_level, open_trades_count, daily_profit

### Trade
- id, user_id, symbol, direction, status, entry_price, current_price, exit_price, stop_loss, take_profit, volume, pnl, pnl_percentage, opened_at, closed_at

### Signal
- id, user_id, symbol, signal_type, confidence, entry_price, stop_loss, take_profit, indicators_data, is_valid, created_at

## Configuration

Key settings in `.env`:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key (change in production!)
- `EXNESS_LOGIN` - Your Exness account login
- `EXNESS_PASSWORD` - Your Exness account password
- `TARGET_SYMBOL` - Trading symbol (default: XAUUSD)
- `TARGET_TIMEFRAME` - Candle timeframe in minutes (default: 5)
- `RISK_PER_TRADE` - Risk percentage per trade (default: 2%)
- `SIGNAL_CONFIDENCE_THRESHOLD` - Minimum confidence for signal (default: 70)

## Integration with Flutter App

The Flutter frontend connects to this backend API:
- Base URL: `http://localhost:8000` or your server address
- All endpoints require JWT authentication (except /auth/register and /auth/login)
- Token is sent in `Authorization: Bearer <token>` header

## Next Steps

1. **Database Setup**
   - Install and configure PostgreSQL
   - Update DATABASE_URL in .env

2. **MT5 Integration**
   - Update EXNESS_LOGIN, EXNESS_PASSWORD in .env
   - Implement real MT5 WebSocket connection in `mt5_connector.py`

3. **Model Training**
   - Prepare historical XAUUSD data
   - Train TensorFlow model for signal generation
   - Integrate model in `signal_generator.py`

4. **Deployment**
   - Set up environment variables on server
   - Deploy to VPS or cloud platform
   - Configure SSL certificate
   - Set DEBUG=False in production

## Development Notes

- Use PostgreSQL for production (SQLite for development)
- Always change SECRET_KEY before deploying
- Monitor API logs for errors
- Test JWT token expiration handling
- Implement proper error handling for MT5 connection failures
