@echo off
REM Scholarship Master Quick Start Script (Windows)

echo ==================================
echo Scholarship Master - Quick Start
echo ==================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo + %PYTHON_VERSION% found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo + Virtual environment created
) else (
    echo + Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo + Virtual environment activated
echo.

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
echo + Dependencies installed
echo.

REM Check for .env file
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo - .env file created. Please edit it with your configuration:
    echo   - GOOGLE_DRIVE_FOLDER_ID
    echo   - GOOGLE_SERVICE_ACCOUNT_JSON
    echo   - OPENAI_API_KEY (optional)
    echo.
    pause
)

echo.
echo + Setup complete!
echo.
echo Next steps:
echo 1. Configure your .env file with Google Drive and OpenAI credentials
echo 2. Set up your Google Drive folder structure
echo 3. Run the workflow: python main.py
echo 4. Generate reports: python cli.py report summary
echo.
pause
