#!/bin/bash
cd /Users/wsit5/.gemini/antigravity/scratch/maggie_kiosk/backend
echo "Starting Maggie Backend..."
# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
pip install reachy-mini || echo "reachy-mini install failed, but continuing..."
# Kill old instances just in case
pkill -f reachy-mini-daemon
pkill -f "python main.py"
echo "Starting Reachy USB Daemon..."
reachy-mini-daemon &
echo "Starting FastAPI Server..."
python main.py
