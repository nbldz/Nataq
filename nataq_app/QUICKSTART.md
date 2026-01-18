# Nataq - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites (Download First)
1. **Python 3.10**: https://www.python.org/downloads/release/python-31011/
2. **FFmpeg**: https://www.gyan.dev/ffmpeg/builds/ (or `choco install ffmpeg`)
3. **NVIDIA Drivers**: Latest from nvidia.com

---

## Installation (Copy-Paste Commands)

```bash
# 1. Open Command Prompt in project folder
cd path\to\nataq_app

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
venv\Scripts\activate

# 4. Install PyTorch with CUDA 11.8 (MUST BE FIRST!)
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118

# 5. Install all dependencies
pip install -r requirements.txt

# 6. Set environment variable
setx COQUI_TOS_AGREED "1"

# 7. Test installation
python test_installation.py

# 8. Run application
python main.py
```

**OR use automated installer:**
```bash
install.bat
```

---

## First Run

1. **Launch application**:
   - Double-click `run_nataq.bat`, OR
   - Run: `python main.py`

2. **Select a test video**:
   - Click "📹 Select Video"
   - Choose a 30-second video

3. **Configure**:
   - Source: English
   - Target: Arabic
   - Dialect: MSA
   - Model: Medium

4. **Process**:
   - Click "🚀 Start Dubbing"
   - Wait 1-2 minutes
   - Preview result!

---

## Troubleshooting

### "CUDA not available"
```bash
# Check GPU
nvidia-smi

# Reinstall PyTorch
pip uninstall torch torchvision torchaudio
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118
```

### "FFmpeg not found"
```bash
# Verify FFmpeg
ffmpeg -version

# If not found, download and add to PATH
# Or: choco install ffmpeg
```

### Application won't start
```bash
# Test Python version (MUST be 3.10)
python --version

# Run test script
python test_installation.py
```

---

## Building Executable

```bash
# Activate environment
venv\Scripts\activate

# Build
pyinstaller nataq.spec

# Output: dist\Nataq\Nataq.exe
```

---

## File Locations

- **Input Videos**: Anywhere you choose
- **Output Videos**: `nataq_app/output/`
- **Temp Files**: `nataq_app/temp/` (auto-cleaned)
- **Models**: `~/.cache/huggingface/` (~5-7GB)

---

## Common Use Cases

### English → Arabic (MSA)
Perfect for educational content, news, formal presentations

### English → Arabic (Egyptian)
Great for entertainment, movies, casual content

### Arabic → English
Educational content, business presentations

### With Voice Cloning
1. Record 10 seconds of target voice
2. Click "🎤 Select Audio"
3. Choose the recording
4. Process as normal

---

## Performance Tips

**For fastest processing:**
- Use "base" Whisper model
- Close other GPU apps
- Use SSD for temp files

**For best quality:**
- Use "large" Whisper model
- Provide reference audio
- Use 1080p source video

---

## Getting Help

1. Check `USER_GUIDE.md` for detailed instructions
2. Run `python test_installation.py`
3. Check logs in progress window
4. See `INSTALLATION.md` for common issues

---

## What's Included

✅ Production-ready Windows application  
✅ GPU-accelerated processing  
✅ 4 Arabic dialects supported  
✅ Voice cloning capability  
✅ Bilingual UI (English/Arabic)  
✅ Complete documentation  
✅ Test scripts  
✅ Build tools for .exe  

---

## Award Submission

This project is submitted for:
**Sharjah International Award for AI in Serving the Arabic Language**

See `AWARD_SUBMISSION.md` for full details.

---

## Next Steps

1. ✅ Install and test
2. ✅ Process a sample video
3. ✅ Try different dialects
4. ✅ Test voice cloning
5. ✅ Build executable
6. ✅ Prepare demo materials
7. ✅ Submit for award!

---

**Questions?** Check the comprehensive guides:
- `README.md` - Project overview
- `INSTALLATION.md` - Detailed setup
- `USER_GUIDE.md` - Complete manual
- `PROJECT_STRUCTURE.md` - Code organization

**Ready to start!** 🎬🌍🗣️
