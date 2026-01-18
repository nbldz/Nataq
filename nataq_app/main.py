"""
Nataq (نطق) - AI Video Dubbing Application
Sharjah International Award for AI in Serving the Arabic Language

Main Application Entry Point
Author: Nobel
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import NataqMainWindow
from utils.config import setup_environment

def main():
    """Initialize and run the Nataq application"""
    
    # Set up environment variables
    setup_environment()
    
    # Enable High DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Nataq")
    app.setOrganizationName("Sharjah AI Award")
    app.setStyle("Fusion")
    
    # Create and show main window
    window = NataqMainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
