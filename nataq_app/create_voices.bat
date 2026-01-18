@echo off
REM Nataq - Voice Pre-training Launcher
REM Run this ONCE to generate pre-trained voices

echo ========================================
echo Nataq - Voice Pre-training
echo ========================================
echo.

REM Activate virtual environment
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found!
    echo Please run install_fixed.bat first
    pause
    exit /b 1
)

REM Run voice creation script
echo.
echo Running voice generation script...
echo.
python create_voices.py

REM Keep window open
echo.
pause
