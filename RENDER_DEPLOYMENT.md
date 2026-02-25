# Render.com Deployment Guide

## Prerequisites
- GitHub account (free at https://github.com)
- Render account (free at https://render.com)

## Step 1: Push Code to GitHub

### 1.1 Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `forex-bot-backend`
3. Choose Public or Private
4. Click "Create repository"

### 1.2 Initialize Git & Push
```bash
cd c:\Users\Farouq Baba\Documents\forex-bot\backend

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: FastAPI trading bot backend"

# Add remote (replace USERNAME and REPO)
git remote add origin https://github.com/USERNAME/forex-bot-backend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 1.3 Verify on GitHub
- Go to https://github.com/USERNAME/forex-bot-backend
- Verify all files are uploaded

---

## Step 2: Deploy on Render

### 2.1 Connect GitHub to Render
1. Go to https://render.com
2. Sign up / Sign in with GitHub
3. Click "Authorize render-oss"

### 2.2 Create Web Service
1. Click "New +" button → "Web Service"
2. Select your `forex-bot-backend` repository
3. Fill in the form:

   | Field | Value |
   |-------|-------|
   | Name | `forex-bot-api` |
   | Environment | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
   | Instance Type | Free |

4. Click "Create Web Service"

### 2.3 Wait for Deployment
- Render will deploy automatically
- Once green ✅, you'll get a URL like:
  ```
  https://forex-bot-api.onrender.com
  ```
- Copy this URL (**you'll need it for Flutter**)

---

## Step 3: Update Flutter App

Edit `lib/services/api_service.dart`:
```dart
static const String _baseUrl = 'https://forex-bot-api.onrender.com';
```

---

## Step 4: Test the Deployment

### Test via Browser
```
https://forex-bot-api.onrender.com/docs
```

### Test via Flutter
```bash
cd c:\Users\Farouq Baba\Documents\forex-bot\forex_bot
flutter run
```

---

## Important Notes

- **Free tier performance**: App may sleep after 15 minutes of inactivity
- **Database**: Currently using SQLite (file-based). For production, add PostgreSQL:
  1. In Render dashboard, create PostgreSQL database
  2. Copy connection string
  3. Update `.env` with `DATABASE_URL`

- **Environment Variables**: In Render dashboard → Settings → Environment
  ```
  SECRET_KEY=your-super-secret-key-change-this
  DATABASE_URL=postgresql://...
  EXNESS_LOGIN=your_login
  EXNESS_PASSWORD=your_password
  ```

- **Auto-deploy**: Every git push to `main` automatically redeploys

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "502 Bad Gateway" | App is still starting, wait 2 min |
| "404 Not Found" | Wrong URL or endpoint |
| "Deployment failed" | Check build logs in Render dashboard |
| "Free tier sleeping" | Upgrade to paid plan or add cron job to keep alive |

