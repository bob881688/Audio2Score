@echo off
echo ========================================
echo Audio2Score Backend - Quick Start
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.10 or higher from python.org
    pause
    exit /b 1
)
echo.

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo ========================================
echo Starting FastAPI server...
echo ========================================
echo API will be available at:
echo   - Main: http://localhost:8000
echo   - Docs: http://localhost:8000/docs
echo ========================================
echo.

uvicorn main:app --reload --port 8000
