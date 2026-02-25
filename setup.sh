#!/bin/bash
# Setup script for Linux/Mac

echo "Setting up Exness AI Trading Bot Backend..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org"
    exit 1
fi

echo "[1/4] Python found: $(python3 --version)"
echo ""

# Create virtual environment
if [ ! -d venv ]; then
    echo "[2/4] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment"
        exit 1
    fi
else
    echo "[2/4] Virtual environment already exists"
fi

# Activate venv
echo "[3/4] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[4/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

echo ""
echo "============================================"
echo "Setup complete!"
echo ""
echo "To run the server:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run: python app/main.py"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo "============================================"
