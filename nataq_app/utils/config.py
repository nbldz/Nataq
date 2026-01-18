"""
Configuration and Environment Setup
"""

import os
import torch
from pathlib import Path

# Application directories
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "output"

# Supported languages and dialects
LANGUAGES = {
    "en": "English",
    "ar": "Arabic",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese"
}

ARABIC_DIALECTS = {
    "msa": "Modern Standard Arabic (الفصحى)",
    "gulf": "Gulf Arabic (الخليجية - السعودية، الإمارات، الكويت)",
    "egyptian": "Egyptian Arabic (المصرية)",
    "levantine": "Levantine Arabic (الشامية - سوريا، لبنان، الأردن، فلسطين)",
    "north_african": "North African Arabic (المغاربية - الجزائر، المغرب، تونس)"
}

# Model configurations
WHISPER_MODELS = ["base", "medium", "large-v2"]
DEFAULT_WHISPER_MODEL = "medium"

# NLLB-200 model for translation
NLLB_MODEL = "facebook/nllb-200-distilled-600M"

# XTTS v2 for voice cloning
XTTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

# Pre-trained voices directory
VOICES_DIR = BASE_DIR / "voices"

# Pre-trained voice options
PRETRAINED_VOICES = {
    "male_ar": {
        "name": "Arabic Male Voice",
        "name_ar": "صوت ذكر عربي",
        "file": "male_arabic.wav",
        "language": "ar"
    },
    "female_ar": {
        "name": "Arabic Female Voice", 
        "name_ar": "صوت أنثى عربي",
        "file": "female_arabic.wav",
        "language": "ar"
    },
    "male_en": {
        "name": "English Male Voice",
        "name_ar": "صوت ذكر إنجليزي",
        "file": "male_english.wav",
        "language": "en"
    },
    "female_en": {
        "name": "English Female Voice",
        "name_ar": "صوت أنثى إنجليزي", 
        "file": "female_english.wav",
        "language": "en"
    }
}

# Processing settings
MAX_VIDEO_SIZE_MB = 500
SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".mkv", ".webm"]
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".m4a", ".ogg"]

# GPU settings
USE_GPU = torch.cuda.is_available()
DEVICE = "cuda" if USE_GPU else "cpu"

def setup_environment():
    """Set up required environment variables and directories"""
    
    # Coqui TTS agreement
    os.environ["COQUI_TOS_AGREED"] = "1"
    
    # Create required directories
    for directory in [MODELS_DIR, TEMP_DIR, OUTPUT_DIR, VOICES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Set PyTorch settings for optimal performance
    if USE_GPU:
        torch.backends.cudnn.benchmark = True
        torch.backends.cuda.matmul.allow_tf32 = True
    
    return True

def get_device_info():
    """Get GPU/CPU device information"""
    if USE_GPU:
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        return f"GPU: {gpu_name} ({gpu_memory:.1f}GB)"
    else:
        return "CPU Mode (GPU not available)"

# Language code mappings for NLLB
NLLB_LANG_CODES = {
    "en": "eng_Latn",
    "ar": "arb_Arab",
    "fr": "fra_Latn",
    "es": "spa_Latn",
    "de": "deu_Latn",
    "it": "ita_Latn",
    "pt": "por_Latn",
    "ru": "rus_Cyrl",
    "ja": "jpn_Jpan",
    "ko": "kor_Hang",
    "zh": "zho_Hans"
}

# Whisper language codes
WHISPER_LANG_CODES = list(LANGUAGES.keys())

# Pre-trained voice samples for faster processing
PRETRAINED_VOICES = {
    "male": {
        "name": "Male Voice (Arabic)",
        "description": "Professional male Arabic voice",
        "sample_url": None,  # Will be set to local path after first generation
        "language": "ar"
    },
    "female": {
        "name": "Female Voice (Arabic)",
        "description": "Professional female Arabic voice", 
        "sample_url": None,
        "language": "ar"
    },
    "custom": {
        "name": "Custom Voice (Upload)",
        "description": "Use your own voice sample",
        "sample_url": None
    }
}

# Voice samples directory
VOICES_DIR = BASE_DIR / "voices"
