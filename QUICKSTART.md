# Quick Start Guide

## Windows Setup

### Step 1: Open PowerShell in backend folder
```
cd c:\Users\Farouq Baba\Documents\forex-bot\backend
```

### Step 2: Run setup script
```
.\setup.bat
```

### Step 3: Activate virtual environment (if not auto-activated)
```
.\venv\Scripts\Activate.ps1
```

### Step 4: Run the API server
```
python app/main.py
```

Server starts at: **http://localhost:8000**

---

## API Testing

Open browser to: http://localhost:8000/docs

### Test Endpoints:

1. **Register User**
```
POST /auth/register
{
  "email": "test@example.com",
  "password": "Test123!",
  "exness_login": "your_demo_login"
}
```

2. **Login**
```
POST /auth/login
{
  "email": "test@example.com",
  "password": "Test123!"
}
```
(Copy the access_token)

3. **Get Account Info**
```
GET /account/info
Header: Authorization: Bearer <access_token>
```

4. **Get Signals**
```
GET /signals/latest
Header: Authorization: Bearer <access_token>
```

---

## Database Setup (Optional - for persistence)

### Using SQLite (Default - No setup needed)
- Database is created automatically as `forex_bot.db`

### Using PostgreSQL (Production)
1. Install PostgreSQL
2. Create database: `forex_bot_db`
3. Update `.env`:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/forex_bot_db
   ```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "python command not found" | Install Python 3.10+ |
| "pip install fails" | Run as Administrator |
| "ModuleNotFoundError" | Make sure venv is activated |
| "Connection to DB failed" | Check DATABASE_URL in .env |
| "Port 8000 in use" | Change PORT in .env |

---

## Next Steps

1. ✅ Backend running
2. Update `lib/services/api_service.dart` in Flutter to point to backend URL
3. Run Flutter app
4. Test login/registration flow
