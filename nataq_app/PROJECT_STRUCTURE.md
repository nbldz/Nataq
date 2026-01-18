# Nataq Project Structure

```
nataq_app/
│
├── main.py                      # Application entry point
├── demo.py                      # CLI demo script
├── test_installation.py         # Installation verification
│
├── gui/                         # GUI components
│   ├── __init__.py
│   └── main_window.py          # Main application window (PyQt5)
│
├── core/                        # Core processing logic
│   ├── __init__.py
│   └── processor.py            # Video processing pipeline
│
├── utils/                       # Utility modules
│   ├── __init__.py
│   └── config.py               # Configuration and constants
│
├── models/                      # AI model cache (auto-created)
│   ├── whisper/
│   ├── nllb/
│   └── xtts/
│
├── temp/                        # Temporary files (auto-created)
│   ├── extracted_audio_*.wav
│   └── synthesized_*.wav
│
├── output/                      # Output videos (auto-created)
│   └── dubbed_*.mp4
│
├── assets/                      # Application assets (optional)
│   ├── icon.ico
│   └── logo.png
│
├── docs/                        # Documentation
│   ├── screenshots/
│   └── diagrams/
│
├── demo/                        # Demo materials
│   ├── sample_video.mp4
│   ├── sample_audio.wav
│   └── nataq_demo.mp4
│
├── venv/                        # Virtual environment
│   ├── Scripts/
│   ├── Lib/
│   └── Include/
│
├── requirements.txt             # Python dependencies
├── nataq.spec                   # PyInstaller specification
│
├── install.bat                  # Windows installation script
├── run_nataq.bat               # Quick launch script
├── build.bat                    # Build executable script
│
├── README.md                    # Project overview
├── INSTALLATION.md              # Installation guide
├── USER_GUIDE.md               # User manual
├── AWARD_SUBMISSION.md         # Award submission document
│
├── .gitignore                   # Git ignore rules
├── .env                         # Environment variables (create manually)
└── LICENSE                      # License file (optional)
```

## Directory Descriptions

### Root Level Files

- **main.py**: Application entry point, launches GUI
- **demo.py**: Command-line demo for testing pipeline
- **test_installation.py**: Verifies all dependencies installed correctly
- **requirements.txt**: All Python package dependencies
- **nataq.spec**: PyInstaller configuration for building .exe

### Core Directories

- **gui/**: All GUI-related code
  - Professional PyQt5 interface
  - Bilingual support (English/Arabic)
  - RTL text handling
  
- **core/**: Business logic and processing
  - Video processing pipeline
  - AI model integration
  - Audio/video synchronization
  
- **utils/**: Shared utilities
  - Configuration management
  - Constants and settings
  - Helper functions

### Auto-created Directories

- **models/**: AI model cache (~5-7GB)
  - Downloaded automatically on first use
  - Cached for faster subsequent runs
  
- **temp/**: Temporary processing files
  - Cleaned automatically after processing
  - Contains intermediate audio files
  
- **output/**: Final dubbed videos
  - Named with timestamp
  - Original videos not modified

### Documentation

- **README.md**: Project overview and quick start
- **INSTALLATION.md**: Step-by-step installation guide
- **USER_GUIDE.md**: Comprehensive user manual
- **AWARD_SUBMISSION.md**: Award submission document

### Scripts

- **install.bat**: Automated Windows installation
- **run_nataq.bat**: Quick launcher for application
- **build.bat**: Build standalone executable

## File Sizes

```
Component               Size
-----------------------------------------
Source Code             ~50 KB
Documentation          ~200 KB
Virtual Environment     ~2 GB
AI Models (cached)      ~5-7 GB
Built Executable        ~2-3 GB
```

## Workflow Diagram

```
User Input (Video)
        ↓
[GUI] Select Files & Configure
        ↓
[Core] VideoProcessor
        ↓
    ┌───┴───┐
    │Extract│ → temp/extracted_audio.wav
    │ Audio │
    └───┬───┘
        ↓
    ┌───┴───┐
    │Whisper│ → Transcription
    │  ASR  │
    └───┬───┘
        ↓
    ┌───┴───┐
    │NLLB   │ → Translation
    │ Trans │
    └───┬───┘
        ↓
    ┌───┴───┐
    │ XTTS  │ → temp/synthesized.wav
    │  TTS  │
    └───┬───┘
        ↓
    ┌───┴───┐
    │FFmpeg │ → output/dubbed_*.mp4
    │ Merge │
    └───┬───┘
        ↓
User Output (Dubbed Video)
```

## Dependencies Graph

```
main.py
  ├─> gui/main_window.py
  │     ├─> core/processor.py
  │     │     ├─> whisper
  │     │     ├─> transformers (NLLB)
  │     │     ├─> TTS (XTTS)
  │     │     └─> ffmpeg
  │     └─> utils/config.py
  │           └─> torch
  └─> utils/config.py
```

## Import Structure

```python
# main.py
from gui.main_window import NataqMainWindow
from utils.config import setup_environment

# gui/main_window.py
from core.processor import VideoProcessor
from utils.config import LANGUAGES, DIALECTS, etc.

# core/processor.py
import whisper
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from TTS.api import TTS
import ffmpeg
from utils.config import DEVICE, MODELS_DIR, etc.
```

## Data Flow

```
Input Files:
  - Video: user_selected.mp4
  - Reference Audio: user_selected.wav (optional)
  ↓
Temporary Files:
  - temp/extracted_audio_TIMESTAMP.wav
  - temp/synthesized_TIMESTAMP.wav
  ↓
Output Files:
  - output/dubbed_TIMESTAMP.mp4
```

## Model Storage

```
~/.cache/huggingface/
├── hub/
│   ├── models--openai--whisper-medium/
│   ├── models--facebook--nllb-200-distilled-600M/
│   └── models--coqui--XTTS-v2/
└── transformers/

OR (if using local MODELS_DIR):

nataq_app/models/
├── whisper/
│   └── medium.pt
├── nllb/
│   ├── config.json
│   ├── pytorch_model.bin
│   └── tokenizer.json
└── xtts/
    ├── config.json
    ├── model.pth
    └── vocab.json
```

## Build Output Structure

```
dist/Nataq/
├── Nataq.exe                    # Main executable
├── _internal/                   # Dependencies
│   ├── torch/
│   ├── transformers/
│   ├── TTS/
│   ├── PyQt5/
│   └── ... (all dependencies)
├── gui/
├── core/
├── utils/
├── README.txt
└── LICENSE.txt
```

## Memory Usage

```
Component                Memory
-----------------------------------------
Application Base         ~500 MB
Whisper Medium          ~3 GB
NLLB-200               ~2.5 GB
XTTS v2                ~1.5 GB
PyTorch + CUDA         ~2 GB
-----------------------------------------
Total Peak              ~9-10 GB RAM
GPU VRAM               ~8-10 GB
```

## Processing Time Breakdown

For a 2-minute video on RTX Titan:

```
Step                    Time        % of Total
----------------------------------------------------
Load Models             60s         25%
Extract Audio           5s          2%
Transcribe (Whisper)    30s         13%
Translate (NLLB)        20s         8%
Synthesize (XTTS)       80s         33%
Merge Video             45s         19%
----------------------------------------------------
Total                   240s        100%
```

## Quick Reference

### Run Application
```bash
venv\Scripts\activate
python main.py
```

### Test Installation
```bash
python test_installation.py
```

### Run Demo
```bash
python demo.py
```

### Build Executable
```bash
pyinstaller nataq.spec
```

### Clean Build
```bash
rmdir /s build dist
pyinstaller nataq.spec
```
