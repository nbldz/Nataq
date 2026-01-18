"""
Nataq - Installation Verification Test
Run this to verify all components are working
"""

import sys
import platform

def test_python_version():
    """Check Python version"""
    print("Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor == 10:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} (Need 3.10)")
        return False

def test_pytorch():
    """Check PyTorch and CUDA"""
    print("\nTesting PyTorch...")
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        
        if torch.cuda.is_available():
            print(f"✓ CUDA available: True")
            print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
            print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            return True
        else:
            print("✗ CUDA not available")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_whisper():
    """Check Whisper"""
    print("\nTesting Whisper...")
    try:
        import whisper
        print(f"✓ Whisper installed")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_transformers():
    """Check Transformers"""
    print("\nTesting Transformers...")
    try:
        from transformers import AutoTokenizer
        print(f"✓ Transformers installed")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_tts():
    """Check TTS"""
    print("\nTesting TTS...")
    try:
        from TTS.api import TTS
        print(f"✓ TTS (Coqui) installed")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_pyqt5():
    """Check PyQt5"""
    print("\nTesting PyQt5...")
    try:
        from PyQt5.QtWidgets import QApplication
        print(f"✓ PyQt5 installed")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_ffmpeg():
    """Check FFmpeg"""
    print("\nTesting FFmpeg...")
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✓ {version_line}")
            return True
        else:
            print("✗ FFmpeg not working")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg not found in PATH")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_imports():
    """Test all required imports"""
    print("\nTesting all imports...")
    
    modules = [
        'torch', 'torchvision', 'torchaudio',
        'whisper', 'transformers', 'TTS',
        'PyQt5', 'pydub', 'librosa',
        'soundfile', 'numpy', 'scipy'
    ]
    
    success = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except ImportError as e:
            print(f"  ✗ {module}: {e}")
            success = False
    
    return success

def main():
    """Run all tests"""
    print("="*50)
    print("Nataq Installation Verification")
    print("="*50)
    print(f"\nSystem: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    
    results = []
    
    results.append(("Python Version", test_python_version()))
    results.append(("PyTorch + CUDA", test_pytorch()))
    results.append(("Whisper", test_whisper()))
    results.append(("Transformers", test_transformers()))
    results.append(("TTS", test_tts()))
    results.append(("PyQt5", test_pyqt5()))
    results.append(("FFmpeg", test_ffmpeg()))
    results.append(("All Imports", test_imports()))
    
    print("\n" + "="*50)
    print("Summary")
    print("="*50)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name:20s} {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*50)
    if all_passed:
        print("✓ All tests passed! Ready to use Nataq.")
    else:
        print("✗ Some tests failed. Please check errors above.")
        print("\nTroubleshooting:")
        print("1. Ensure Python 3.10 is installed")
        print("2. Reinstall PyTorch: pip install torch==2.2.0 --index-url https://download.pytorch.org/whl/cu118")
        print("3. Install FFmpeg and add to PATH")
        print("4. Run: pip install -r requirements.txt")
    print("="*50)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
