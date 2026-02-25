@echo off
REM Windows Setup Script for Backend

echo Setting up Exness AI Trading Bot Backend...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Python found
echo.

REM Create virtual environment
if not exist venv (
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error creating virtual environment
        pause
        exit /b 1
    )
) else (
    echo [2/4] Virtual environment already exists
)

REM Activate venv
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [4/4] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup complete!
echo.
echo To run the server:
echo   1. Open PowerShell
echo   2. Run: .\venv\Scripts\Activate.ps1
echo   3. Run: python app/main.py
echo.
echo API will be available at: http://localhost:8000
echo Docs: http://localhost:8000/docs
echo ============================================
pause
