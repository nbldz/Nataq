@echo off
REM Nataq Application - Build Executable Script

echo ========================================
echo Nataq - Build Executable
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo.

REM Build executable using PyInstaller
echo Building executable...
echo This will take 10-20 minutes...
echo.
pyinstaller nataq.spec

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.

if exist dist\Nataq\Nataq.exe (
    echo SUCCESS: Executable created!
    echo Location: dist\Nataq\Nataq.exe
    echo.
    echo To distribute:
    echo   1. Copy the entire "dist\Nataq" folder
    echo   2. Include FFmpeg binaries
    echo   3. Add README.txt with instructions
    echo.
) else (
    echo ERROR: Build failed!
    echo Check build\Nataq\warn-*.txt for details
    echo.
)

pause
