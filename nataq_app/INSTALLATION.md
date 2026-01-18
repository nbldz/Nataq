# Nataq (نطق) - Installation Guide
## AI Video Dubbing Application for Windows 11

### System Requirements

**Hardware:**
- NVIDIA GPU with CUDA support (RTX Titan, RTX 3090, etc.)
- Minimum 16GB RAM (24GB recommended)
- 20GB free disk space
- Windows 11 (tested) or Windows 10

**Software:**
- Python 3.10 (MUST be 3.10, not 3.11 or 3.12)
- FFmpeg installed and in PATH
- NVIDIA GPU drivers (latest)
- CUDA 11.8 compatible driver

---

## Installation Steps

### Step 1: Install Python 3.10

1. Download Python 3.10.11 from: https://www.python.org/downloads/release/python-31011/
2. Run installer and **CHECK "Add Python to PATH"**
3. Verify installation:
```bash
python --version
# Should show: Python 3.10.11
```

### Step 2: Install FFmpeg

**Option A: Using Chocolatey (Recommended)**
```bash
# Install Chocolatey first if not installed
# Then:
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add to PATH: `C:\ffmpeg\bin`
4. Verify:
```bash
ffmpeg -version
```

### Step 3: Create Virtual Environment

```bash
# Navigate to project directory
cd path\to\nataq_app

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your prompt
```

### Step 4: Install PyTorch with CUDA 11.8

**CRITICAL: Install PyTorch FIRST before other packages**

```bash
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118
```

Verify PyTorch installation:
```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

You should see:
```
PyTorch: 2.2.0+cu118
CUDA Available: True
GPU: NVIDIA GeForce RTX Titan (or your GPU name)
```

### Step 5: Install Application Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- PyQt5 (GUI framework)
- openai-whisper (speech recognition)
- transformers (translation)
- TTS (Coqui XTTS v2)
- All required utilities

**Note:** Installation may take 10-15 minutes depending on internet speed.

### Step 6: Set Environment Variables

Create a `.env` file in the project root:

```bash
# .env file
COQUI_TOS_AGREED=1
CUDA_VISIBLE_DEVICES=0
```

Or set permanently in Windows:
```bash
setx COQUI_TOS_AGREED "1"
```

### Step 7: Download Required Models (First Run)

Models will auto-download on first use, but you can pre-download:

```bash
python -c "import whisper; whisper.load_model('medium')"
python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; AutoTokenizer.from_pretrained('facebook/nllb-200-distilled-600M'); AutoModelForSeq2SeqLM.from_pretrained('facebook/nllb-200-distilled-600M')"
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

Total download size: ~5-7GB

### Step 8: Test Installation

```bash
# Run the application
python main.py
```

The GUI should launch. Check the "Settings" tab to verify GPU is detected.

---

## Building Standalone Executable

### Method 1: Using PyInstaller (Recommended)

```bash
# Activate virtual environment
venv\Scripts\activate

# Build executable
pyinstaller nataq.spec

# Output will be in: dist\Nataq\
```

### Method 2: One-folder Bundle

```bash
pyinstaller --name Nataq --windowed --onedir main.py
```

### Method 3: One-file Bundle (Slower startup)

```bash
pyinstaller --name Nataq --windowed --onefile main.py
```

**Note:** Building .exe may take 10-20 minutes and produce 2-3GB executable folder.

---

## Distribution Package

To create a distributable package:

1. Build the executable (see above)
2. Copy the `dist\Nataq\` folder
3. Create installer folder structure:
```
Nataq_Installer\
├── Nataq\              (from dist\Nataq\)
├── FFmpeg\             (ffmpeg.exe, ffplay.exe, ffprobe.exe)
├── install.bat         (installation script)
├── README.txt          (user guide)
└── samples\            (sample videos/audio)
```

4. Create `install.bat`:
```batch
@echo off
echo Installing Nataq...
xcopy /E /I Nataq "C:\Program Files\Nataq"
xcopy /E /I FFmpeg "C:\Program Files\Nataq\FFmpeg"
setx PATH "%PATH%;C:\Program Files\Nataq\FFmpeg"
echo Installation complete!
echo Run Nataq from: C:\Program Files\Nataq\Nataq.exe
pause
```

---

## Troubleshooting

### Issue: "CUDA not available"
**Solution:**
- Verify NVIDIA drivers are latest
- Reinstall PyTorch with CUDA 11.8
- Check GPU with: `nvidia-smi`

### Issue: "FFmpeg not found"
**Solution:**
```bash
where ffmpeg
# Should show path to ffmpeg.exe
# If not, add FFmpeg to PATH
```

### Issue: "DLL load failed"
**Solution:**
- Install Visual C++ Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Restart computer

### Issue: "ModuleNotFoundError: TTS"
**Solution:**
```bash
pip uninstall TTS
pip install TTS==0.22.0
```

### Issue: Building .exe fails
**Solution:**
- Ensure all dependencies are installed in venv
- Try one-folder build instead of one-file
- Check PyInstaller logs in `build\Nataq\`

### Issue: Models download slowly
**Solution:**
- Models are large (5-7GB total)
- Use wired internet connection
- Download manually from Hugging Face:
  - https://huggingface.co/facebook/nllb-200-distilled-600M
  - https://huggingface.co/openai/whisper-medium

### Issue: Application crashes on startup
**Solution:**
1. Check Python version: `python --version` (must be 3.10)
2. Verify GPU drivers
3. Run from command line to see error messages
4. Check Windows Event Viewer for details

---

## Testing the Application

### Quick Test

1. Launch Nataq
2. Click "Select Video" and choose a short video (10-30 seconds)
3. Select languages (e.g., English → Arabic)
4. Click "Start Dubbing"
5. Wait for processing (1-5 minutes depending on video length)
6. Preview output

### Test Data

Create a test video:
1. Record yourself speaking for 10 seconds
2. Save as .mp4
3. Use as test input

Or download sample videos from:
- YouTube (short clips)
- Pexels Videos (free stock videos)

---

## Performance Optimization

### GPU Memory Management

For 24GB GPU (RTX Titan):
- Can process videos up to 5 minutes
- Use Whisper "medium" model
- Enable CUDA memory caching

For 12GB GPU:
- Use Whisper "base" model
- Process videos in chunks
- Reduce batch sizes

### Speed Improvements

1. Use SSD for temp files
2. Close other GPU applications
3. Use Whisper "base" for faster processing
4. Enable Windows Game Mode

---

## Uninstallation

```bash
# Remove virtual environment
rmdir /s venv

# Remove models cache
rmdir /s /q %USERPROFILE%\.cache\huggingface
rmdir /s /q %USERPROFILE%\.cache\whisper

# Delete application files
rmdir /s nataq_app
```

---

## Support

For issues or questions:
- Check logs in `nataq_app\logs\`
- Review error messages in progress window
- Verify system requirements
- Ensure all dependencies are correct versions

---

## Award Submission Checklist

- [ ] Application runs without errors
- [ ] GPU acceleration working
- [ ] All languages tested
- [ ] Arabic dialects working
- [ ] Voice cloning functional
- [ ] Professional UI/UX
- [ ] Demo video prepared
- [ ] Documentation complete
- [ ] Executable built and tested
- [ ] Sample outputs ready

---

**Author:** Nobel  
**Institution:** University of Sharjah  
**Award:** Sharjah International Award for AI in Serving the Arabic Language  
**Date:** December 2025
