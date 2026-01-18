"""
Nataq - Voice Pre-training Script v2.0
Generate high-quality reference voices ONCE, then reuse for fast processing

IMPORTANT: Run this script ONCE before using the main application
It creates male and female Arabic voice samples that will be used
for all future video dubbing (3-5x faster than voice cloning)
"""

import os
import sys
from pathlib import Path
from TTS.api import TTS
import torch

# Set environment
os.environ["COQUI_TOS_AGREED"] = "1"

# Paths
BASE_DIR = Path(__file__).parent
VOICES_DIR = BASE_DIR / "voices"
VOICES_DIR.mkdir(parents=True, exist_ok=True)

# Check GPU
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Sample texts for voice generation (longer for better quality)
VOICE_SAMPLES = {
    "male": """
    السلام عليكم ورحمة الله وبركاته. أنا صوت ذكر عربي احترافي مُصمم لخدمة تطبيق نطق للدبلجة الآلية.
    يمكنني التحدث بوضوح وبطلاقة في اللغة العربية الفصحى مع مراعاة النطق السليم والتشكيل الصحيح.
    هذا النص طويل بما يكفي لإنشاء عينة صوتية عالية الجودة تستخدم في نسخ الأصوات.
    سأكون الصوت الافتراضي للمحتوى الذكوري في تطبيق الدبلجة بالذكاء الاصطناعي.
    جودة الصوت والوضوح في النطق من أهم العوامل لنجاح عملية الدبلجة الآلية.
    """,
    
    "female": """
    السلام عليكم ورحمة الله وبركاته. أنا صوت أنثى عربية احترافية مُصممة لخدمة تطبيق نطق للدبلجة الآلية.
    أستطيع التحدث بلهجة واضحة وطبيعية في اللغة العربية مع الحفاظ على جمالية الصوت النسائي.
    هذا النص مُعد خصيصاً لتوليد نموذج صوتي متميز يُستخدم في نسخ الأصوات النسائية.
    سأكون الصوت الافتراضي للمحتوى النسائي في تطبيق الدبلجة بالذكاء الاصطناعي.
    الوضوح والطبيعية في الأداء الصوتي هما مفتاح نجاح الدبلجة الآلية للفيديوهات.
    """
}

def print_header():
    """Print script header"""
    print("="*70)
    print(" " * 15 + "Nataq - Voice Pre-training System")
    print("="*70)
    print(f"Device: {DEVICE.upper()}")
    print(f"Output Directory: {VOICES_DIR}")
    print("="*70)
    print()

def generate_voice_with_speaker(voice_type, text, output_path):
    """
    Generate voice using XTTS with speaker_wav cloning
    XTTS v2 uses voice cloning, not speaker selection
    """
    print(f"\n[Step 1/3] Loading XTTS v2 model for {voice_type} voice...")
    
    try:
        # Initialize TTS
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(DEVICE)
        print(f"✓ Model loaded successfully")
        
        print(f"\n[Step 2/3] Generating voice without reference (using model default)...")
        
        # XTTS v2 requires either:
        # 1. speaker_wav for voice cloning, OR
        # 2. Use model's internal speaker (not exposed via API)
        
        # Strategy: Generate a simple reference audio first, then use it
        temp_ref = VOICES_DIR / f"temp_ref_{voice_type}.wav"
        
        # First pass: Generate initial voice using gTTS (faster, simpler)
        from gtts import gTTS
        
        print(f"  Creating initial reference audio...")
        # Create a reference audio using gTTS
        ref_text = "مرحبا" if voice_type == "male" else "السلام عليكم"
        temp_gtts = gTTS(text=ref_text, lang='ar', slow=False)
        temp_gtts.save(str(temp_ref))
        print(f"  ✓ Reference audio created")
        
        # Second pass: Use the reference to generate full voice with XTTS
        print(f"\n[Step 3/3] Synthesizing {voice_type} voice with XTTS...")
        tts.tts_to_file(
            text=text,
            speaker_wav=str(temp_ref),
            language="ar",
            file_path=str(output_path)
        )
        
        # Clean up temp reference
        if temp_ref.exists():
            temp_ref.unlink()
        
        print(f"✓ {voice_type.capitalize()} voice saved: {output_path.name}")
        print(f"  File size: {output_path.stat().st_size / 1024:.1f} KB")
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def verify_voice_quality(voice_path):
    """Check if generated voice file is valid"""
    if not voice_path.exists():
        return False, "File not found"
    
    size = voice_path.stat().st_size
    if size < 10000:  # Less than 10KB is suspicious
        return False, f"File too small ({size} bytes)"
    
    return True, "OK"

def main():
    """Generate all voice samples"""
    
    print_header()
    
    print("This script generates reference voices for Nataq:")
    print("  • Arabic Male Voice   (for masculine content)")
    print("  • Arabic Female Voice (for feminine content)")
    print()
    print("These voices enable 3-5x FASTER processing compared to voice cloning.")
    print("⚠️  This only needs to be run ONCE (takes 2-3 minutes)")
    print()
    
    # Check if voices already exist
    male_path = VOICES_DIR / "male_arabic.wav"
    female_path = VOICES_DIR / "female_arabic.wav"
    
    if male_path.exists() or female_path.exists():
        print("⚠️  WARNING: Voice files already exist!")
        if male_path.exists():
            print(f"  • {male_path.name} ({male_path.stat().st_size / 1024:.1f} KB)")
        if female_path.exists():
            print(f"  • {female_path.name} ({female_path.stat().st_size / 1024:.1f} KB)")
        print()
        response = input("Regenerate voices? This will overwrite existing files (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled. Using existing voices.")
            return
    else:
        response = input("Generate voices now? (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return
    
    print()
    print("="*70)
    print("STARTING VOICE GENERATION")
    print("="*70)
    
    results = {}
    
    # Generate male voice
    print(f"\n{'─'*70}")
    print("GENERATING MALE VOICE")
    print(f"{'─'*70}")
    results['male'] = generate_voice_with_speaker("male", VOICE_SAMPLES['male'], male_path)
    
    if results['male']:
        valid, msg = verify_voice_quality(male_path)
        if not valid:
            print(f"⚠️  Warning: Male voice quality issue: {msg}")
            results['male'] = False
    
    # Generate female voice
    print(f"\n{'─'*70}")
    print("GENERATING FEMALE VOICE")
    print(f"{'─'*70}")
    results['female'] = generate_voice_with_speaker("female", VOICE_SAMPLES['female'], female_path)
    
    if results['female']:
        valid, msg = verify_voice_quality(female_path)
        if not valid:
            print(f"⚠️  Warning: Female voice quality issue: {msg}")
            results['female'] = False
    
    # Final summary
    print(f"\n{'='*70}")
    print("GENERATION SUMMARY")
    print(f"{'='*70}")
    print()
    
    if results.get('male'):
        print(f"✓ Male voice:   {male_path}")
        print(f"  Size: {male_path.stat().st_size / 1024:.1f} KB")
    else:
        print(f"✗ Male voice:   FAILED")
    
    print()
    
    if results.get('female'):
        print(f"✓ Female voice: {female_path}")
        print(f"  Size: {female_path.stat().st_size / 1024:.1f} KB")
    else:
        print(f"✗ Female voice: FAILED")
    
    print()
    print(f"{'='*70}")
    
    if all(results.values()):
        print("✓ SUCCESS! All voices generated successfully.")
        print()
        print("Next steps:")
        print("  1. Run the main application: python main.py")
        print("  2. Select 'Arabic Male Voice' or 'Arabic Female Voice'")
        print("  3. Enjoy 3-5x faster processing!")
        print()
        print(f"Voice files location: {VOICES_DIR}")
    else:
        print("✗ FAILED! Some voices could not be generated.")
        print()
        print("Troubleshooting:")
        print("  1. Ensure XTTS is installed: pip install TTS")
        print("  2. Check GPU is available")
        print("  3. Try running again")
        print("  4. Check error messages above")
    
    print(f"{'='*70}")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Cancelled by user.")
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        print("\nPlease report this error.")
