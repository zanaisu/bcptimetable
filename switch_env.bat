@echo off
echo BCP Timetable Environment Switcher
echo ================================
echo.
echo This script helps you switch between local development and Railway deployment environments.
echo.

if "%1"=="local" (
    echo Switching to local development environment...
    copy /Y .env.local .env
    echo Environment switched to local development.
    exit /b 0
)

if "%1"=="railway" (
    echo Switching to Railway deployment environment...
    copy /Y .env.railway .env
    echo Environment switched to Railway deployment.
    exit /b 0
)

echo Usage:
echo   switch_env.bat local   - Switch to local development environment
echo   switch_env.bat railway - Switch to Railway deployment environment
echo.
echo First, make sure you have both .env.local and .env.railway files.
echo If you don't have .env.local, rename your current .env file to .env.local.
echo.

if exist .env (
    echo Current .env file detected. Backing it up as .env.backup...
    copy /Y .env .env.backup
    echo Backup created as .env.backup
)

if not exist .env.local (
    if exist .env (
        echo Creating .env.local from current .env file...
        copy /Y .env .env.local
        echo Created .env.local
    ) else (
        echo No .env file found. Creating a default .env.local for local development...
        echo # Local Development Configuration > .env.local
        echo FLASK_APP=run.py >> .env.local
        echo FLASK_DEBUG=1 >> .env.local
        echo SECRET_KEY=dev-key-for-testing >> .env.local
        echo DATABASE_URL=sqlite:///timetable.db >> .env.local
        echo Created default .env.local
    )
)

echo.
echo Setup complete. Now you can use:
echo   switch_env.bat local   - to switch to local development
echo   switch_env.bat railway - to switch to Railway deployment
