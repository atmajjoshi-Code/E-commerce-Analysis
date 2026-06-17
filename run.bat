@echo off
echo ============================================
echo   E-Commerce Analytics Dashboard
echo ============================================
echo.
echo [1] Installing required libraries...
pip install -r requirements.txt
echo.
echo [2] Starting dashboard...
echo     Open browser at: http://127.0.0.1:8050
echo     Press Ctrl+C to stop
echo.
python app.py
pause
