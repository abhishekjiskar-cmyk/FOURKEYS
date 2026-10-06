@echo off
REM Multi-Agent Gemma System - Setup Script for Windows

echo ==================================
echo Multi-Agent Gemma System Setup
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Copy environment file
if not exist .env (
    echo.
    echo Creating .env file...
    copy .env.example .env
    echo WARNING: Please edit .env and add your API keys
) else (
    echo.
    echo .env file already exists
)

REM Create results directory
if not exist results mkdir results

echo.
echo ==================================
echo Setup complete!
echo ==================================
echo.
echo Next steps:
echo 1. Edit .env and add your GOOGLE_API_KEY or HF_TOKEN
echo 2. Run the web interface: streamlit run app.py
echo 3. Or run evaluation: python evaluation.py
echo.
pause
