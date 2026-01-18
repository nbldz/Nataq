"""
Standalone Voice Converter - No Dependencies
Works with any Python version, only needs FFmpeg
"""

import os
import subprocess
import json
from pathlib import Path

# Define voices directly (no imports)
VOICES_DIR = Path(__file__).parent / "voices"

PRETRAINED_VOICES = {
    "male_ar": {
        "name": "Arabic Male Voice",
        "name_ar": "صوت ذكر عربي",
        "file": "male_arabic.wav"
    },
    "female_ar": {
        "name": "Arabic Female Voice", 
        "name_ar": "صوت أنثى عربي",
        "file": "female_arabic.wav"
    },
    "male_en": {
        "name": "English Male Voice",
        "name_ar": "صوت ذكر إنجليزي",
        "file": "male_english.wav"
    },
    "female_en": {
        "name": "English Female Voice",
        "name_ar": "صوت أنثى إنجليزي", 
        "file": "female_english.wav"
    }
}

def check_ffmpeg():
    """Check if ffmpeg is available"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, 
                      check=True,
                      timeout=5)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def convert_voice(input_file, output_name):
    """Convert audio to voice format using FFmpeg"""
    print(f"\nConverting: {input_file}")
    print(f"Output: {output_name}")
    
    output_path = VOICES_DIR / output_name
    
    try:
        # Convert using ffmpeg
        cmd = [
            'ffmpeg',
            '-i', str(input_file),
            '-ar', '22050',        # 22050 Hz sample rate
            '-ac', '1',            # Mono
            '-t', '30',            # Max 30 seconds
            '-acodec', 'pcm_s16le',  # 16-bit PCM
            '-y',                  # Overwrite
            str(output_path)
        ]
        
        print("Converting...")
        result = subprocess.run(cmd, 
                              capture_output=True, 
                              text=True,
                              timeout=60)
        
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        
        print(f"✓ Created: {output_path}")
        print(f"  Size: {output_path.stat().st_size / 1024:.1f} KB")
        return True
        
    except subprocess.TimeoutExpired:
        print("Error: Conversion timed out")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("="*60)
    print("Nataq - Standalone Voice Converter")
    print("="*60)
    print()
    
    # Check ffmpeg
    if not check_ffmpeg():
        print("ERROR: FFmpeg not found!")
        print("\nInstall FFmpeg:")
        print("  choco install ffmpeg")
        print("  OR download from: https://www.gyan.dev/ffmpeg/builds/")
        input("\nPress Enter to exit...")
        return
    
    # Create voices directory
    VOICES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Voices directory: {VOICES_DIR}")
    print()
    
    # Show status
    print("Voice files needed:")
    voice_list = list(PRETRAINED_VOICES.items())
    for i, (voice_id, info) in enumerate(voice_list, 1):
        exists = "✓" if (VOICES_DIR / info['file']).exists() else "✗"
        print(f"  {exists} {i}. {info['name']} ({info['file']})")
    print()
    
    # Select voice
    slot = input("Select voice to create (1-4) or Q to quit: ").strip()
    
    if slot.upper() == 'Q':
        return
    
    try:
        slot_num = int(slot)
        if slot_num < 1 or slot_num > 4:
            print("Invalid selection")
            return
        voice_id, voice_info = voice_list[slot_num - 1]
        output_name = voice_info['file']
    except ValueError:
        print("Invalid selection")
        return
    
    print(f"\nCreating: {voice_info['name']}")
    print()
    
    # Get input file
    print("Enter path to your audio file:")
    print("(Supported: MP3, WAV, M4A, OGG, etc.)")
    print("Requirements: 5-30 seconds, clear speech")
    print()
    input_file = input("File path (or drag & drop): ").strip().strip('"')
    
    if not input_file:
        print("No file specified")
        return
    
    if not os.path.exists(input_file):
        print(f"File not found: {input_file}")
        return
    
    # Convert
    if convert_voice(input_file, output_name):
        print("\n" + "="*60)
        print("SUCCESS!")
        print("="*60)
        
        # Count created voices
        created = sum(1 for _, info in PRETRAINED_VOICES.items() 
                     if (VOICES_DIR / info['file']).exists())
        print(f"\nProgress: {created}/4 voices created")
        
        if created == 4:
            print("\n✓ All voices ready!")
        else:
            print(f"\nRemaining: {4 - created} voice(s)")
    else:
        print("\nConversion failed")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
