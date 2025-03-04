@echo off
echo Resetting database with new schema...

echo Checking if there's a backup folder...
if not exist "instance\backups" mkdir instance\backups

echo Creating backup of existing database...
if exist "instance\timetable.db" copy "instance\timetable.db" "instance\backups\timetable_%date:~-4,4%%date:~-7,2%%date:~-10,2%.db"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Creating new database with updated schema...
python run.py reset-db

echo Database reset complete!
pause