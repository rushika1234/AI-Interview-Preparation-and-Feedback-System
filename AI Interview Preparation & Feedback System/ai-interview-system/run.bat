@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting AI Interview System...
echo Open your browser at: http://localhost:5000
echo.
python app.py
pause
