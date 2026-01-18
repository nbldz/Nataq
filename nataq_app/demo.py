"""
Nataq - Quick Demo Script
Test the core processing pipeline without GUI
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.processor import VideoProcessor
from utils.config import setup_environment, get_device_info

def demo_processing():
    """Run a quick demo of the processing pipeline"""
    
    print("="*60)
    print("Nataq - Processing Demo")
    print("="*60)
    print()
    
    # Setup environment
    print("Setting up environment...")
    setup_environment()
    print(f"Device: {get_device_info()}")
    print()
    
    # Initialize processor
    print("Initializing video processor...")
    processor = VideoProcessor()
    print()
    
    # Demo parameters
    print("Demo Configuration:")
    print("  Source Language: English (en)")
    print("  Target Language: Arabic (ar)")
    print("  Arabic Dialect: MSA")
    print("  Whisper Model: base (for speed)")
    print()
    
    # Check for test video
    test_video = input("Enter path to test video (or press Enter to skip): ").strip()
    
    if not test_video or not os.path.exists(test_video):
        print("\nNo valid video provided. Demo will show initialization only.")
        print()
        print("To test the full pipeline:")
        print("1. Place a short video (30-60 seconds) in the project folder")
        print("2. Run this script again and provide the video path")
        print("3. Or use the GUI: python main.py")
        print()
        return
    
    # Progress callback
    def progress_callback(percent, message):
        print(f"[{percent:3d}%] {message}")
    
    print("\nStarting processing...")
    print("-" * 60)
    
    try:
        output_path = processor.process_video(
            video_path=test_video,
            reference_audio=None,  # No voice cloning in demo
            source_lang="en",
            target_lang="ar",
            dialect="msa",
            whisper_model="base",
            progress_callback=progress_callback
        )
        
        print("-" * 60)
        print()
        print("✅ Processing Complete!")
        print(f"Output: {output_path}")
        print()
        print("You can now:")
        print(f"  1. Play the video: {output_path}")
        print(f"  2. Compare with original: {test_video}")
        print()
        
    except Exception as e:
        print("-" * 60)
        print()
        print(f"❌ Error: {str(e)}")
        print()
        print("Troubleshooting:")
        print("  1. Ensure FFmpeg is installed and in PATH")
        print("  2. Check that GPU drivers are up to date")
        print("  3. Verify video file is not corrupted")
        print("  4. Run: python test_installation.py")
        print()

def main():
    """Main demo function"""
    try:
        demo_processing()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
