@echo off
echo ========================================
echo Microscope Control System
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure it.
    pause
    exit /b 1
)

echo.
echo Starting application...
echo.
echo Web Interface: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run the application
python backend\main.py

pause
