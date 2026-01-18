@echo off
REM Quick Voice Converter for Nataq Pre-trained Voices
REM Uses FFmpeg directly (no Python dependencies)

echo ========================================
echo Nataq - Quick Voice Converter
echo ========================================
echo.

REM Check FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: FFmpeg not found!
    echo Please install: choco install ffmpeg
    pause
    exit /b 1
)

REM Create voices directory
if not exist voices mkdir voices

echo Available voice slots:
echo   1. Arabic Male   - voices\male_arabic.wav
echo   2. Arabic Female - voices\female_arabic.wav
echo   3. English Male  - voices\male_english.wav
echo   4. English Female - voices\female_english.wav
echo.

set /p SLOT="Select slot (1-4): "

if "%SLOT%"=="1" set OUTPUT=voices\male_arabic.wav
if "%SLOT%"=="2" set OUTPUT=voices\female_arabic.wav
if "%SLOT%"=="3" set OUTPUT=voices\male_english.wav
if "%SLOT%"=="4" set OUTPUT=voices\female_english.wav

if "%OUTPUT%"=="" (
    echo Invalid selection
    pause
    exit /b 1
)

echo.
echo Drag and drop your audio file here, then press Enter:
set /p INPUT=

REM Remove quotes
set INPUT=%INPUT:"=%

if not exist "%INPUT%" (
    echo File not found: %INPUT%
    pause
    exit /b 1
)

echo.
echo Converting %INPUT%
echo to %OUTPUT%...
echo.

REM Convert using FFmpeg
ffmpeg -i "%INPUT%" -ar 22050 -ac 1 -t 30 -acodec pcm_s16le -y "%OUTPUT%"

if errorlevel 1 (
    echo.
    echo Conversion failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Success!
echo ========================================
echo.
echo Voice file created: %OUTPUT%
echo.
echo Created voices:
if exist voices\male_arabic.wav echo   [X] Arabic Male
if exist voices\female_arabic.wav echo   [X] Arabic Female
if exist voices\male_english.wav echo   [X] English Male
if exist voices\female_english.wav echo   [X] English Female
echo.
echo To use in Nataq:
echo   1. Run: python main.py
echo   2. Select "Use Pre-trained Voice"
echo   3. Choose voice from dropdown
echo   4. Process video!
echo.

pause
