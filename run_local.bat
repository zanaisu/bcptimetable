@echo off
:: Clear error logs at the start of each run
echo Setting up environment... > errorlogs.txt
echo. >> errorlogs.txt

:: Create a log file header
echo Logs from run on %date% at %time% > errorlogs.txt
echo ------------------------------------------------- >> errorlogs.txt
echo. >> errorlogs.txt

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv 2>> errorlogs.txt
    if %errorlevel% neq 0 (
        echo Error creating virtual environment! See errorlogs.txt for details.
        pause
        exit /b %errorlevel%
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate 2>> errorlogs.txt
if %errorlevel% neq 0 (
    echo Error activating virtual environment! See errorlogs.txt for details.
    pause
    exit /b %errorlevel%
)

:: Clean virtual environment and reinstall
echo Cleaning up previous installation...
pip uninstall -y Flask Flask-SQLAlchemy Flask-Login Flask-Migrate Flask-WTF SQLAlchemy 2>> errorlogs.txt

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt 2>> errorlogs.txt
if %errorlevel% neq 0 (
    echo Warning: Some requirements failed to install. Will try to continue anyway...
)

:: Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env 2>> errorlogs.txt
    if %errorlevel% neq 0 (
        echo Error creating .env file! See errorlogs.txt for details.
        pause
        exit /b %errorlevel%
    )
)

:: Initialize database directory if it doesn't exist
if not exist instance (
    echo Creating instance directory...
    mkdir instance 2>> errorlogs.txt
)

:: Clean up any database files and create a clean instance directory
echo Running database cleanup script...
python db_debug.py > errorlogs.txt 2>&1 < NUL
echo y >> errorlogs.txt
if %errorlevel% neq 0 (
    echo Error cleaning up database files! See errorlogs.txt for details.
    echo Will try to continue with the rest of the setup...
)

:: Create a simplified database initialization script
echo Creating database initialization script...
echo import os >> create_db.py
echo from app import create_app, db >> create_db.py
echo from app.models.user import User >> create_db.py
echo from app.models.task import Task >> create_db.py
echo from app.models.subject import Subject >> create_db.py
echo from app.models.topic import Topic, TopicConfidence, SubtopicConfidence >> create_db.py
echo app = create_app() >> create_db.py
echo print(f"Using instance path: {app.instance_path}") >> create_db.py
echo with app.app_context(): >> create_db.py
echo     db.create_all() >> create_db.py
echo     print(f"Database created at: {app.config['SQLALCHEMY_DATABASE_URI']}") >> create_db.py

echo Initializing database...
python create_db.py >> errorlogs.txt 2>&1
if %errorlevel% neq 0 (
    echo Error creating database! See errorlogs.txt for details.
    echo Will try to continue with the rest of the setup...
)

:: Create a simplified curriculum loading script
echo Creating curriculum loading script...
echo from app import create_app >> load_curriculum.py
echo from app.init_db import init_db >> load_curriculum.py
echo app = create_app() >> load_curriculum.py
echo with app.app_context(): >> load_curriculum.py
echo     init_db() >> load_curriculum.py
echo     print("Curriculum data loaded successfully") >> load_curriculum.py

:: Load curriculum data
echo Loading curriculum data...
python load_curriculum.py >> errorlogs.txt 2>&1
if %errorlevel% neq 0 (
    echo Error loading curriculum data! See errorlogs.txt for details.
    echo Will try to continue with the rest of the setup...
)

:: Clean up temporary files
del create_db.py
del load_curriculum.py

:: Run the application
echo Starting application...
echo.
echo ----------------------------------------------
echo    A-Level Study Tracker is starting up!
echo ----------------------------------------------
echo.
echo The application will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when done.
echo.

python -m flask run 2>> errorlogs.txt

:: Deactivate environment when the app stops
call venv\Scripts\deactivate

:: Pause to keep the window open
echo.
echo Application has stopped. Press any key to exit...
pause > nul