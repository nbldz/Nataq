@echo off
REM Nataq Application - FIXED Windows Installation Script
REM This version handles Conda/Miniconda conflicts

echo ========================================
echo Nataq Installation Script (FIXED)
echo ========================================
echo.

REM IMPORTANT: Deactivate Conda if active
echo [0/8] Checking for Conda environment...
conda deactivate 2>nul
echo Conda deactivated (if it was active)
echo.

REM Check Python version
echo [1/8] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo.
    echo CRITICAL: You have Miniconda installed but need pure Python 3.10
    echo.
    echo Please install Python 3.10 from: https://www.python.org/downloads/release/python-31011/
    echo Make sure to CHECK "Add Python to PATH" during installation
    echo.
    echo After installing, open a NEW command prompt and run this script again.
    pause
    exit /b 1
)

python --version
echo.

REM Important warning about Conda
echo WARNING: Miniconda detected in your system
echo For this application to work, you MUST use pure Python, not Conda Python
echo.
echo Verify you're using the right Python:
python -c "import sys; print('Python location:', sys.executable)"
echo.
echo If the path above shows 'miniconda' or 'conda', you need to:
echo 1. Install Python 3.10 from python.org
echo 2. Make sure it's FIRST in your PATH (before Conda)
echo 3. Open a NEW command prompt
echo 4. Run this script again
echo.
pause

REM Check FFmpeg
echo [2/8] Checking FFmpeg installation...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg not found!
    echo Please install FFmpeg:
    echo   Option 1: choco install ffmpeg
    echo   Option 2: Download from https://www.gyan.dev/ffmpeg/builds/
    pause
)
echo FFmpeg: OK
echo.

REM Remove old venv if exists
if exist venv (
    echo [3/8] Removing old virtual environment...
    rmdir /s /q venv
)

REM Create virtual environment with pure Python
echo [4/8] Creating virtual environment with pure Python...
python -m venv venv --clear
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment!
    echo This usually means you're using Conda's Python.
    echo Please install pure Python 3.10 from python.org
    pause
    exit /b 1
)
echo Virtual environment created.
echo.

REM Activate virtual environment
echo [5/8] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo [6/8] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install PyTorch with CUDA (latest available)
echo [7/8] Installing PyTorch with CUDA 11.8...
echo This may take several minutes...
echo Installing latest PyTorch for CUDA 11.8...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
echo.

REM Install dependencies
echo [8/8] Installing application dependencies...
echo This may take 10-15 minutes...
pip install --no-cache-dir -r requirements.txt
echo.

REM Set environment variables
echo Setting environment variables...
set COQUI_TOS_AGREED=1
echo.

REM Verify installation
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Verifying PyTorch + CUDA...
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
echo.

echo ========================================
echo Ready to use!
echo ========================================
echo.
echo To run Nataq:
echo   1. Double-click: run_nataq.bat
echo   OR
echo   2. In command prompt:
echo      venv\Scripts\activate
echo      python main.py
echo.

pause
