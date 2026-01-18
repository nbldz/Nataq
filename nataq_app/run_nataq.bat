@echo off
REM Nataq Application - Quick Launch Script

echo Starting Nataq...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run application
python main.py

REM Keep window open if error occurs
if errorlevel 1 pause
