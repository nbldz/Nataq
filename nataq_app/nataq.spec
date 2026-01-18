# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller Spec File for Nataq Application
Builds standalone Windows .exe with all dependencies
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect data files for TTS models
tts_datas = collect_data_files('TTS')
whisper_datas = collect_data_files('whisper')
transformers_datas = collect_data_files('transformers')

# Hidden imports
hiddenimports = [
    'tiktoken_ext.openai_public',
    'tiktoken_ext',
    'sklearn.utils._cython_blas',
    'sklearn.neighbors.typedefs',
    'sklearn.neighbors.quad_tree',
    'sklearn.tree._utils',
    'scipy.special.cython_special',
    'torch',
    'torchaudio',
    'torchvision',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'TTS',
    'TTS.utils',
    'TTS.tts',
    'TTS.vocoder',
    'TTS.encoder',
    'whisper',
    'transformers',
    'sentencepiece',
    'gruut',
    'phonemizer',
    'librosa',
    'soundfile',
    'pydub',
    'ffmpeg',
] + collect_submodules('TTS') + collect_submodules('transformers')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('gui', 'gui'),
        ('core', 'core'),
        ('utils', 'utils'),
        ('README.md', '.'),
    ] + tts_datas + whisper_datas + transformers_datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'pandas',
        'notebook',
        'IPython',
        'jupyter',
        'spacy',
        'blis',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Nataq',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI application, no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Nataq',
)
