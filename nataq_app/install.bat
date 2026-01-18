@echo off
REM Nataq Application - Windows Installation Script
REM Run this script to set up the application

echo ========================================
echo Nataq Installation Script
echo ========================================
echo.

REM Check Python version
echo [1/7] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.10 from https://www.python.org/
    pause
    exit /b 1
)

python --version
echo.

REM Check FFmpeg
echo [2/7] Checking FFmpeg installation...
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

REM Create virtual environment
echo [3/7] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created.
)
echo.

REM Activate virtual environment
echo [4/7] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install PyTorch with CUDA
echo [5/7] Installing PyTorch with CUDA 11.8...
echo This may take several minutes...
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118
echo.

REM Install dependencies
echo [6/7] Installing application dependencies...
echo This may take 10-15 minutes...
pip install -r requirements.txt
echo.

REM Set environment variables
echo [7/7] Setting environment variables...
setx COQUI_TOS_AGREED "1"
echo.

REM Verify installation
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Verifying PyTorch + CUDA...
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
echo.

echo ========================================
echo Ready to use!
echo ========================================
echo.
echo To run Nataq:
echo   1. Open command prompt
echo   2. Navigate to this folder
echo   3. Run: venv\Scripts\activate
echo   4. Run: python main.py
echo.
echo Or simply double-click: run_nataq.bat
echo.

pause
