"""
Nataq Main Window - UPDATED with Pre-trained Voices
Professional GUI with Arabic RTL Support
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, QProgressBar,
                             QTextEdit, QFileDialog, QGroupBox, QGridLayout,
                             QTabWidget, QMessageBox, QApplication, QRadioButton,
                             QButtonGroup, QCheckBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap
import os
from pathlib import Path
from utils.config import (LANGUAGES, ARABIC_DIALECTS, WHISPER_MODELS, 
                         DEFAULT_WHISPER_MODEL, SUPPORTED_VIDEO_FORMATS,
                         SUPPORTED_AUDIO_FORMATS, get_device_info, VOICES_DIR)
from core.processor import VideoProcessor

class ProcessingThread(QThread):
    """Background thread for video processing"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(str, bool)
    error = pyqtSignal(str)
    
    def __init__(self, processor, video_path, voice_type, reference_audio, source_lang, 
                 target_lang, dialect, whisper_model, add_subtitles):
        super().__init__()
        self.processor = processor
        self.video_path = video_path
        self.voice_type = voice_type
        self.reference_audio = reference_audio
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.dialect = dialect
        self.whisper_model = whisper_model
        self.add_subtitles = add_subtitles
    
    def run(self):
        try:
            output_path = self.processor.process_video(
                video_path=self.video_path,
                voice_type=self.voice_type,
                reference_audio=self.reference_audio,
                source_lang=self.source_lang,
                target_lang=self.target_lang,
                dialect=self.dialect,
                whisper_model=self.whisper_model,
                add_subtitles=self.add_subtitles,
                progress_callback=self.update_progress
            )
            self.finished.emit(output_path, True)
        except Exception as e:
            self.error.emit(str(e))
            self.finished.emit("", False)
    
    def update_progress(self, percent, message):
        self.progress.emit(percent, message)

class NataqMainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.video_path = None
        self.reference_audio = None
        self.output_path = None
        self.processor = VideoProcessor()
        self.processing_thread = None
        self.current_language = "en"  # Start with English
        
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Nataq (نطق) - AI Video Dubbing")
        self.setMinimumSize(1000, 750)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Tab widget for different sections
        tabs = QTabWidget()
        tabs.addTab(self.create_dubbing_tab(), "🎬 Video Dubbing")
        tabs.addTab(self.create_settings_tab(), "⚙️ Settings")
        tabs.addTab(self.create_about_tab(), "ℹ️ About")
        main_layout.addWidget(tabs)
        
        # Status bar
        self.statusBar().showMessage(f"Ready | {get_device_info()}")
    
    def create_header(self):
        """Create application header with branding"""
        header = QWidget()
        layout = QHBoxLayout(header)
        
        # Logo/Title
        title_layout = QVBoxLayout()
        
        title_en = QLabel("Nataq - AI Video Dubbing")
        title_en.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_layout.addWidget(title_en)
        
        title_ar = QLabel("نطق - دبلجة الفيديو بالذكاء الاصطناعي")
        title_ar.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title_ar.setAlignment(Qt.AlignRight)
        title_layout.addWidget(title_ar)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Language toggle
        self.lang_toggle = QPushButton("عربي")
        self.lang_toggle.setFixedSize(80, 35)
        self.lang_toggle.clicked.connect(self.toggle_language)
        layout.addWidget(self.lang_toggle)
        
        return header
    
    def create_dubbing_tab(self):
        """Create main dubbing interface tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Input section
        input_group = QGroupBox("📁 Input Files")
        input_layout = QGridLayout()
        
        # Video upload
        video_label = QLabel("Video File:")
        video_label.setFont(QFont("Segoe UI", 10))
        input_layout.addWidget(video_label, 0, 0)
        
        self.video_path_label = QLabel("No file selected")
        self.video_path_label.setStyleSheet("color: #666; font-style: italic;")
        input_layout.addWidget(self.video_path_label, 0, 1)
        
        self.video_btn = QPushButton("📹 Select Video")
        self.video_btn.clicked.connect(self.select_video)
        input_layout.addWidget(self.video_btn, 0, 2)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Voice selection section
        voice_group = QGroupBox("🎤 Voice Selection")
        voice_layout = QVBoxLayout()
        
        voice_info = QLabel("Choose a pre-trained voice for faster processing, or upload your own:")
        voice_info.setWordWrap(True)
        voice_info.setStyleSheet("color: #666; font-style: italic;")
        voice_layout.addWidget(voice_info)
        
        # Radio buttons for voice selection
        self.voice_button_group = QButtonGroup()
        
        self.male_voice_radio = QRadioButton("🎙️ Arabic Male Voice (Fast - Recommended)")
        self.male_voice_radio.setChecked(True)
        self.voice_button_group.addButton(self.male_voice_radio, 0)
        voice_layout.addWidget(self.male_voice_radio)
        
        self.female_voice_radio = QRadioButton("🎙️ Arabic Female Voice (Fast - Recommended)")
        self.voice_button_group.addButton(self.female_voice_radio, 1)
        voice_layout.addWidget(self.female_voice_radio)
        
        self.custom_voice_radio = QRadioButton("📁 Custom Voice (Upload 5-30 sec audio)")
        self.voice_button_group.addButton(self.custom_voice_radio, 2)
        self.custom_voice_radio.toggled.connect(self.on_voice_type_changed)
        voice_layout.addWidget(self.custom_voice_radio)
        
        # Custom voice upload section (hidden by default)
        custom_voice_widget = QWidget()
        custom_voice_layout = QHBoxLayout(custom_voice_widget)
        custom_voice_layout.setContentsMargins(30, 0, 0, 0)
        
        self.audio_path_label = QLabel("No custom voice selected")
        self.audio_path_label.setStyleSheet("color: #666; font-style: italic;")
        custom_voice_layout.addWidget(self.audio_path_label)
        
        self.audio_btn = QPushButton("📂 Browse Audio File")
        self.audio_btn.clicked.connect(self.select_audio)
        custom_voice_layout.addWidget(self.audio_btn)
        
        custom_voice_widget.setVisible(False)
        self.custom_voice_widget = custom_voice_widget
        voice_layout.addWidget(custom_voice_widget)
        
        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)
        
        # Language selection
        lang_group = QGroupBox("🌐 Language Configuration")
        lang_layout = QGridLayout()
        
        # Source language
        source_label = QLabel("Source Language:")
        lang_layout.addWidget(source_label, 0, 0)
        
        self.source_lang = QComboBox()
        self.source_lang.addItems([f"{code} - {name}" for code, name in LANGUAGES.items()])
        self.source_lang.setCurrentText("en - English")
        lang_layout.addWidget(self.source_lang, 0, 1)
        
        # Target language
        target_label = QLabel("Target Language:")
        lang_layout.addWidget(target_label, 1, 0)
        
        self.target_lang = QComboBox()
        self.target_lang.addItems([f"{code} - {name}" for code, name in LANGUAGES.items()])
        self.target_lang.setCurrentText("ar - Arabic")
        self.target_lang.currentTextChanged.connect(self.on_target_language_changed)
        lang_layout.addWidget(self.target_lang, 1, 1)
        
        # Arabic dialect (shown when Arabic is target)
        self.dialect_label = QLabel("Arabic Dialect:")
        lang_layout.addWidget(self.dialect_label, 2, 0)
        
        self.dialect_combo = QComboBox()
        self.dialect_combo.addItems([f"{code} - {name}" for code, name in ARABIC_DIALECTS.items()])
        lang_layout.addWidget(self.dialect_combo, 2, 1)
        
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        
        # Subtitle option
        subtitle_group = QGroupBox("♿ Accessibility (For Deaf/Hard-of-Hearing)")
        subtitle_layout = QVBoxLayout()
        
        self.subtitle_checkbox = QCheckBox("Add subtitles to video (burned-in)")
        self.subtitle_checkbox.setChecked(True)  # Enabled by default
        self.subtitle_checkbox.setToolTip("Adds translated text as subtitles for accessibility")
        subtitle_layout.addWidget(self.subtitle_checkbox)
        
        subtitle_info = QLabel("Subtitles will be permanently embedded in the video")
        subtitle_info.setStyleSheet("color: #666; font-style: italic; font-size: 9pt;")
        subtitle_layout.addWidget(subtitle_info)
        
        subtitle_group.setLayout(subtitle_layout)
        layout.addWidget(subtitle_group)
        
        # Whisper model selection
        model_group = QGroupBox("🤖 AI Model Settings")
        model_layout = QHBoxLayout()
        
        model_label = QLabel("Whisper Model:")
        model_layout.addWidget(model_label)
        
        self.whisper_model = QComboBox()
        self.whisper_model.addItems(WHISPER_MODELS)
        self.whisper_model.setCurrentText(DEFAULT_WHISPER_MODEL)
        model_layout.addWidget(self.whisper_model)
        
        model_info = QLabel("(base=fastest, medium=balanced, large=best quality)")
        model_info.setStyleSheet("color: #666; font-style: italic;")
        model_layout.addWidget(model_info)
        model_layout.addStretch()
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # Process button
        self.process_btn = QPushButton("🚀 Start Dubbing")
        self.process_btn.setMinimumHeight(50)
        self.process_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.process_btn.clicked.connect(self.start_processing)
        self.process_btn.setEnabled(False)
        layout.addWidget(self.process_btn)
        
        # Progress section
        progress_group = QGroupBox("📊 Processing Progress")
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_text = QTextEdit()
        self.progress_text.setReadOnly(True)
        self.progress_text.setMaximumHeight(150)
        self.progress_text.setPlaceholderText("Processing logs will appear here...")
        progress_layout.addWidget(self.progress_text)
        
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)
        
        # Output section
        output_group = QGroupBox("💾 Output")
        output_layout = QHBoxLayout()
        
        self.output_label = QLabel("No output yet")
        self.output_label.setStyleSheet("color: #666; font-style: italic;")
        output_layout.addWidget(self.output_label)
        
        self.preview_btn = QPushButton("▶️ Preview")
        self.preview_btn.clicked.connect(self.preview_output)
        self.preview_btn.setEnabled(False)
        output_layout.addWidget(self.preview_btn)
        
        self.open_folder_btn = QPushButton("📂 Open Folder")
        self.open_folder_btn.clicked.connect(self.open_output_folder)
        self.open_folder_btn.setEnabled(False)
        output_layout.addWidget(self.open_folder_btn)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        layout.addStretch()
        
        return widget
    
    def create_settings_tab(self):
        """Create settings tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        settings_label = QLabel("⚙️ Application Settings")
        settings_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(settings_label)
        
        # Device info
        device_group = QGroupBox("🖥️ Hardware Information")
        device_layout = QVBoxLayout()
        
        device_info = QLabel(get_device_info())
        device_info.setFont(QFont("Segoe UI", 10))
        device_layout.addWidget(device_info)
        
        device_group.setLayout(device_layout)
        layout.addWidget(device_group)
        
        # Voice info
        voice_info_group = QGroupBox("🎤 Pre-trained Voices")
        voice_info_layout = QVBoxLayout()
        
        info_text = QLabel(
            "This application includes pre-trained Arabic voices (male and female) "
            "for faster processing. Using pre-trained voices reduces processing time "
            "significantly compared to voice cloning from uploaded audio."
        )
        info_text.setWordWrap(True)
        voice_info_layout.addWidget(info_text)
        
        voice_info_group.setLayout(voice_info_layout)
        layout.addWidget(voice_info_group)
        
        layout.addStretch()
        
        return widget
    
    def create_about_tab(self):
        """Create about tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Award info
        award_label = QLabel("🏆 Sharjah International Award for AI in Serving the Arabic Language")
        award_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        award_label.setWordWrap(True)
        layout.addWidget(award_label)
        
        # Description
        desc = QLabel(
            "Nataq (نطق) is an advanced AI-powered video dubbing application that "
            "enables seamless translation and voice synthesis between Arabic and other languages. "
            "\n\nKey Features:\n"
            "• Automatic speech recognition using Whisper AI\n"
            "• Neural machine translation with NLLB-200\n"
            "• Voice synthesis with XTTS v2\n"
            "• Pre-trained Arabic voices for faster processing\n"
            "• Support for multiple Arabic dialects (MSA, Egyptian, Levantine, Gulf)\n"
            "• GPU-accelerated processing\n"
            "• Professional video synchronization"
        )
        desc.setWordWrap(True)
        desc.setFont(QFont("Segoe UI", 10))
        layout.addWidget(desc)
        
        # Arabic description
        desc_ar = QLabel(
            "نطق هو تطبيق متقدم لدبلجة الفيديو بالذكاء الاصطناعي يتيح الترجمة السلسة "
            "ونسخ الصوت بين العربية واللغات الأخرى.\n\n"
            "الميزات الرئيسية:\n"
            "• التعرف التلقائي على الكلام باستخدام Whisper AI\n"
            "• الترجمة الآلية العصبية مع NLLB-200\n"
            "• توليد الصوت باستخدام XTTS v2\n"
            "• أصوات عربية مُدرَّبة مسبقاً لمعالجة أسرع\n"
            "• دعم اللهجات العربية المتعددة (الفصحى، المصرية، الشامية، الخليجية)\n"
            "• معالجة مسرّعة بواسطة GPU\n"
            "• مزامنة احترافية للفيديو"
        )
        desc_ar.setWordWrap(True)
        desc_ar.setFont(QFont("Segoe UI", 10))
        desc_ar.setAlignment(Qt.AlignRight)
        layout.addWidget(desc_ar)
        
        # Version info
        version_label = QLabel("Version 1.1.0 | University of Sharjah")
        version_label.setFont(QFont("Segoe UI", 9))
        version_label.setStyleSheet("color: #666;")
        layout.addWidget(version_label)
        
        layout.addStretch()
        
        return widget
    
    def on_voice_type_changed(self, checked):
        """Show/hide custom voice upload based on selection"""
        self.custom_voice_widget.setVisible(checked)
        if not checked:
            self.reference_audio = None
            self.audio_path_label.setText("No custom voice selected")
            self.audio_path_label.setStyleSheet("color: #666; font-style: italic;")
    
    def select_video(self):
        """Handle video file selection"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video File",
            "",
            f"Video Files (*{' *'.join(SUPPORTED_VIDEO_FORMATS)})"
        )
        
        if file_path:
            self.video_path = file_path
            self.video_path_label.setText(os.path.basename(file_path))
            self.video_path_label.setStyleSheet("color: #000;")
            self.process_btn.setEnabled(True)
            self.log_message(f"✓ Video selected: {os.path.basename(file_path)}")
    
    def select_audio(self):
        """Handle reference audio selection"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Reference Audio",
            "",
            f"Audio Files (*{' *'.join(SUPPORTED_AUDIO_FORMATS)})"
        )
        
        if file_path:
            self.reference_audio = file_path
            self.audio_path_label.setText(os.path.basename(file_path))
            self.audio_path_label.setStyleSheet("color: #000;")
            self.log_message(f"✓ Custom voice selected: {os.path.basename(file_path)}")
    
    def on_target_language_changed(self, text):
        """Show/hide dialect selection based on target language"""
        is_arabic = text.startswith("ar")
        self.dialect_label.setVisible(is_arabic)
        self.dialect_combo.setVisible(is_arabic)
    
    def start_processing(self):
        """Start video processing in background thread"""
        if not self.video_path:
            QMessageBox.warning(self, "No Video", "Please select a video file first.")
            return
        
        # Get voice type
        voice_type = "male"  # default
        if self.female_voice_radio.isChecked():
            voice_type = "female"
        elif self.custom_voice_radio.isChecked():
            voice_type = "custom"
            if not self.reference_audio:
                QMessageBox.warning(self, "No Custom Voice", 
                                  "Please select a custom voice audio file or choose a pre-trained voice.")
                return
        
        # Get selected languages
        source = self.source_lang.currentText().split(" - ")[0]
        target = self.target_lang.currentText().split(" - ")[0]
        dialect = self.dialect_combo.currentText().split(" - ")[0] if target == "ar" else None
        whisper_model = self.whisper_model.currentText()
        
        # Get subtitle option
        add_subtitles = self.subtitle_checkbox.isChecked()
        
        # Disable UI during processing
        self.process_btn.setEnabled(False)
        self.video_btn.setEnabled(False)
        self.audio_btn.setEnabled(False)
        self.male_voice_radio.setEnabled(False)
        self.female_voice_radio.setEnabled(False)
        self.custom_voice_radio.setEnabled(False)
        self.progress_bar.setValue(0)
        self.progress_text.clear()
        
        # Start processing thread
        self.processing_thread = ProcessingThread(
            self.processor,
            self.video_path,
            voice_type,
            self.reference_audio,
            source,
            target,
            dialect,
            whisper_model,
            add_subtitles  # Add subtitle option
        )
        
        self.processing_thread.progress.connect(self.update_progress)
        self.processing_thread.finished.connect(self.processing_finished)
        self.processing_thread.error.connect(self.processing_error)
        self.processing_thread.start()
        
        voice_msg = f"Using {voice_type} voice"
        self.log_message(f"🚀 Processing started... {voice_msg}")
    
    def update_progress(self, percent, message):
        """Update progress bar and log"""
        self.progress_bar.setValue(percent)
        self.log_message(message)
    
    def log_message(self, message):
        """Add message to progress log"""
        self.progress_text.append(message)
        self.progress_text.verticalScrollBar().setValue(
            self.progress_text.verticalScrollBar().maximum()
        )
    
    def processing_finished(self, output_path, success):
        """Handle processing completion"""
        # Re-enable UI
        self.process_btn.setEnabled(True)
        self.video_btn.setEnabled(True)
        self.audio_btn.setEnabled(True)
        self.male_voice_radio.setEnabled(True)
        self.female_voice_radio.setEnabled(True)
        self.custom_voice_radio.setEnabled(True)
        
        if success:
            self.output_path = output_path
            self.output_label.setText(os.path.basename(output_path))
            self.output_label.setStyleSheet("color: #000;")
            self.preview_btn.setEnabled(True)
            self.open_folder_btn.setEnabled(True)
            self.log_message("✅ Processing completed successfully!")
            
            QMessageBox.information(
                self,
                "Success",
                f"Video dubbing completed!\n\nOutput: {os.path.basename(output_path)}"
            )
        else:
            self.log_message("❌ Processing failed.")
    
    def processing_error(self, error_msg):
        """Handle processing error"""
        self.log_message(f"❌ Error: {error_msg}")
        QMessageBox.critical(self, "Processing Error", f"An error occurred:\n\n{error_msg}")
    
    def preview_output(self):
        """Preview the output video"""
        if self.output_path and os.path.exists(self.output_path):
            os.startfile(self.output_path)
    
    def open_output_folder(self):
        """Open the output folder"""
        if self.output_path:
            folder = os.path.dirname(self.output_path)
            os.startfile(folder)
    
    def toggle_language(self):
        """Toggle UI language between English and Arabic"""
        if self.current_language == "en":
            self.current_language = "ar"
            self.lang_toggle.setText("English")
            QApplication.setLayoutDirection(Qt.RightToLeft)
        else:
            self.current_language = "en"
            self.lang_toggle.setText("عربي")
            QApplication.setLayoutDirection(Qt.LeftToRight)
    
    def apply_styles(self):
        """Apply modern styling to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0052a3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QComboBox, QRadioButton {
                font-size: 10pt;
            }
            QRadioButton {
                padding: 5px;
            }
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QProgressBar {
                border: 2px solid #ddd;
                border-radius: 5px;
                text-align: center;
                background-color: white;
            }
            QProgressBar::chunk {
                background-color: #0066cc;
                border-radius: 3px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: white;
                font-family: 'Consolas', monospace;
            }
        """)
