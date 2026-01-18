# CRITICAL FIX - Installation for Users with Miniconda/Anaconda

## 🚨 Problem Identified

You have **Miniconda installed**, which is causing conflicts with pip installations. This is one of the exact scenarios I warned about in the original documentation.

## ✅ Solution: Use Pure Python 3.10

You have **TWO options**:

---

## Option 1: Install Pure Python 3.10 (RECOMMENDED)

### Step 1: Download Python 3.10
1. Go to: https://www.python.org/downloads/release/python-31011/
2. Download: **Windows installer (64-bit)**
3. Run the installer

### Step 2: CRITICAL - Installation Settings
- ✅ **CHECK** "Add Python 3.10 to PATH"
- ✅ **CHECK** "Install for all users" (optional)
- Click "Install Now"

### Step 3: Verify Installation
Open a **NEW** Command Prompt and run:
```bash
python --version
# Should show: Python 3.10.11

# Check it's NOT conda:
python -c "import sys; print(sys.executable)"
# Should show: C:\Users\...\Python310\python.exe
# Should NOT show: miniconda or conda
```

### Step 4: Fix PATH Order
If it still shows Miniconda Python:

1. Press `Win + X` → System
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", find `Path`
5. Click "Edit"
6. **Move Python 3.10 ABOVE Miniconda paths**:
   ```
   C:\Users\YourName\AppData\Local\Programs\Python\Python310\
   C:\Users\YourName\AppData\Local\Programs\Python\Python310\Scripts\
   ```
7. Click OK on everything
8. **Open NEW command prompt**

### Step 5: Install Nataq
```bash
cd path\to\nataq_app
install_fixed.bat
```

---

## Option 2: Use Conda Environment (Alternative)

If you want to keep using Conda:

### Step 1: Create Clean Conda Environment
```bash
# Deactivate current environment
conda deactivate

# Create new environment with Python 3.10
conda create -n nataq python=3.10 -y

# Activate it
conda activate nataq
```

### Step 2: Install PyTorch via Conda
```bash
# Install PyTorch with CUDA 11.8
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
```

### Step 3: Install Other Dependencies
```bash
cd nataq_app

# Install with pip (in conda env)
pip install --no-deps openai-whisper
pip install transformers sentencepiece protobuf sacremoses
pip install TTS pydub librosa soundfile
pip install PyQt5
pip install ffmpeg-python tqdm requests colorama
pip install python-dotenv pyyaml
```

### Step 4: Set Environment Variable
```bash
set COQUI_TOS_AGREED=1
```

### Step 5: Run Application
```bash
python main.py
```

---

## 🔍 Verify Which Python You're Using

Run this to check:
```bash
python -c "import sys; print('Executable:', sys.executable); print('Version:', sys.version)"
```

**Good output (Pure Python):**
```
Executable: C:\Users\Nobel\AppData\Local\Programs\Python\Python310\python.exe
Version: 3.10.11 (main, ...)
```

**Bad output (Conda Python):**
```
Executable: C:\sharjah\miniconda\python.exe
Version: 3.10.x |Anaconda, Inc.| (main, ...)
```

---

## 🛠️ Troubleshooting Specific Errors

### Error: "KeyError: '__version__'"
**Cause:** Conda's pip trying to build packages from source  
**Solution:** Use Pure Python 3.10 (Option 1 above)

### Error: "torch==2.2.0 not found"
**Cause:** PyTorch changed their versioning  
**Solution:** Install latest: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

### Error: "venv could not be loaded"
**Cause:** Running in PowerShell with execution policy restrictions  
**Solution:** 
```powershell
# Run as Administrator:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use Command Prompt instead of PowerShell
```

### Error: "Getting requirements to build wheel"
**Cause:** Conda's setuptools conflicts with pip  
**Solution:** Use Pure Python (not conda)

---

## 📋 Quick Fix Checklist

- [ ] Install Python 3.10 from python.org
- [ ] Verify it's not conda: `python -c "import sys; print(sys.executable)"`
- [ ] Ensure Python 3.10 is FIRST in PATH
- [ ] Open **NEW** command prompt
- [ ] Run `install_fixed.bat`
- [ ] If errors, use Option 2 (Conda environment)

---

## 🎯 Recommended: Complete Fresh Install

**Best approach for clean installation:**

```bash
# 1. Download Python 3.10.11 from python.org
# 2. Install with "Add to PATH" checked
# 3. Open NEW Command Prompt
# 4. Navigate to project:
cd C:\path\to\nataq_app

# 5. Create virtual environment:
python -m venv venv

# 6. Activate (Command Prompt):
venv\Scripts\activate

# 7. Upgrade pip:
python -m pip install --upgrade pip

# 8. Install PyTorch FIRST:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 9. Verify CUDA:
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True

# 10. Install dependencies:
pip install -r requirements.txt

# 11. Set environment:
set COQUI_TOS_AGREED=1

# 12. Test:
python test_installation.py

# 13. Run:
python main.py
```

---

## 💡 Why This Happens

**Conda vs Pip Conflicts:**
- Conda has its own package manager
- Mixing conda and pip causes dependency conflicts
- Some packages try to build from source in conda
- Build tools aren't always available in conda environments

**Solution:**
- Use **pure Python** for pip-based projects
- OR use **pure conda** for conda-based projects
- **DON'T MIX** both in the same project

---

## ✅ After Successful Installation

Once installed, run:
```bash
python test_installation.py
```

You should see all ✓ marks:
```
✓ Python 3.10.x
✓ PyTorch version: 2.x.x+cu118
✓ CUDA available: True
✓ GPU: NVIDIA GeForce RTX Titan
✓ Whisper installed
✓ Transformers installed
✓ TTS installed
✓ PyQt5 installed
✓ FFmpeg: ffmpeg version ...
```

Then you can run:
```bash
python main.py
```

---

## 📞 Still Having Issues?

If you continue to have problems:

1. **Share your output** from:
   ```bash
   python -c "import sys; print(sys.executable, sys.version)"
   where python
   ```

2. **Check if conda is active**:
   ```bash
   conda info
   ```

3. **Try the Conda Option 2** above if Pure Python doesn't work

---

**The key is: Pure Python 3.10 from python.org, NOT Miniconda's Python!**
