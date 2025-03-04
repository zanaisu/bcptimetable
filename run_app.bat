@echo off

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

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

python -m flask run

:: Deactivate environment when the app stops
call venv\Scripts\deactivate

:: Pause to keep the window open
echo.
echo Application has stopped. Press any key to exit...
pause