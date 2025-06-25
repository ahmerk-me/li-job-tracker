@echo off
echo LinkedIn Job Tracker
echo ===================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip show requests >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Check if config exists
if not exist config.json (
    echo Configuration file not found.
    echo Running setup...
    python setup.py
    if errorlevel 1 (
        echo Setup failed. Please run setup.py manually.
        pause
        exit /b 1
    )
)

echo.
echo Choose an option:
echo 1. Run once (check for new jobs now)
echo 2. Run continuously (check every 30 minutes)
echo 3. Test configuration
echo 4. Exit

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Running job tracker once...
    python linkedin_job_tracker.py
) else if "%choice%"=="2" (
    echo Running job tracker continuously...
    echo Press Ctrl+C to stop
    python linkedin_job_tracker.py --continuous
) else if "%choice%"=="3" (
    echo Testing configuration...
    python test_tracker.py
) else if "%choice%"=="4" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please run the script again.
)

echo.
pause 