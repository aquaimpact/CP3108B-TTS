from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                           QPushButton, QLabel, QMessageBox, QProgressBar, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os

from ui.voice_settings_component import VoiceSettingsComponent
from ui.audio_settings_component import AudioSettingsComponent
from ui.text_input_component import TextInputComponent
from ui.file_settings_component import FileSettingsComponent
from ui.settings_tab_component import SettingsTabComponent
from ui.ssml_editor_component import SSMLEditorComponent
from logic.tts_worker import TTSWorker
from logic.tts_service_manager import TTSServiceManager
from logic.audio_player_manager import AudioPlayerManager
from logic.settings_manager import SettingsManager
from logic.voice_data_manager import VoiceDataManager
from logic.ssml_manager import SSMLManager
from models.tts_config import TTSRequest
from models.settings_config import AppSettings
from models.tts_config import SSMLConfig

class MainWindow(QMainWindow):
    """Main application window with organized UI and Logic separation"""
    
    def __init__(self):
        super().__init__()
        print("Setting Up...")
        self._setup_logic_managers()
        print("Logic Managers Set Up!")
        self._setup_ui()
        print("UI Set Up!")
        self._setup_connections()
        print("Connections Set Up!")
        self._load_settings()
        print("Loaded Settings!")
        self._current_audio_path = None
    
    def _setup_logic_managers(self) -> None:
        """Initialize logic managers"""
        self.tts_manager = TTSServiceManager()
        self.audio_manager = AudioPlayerManager()
        self.settings_manager = SettingsManager()
        self.voice_data_manager = VoiceDataManager(self.tts_manager)
        self.ssml_manager = SSMLManager()
    
    def _setup_ui(self) -> None:
        """Setup the user interface"""
        self.setWindowTitle("Google Text-to-Speech Converter")
        self.setGeometry(100, 100, 900, 750)
        
        # Central widget with tab widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Google Text-to-Speech Converter")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # TTS Tab
        self._setup_tts_tab()
        
        # Settings Tab
        self._setup_settings_tab()
    
    def _setup_tts_tab(self) -> None:
        """Setup the main TTS conversion tab"""
        tts_widget = QWidget()
        tts_layout = QVBoxLayout(tts_widget)
        
        # UI Components - Pass voice_data_manager to voice component
        self.voice_component = VoiceSettingsComponent(self.voice_data_manager)
        self.audio_component = AudioSettingsComponent()

        # Text & SSML editor
        self.text_editor = SSMLEditorComponent(self.ssml_manager)

        self.file_component = FileSettingsComponent()
        
        tts_layout.addWidget(self.voice_component)
        tts_layout.addWidget(self.audio_component)
        tts_layout.addWidget(self.text_editor)
        tts_layout.addWidget(self.file_component)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        tts_layout.addWidget(self.progress_bar)
        
        # Buttons
        self._setup_tts_buttons(tts_layout)
        
        # Add tab
        self.tab_widget.addTab(tts_widget, "Text-to-Speech")
    
    def _setup_settings_tab(self) -> None:
        """Setup the settings tab"""
        self.settings_component = SettingsTabComponent()
        self.tab_widget.addTab(self.settings_component, "Settings")
    
    def _setup_tts_buttons(self, layout: QVBoxLayout) -> None:
        """Setup TTS action buttons"""
        button_layout = QHBoxLayout()
        
        # Convert button
        self.convert_button = QPushButton("Convert to Speech")
        self.convert_button.clicked.connect(self._convert_text_to_speech)
        self.convert_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        # Play button
        self.play_button = QPushButton("Play Audio")
        self.play_button.clicked.connect(self._play_audio)
        self.play_button.setEnabled(False)
        
        # Stop button
        self.stop_button = QPushButton("Stop Audio")
        self.stop_button.clicked.connect(self._stop_audio)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)
        
        layout.addLayout(button_layout)
    
    def _setup_connections(self) -> None:
        """Setup signal connections between UI and Logic"""
        # Settings connections
        self.settings_component.credentials_updated.connect(self._on_credentials_updated)
        self.settings_component.settings_changed.connect(self._save_current_settings)

        # Voice selection connections
        self.voice_component.voice_changed.connect(self._on_voice_changed)

    def _on_voice_changed(self, voice_name: str) -> None:
        """Handle voice selection change"""
        # Extract voice type from voice name
        voice_type = self.voice_data_manager._extract_voice_type(voice_name)
        
        # Update text editor compatibility
        self.text_editor.set_voice_type_compatibility(voice_type)

    def _load_settings(self) -> None:
        """Load application settings"""
        settings = self.settings_manager.load_settings()
        
        # Load settings into settings component
        self.settings_component.load_settings_data(settings)
        
        # Initialize TTS service if credentials are available
        if settings.google_credentials.credentials_path and settings.google_credentials.is_valid:
            success, message = self.tts_manager.initialize_with_credentials(
                settings.google_credentials.credentials_path
            )
            if success:
                # Enable voice component and refresh data
                self.voice_component.set_credentials_available(True)
                self.voice_component._refresh_data()
            else:
                QMessageBox.warning(self, "TTS Initialization", 
                                  f"Failed to initialize TTS service: {message}")
                self.voice_component.set_credentials_available(False)
        else:
            # Try default initialization
            success, message = self.tts_manager.initialize_default()
            if success:
                self.voice_component.set_credentials_available(True)
                self.voice_component._refresh_data() ## Loads very slowly
            else:
                # Show info message about needing to configure credentials
                self.voice_component.set_credentials_available(False)
                self._show_credentials_info()
    
    def _show_credentials_info(self) -> None:
        """Show information about configuring credentials"""
        QMessageBox.information(
            self, "Setup Required",
            "Google TTS credentials are not configured.\n\n"
            "Please go to the Settings tab to configure your Google Cloud credentials."
        )
    
    def _on_credentials_updated(self, credentials_path: str) -> None:
        """Handle credentials update from UI"""
        success, message = self.tts_manager.initialize_with_credentials(credentials_path)
        
        if success:
            # Enable voice component and refresh data
            self.voice_component.set_credentials_available(True)
            self.voice_component._refresh_data()
            QMessageBox.information(self, "Success", "TTS service initialized successfully!")
        else:
            self.voice_component.set_credentials_available(False)
            QMessageBox.warning(self, "Error", f"Failed to initialize TTS service:\n{message}")
    
    def _save_current_settings(self) -> None:
        """Save current application settings"""
        settings_data = self.settings_component.get_settings_data()
        
        # Create settings object
        settings = self.settings_manager.get_settings()
        
        # Update with current data
        if settings_data['credentials_path']:
            self.settings_manager.update_google_credentials(
                settings_data['credentials_path']
            )
        
        settings.last_output_directory = settings_data['output_directory']
        settings.remember_settings = settings_data['remember_settings']
        
        # Save settings
        self.settings_manager.save_settings(settings)
    
    def _convert_text_to_speech(self) -> None:
        """Convert text to speech using logic managers"""
        if not self.tts_manager.is_available:
            QMessageBox.critical(
                self, "Error", 
                "TTS service is not available!\n\n"
                "Please configure your Google Cloud credentials in the Settings tab."
            )
            # Switch to settings tab
            self.tab_widget.setCurrentIndex(1)
            return

        # Validate Content
        is_valid, error_msg = self.text_editor.validate_content_for_tts()

        if not is_valid:
            QMessageBox.warning(self, "Validation Error", error_msg)
            return
        
        # Get content and determine if it's SSML
        content, is_ssml = self.text_editor.get_content_for_tts()
        
        # Create TTS request from UI components
        voice_config = self.voice_component.get_voice_config()
        audio_config = self.audio_component.get_audio_config()
        
        # Use default output directory if set
        settings = self.settings_manager.get_settings()
        if settings.last_output_directory:
            # Update file component with default directory
            current_filename = self.file_component.filename_input.text() or "output_audio"
            if not os.path.isabs(current_filename):
                full_path = os.path.join(settings.last_output_directory, current_filename)
                self.file_component.set_filename(full_path)
        
        output_path = self.file_component.get_output_path(audio_config.format)
        
        # Create SSML config if content is SSML
        ssml_config = None

        if is_ssml:
            ssml_config = SSMLConfig(
                enabled=True,
                ssml_text=content
            )

        request = TTSRequest(
            text=content if not is_ssml else "",
            voice_config=voice_config,
            audio_config=audio_config,
            output_path=output_path,
            ssml_config=ssml_config
        )

        # Start conversion using logic
        self._start_conversion(request)
    
    def _start_conversion(self, request: TTSRequest) -> None:
        """Start TTS conversion using worker thread"""
        self.convert_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Create and start worker with logic manager
        self.worker = TTSWorker(request, self.tts_manager)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.conversion_finished.connect(self._on_conversion_finished)
        self.worker.conversion_failed.connect(self._on_conversion_failed)
        self.worker.start()
    
    def _on_conversion_finished(self, output_path: str) -> None:
        """Handle successful conversion"""
        self.convert_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.play_button.setEnabled(True)
        self._current_audio_path = output_path
        
        QMessageBox.information(
            self, "Success",
            f"Audio file saved successfully as:\n{output_path}"
        )
    
    def _on_conversion_failed(self, error_message: str) -> None:
        """Handle conversion failure"""
        self.convert_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.critical(self, "Error", f"Conversion failed:\n{error_message}")
    
    def _play_audio(self) -> None:
        """Play the generated audio using audio manager"""
        if not self._current_audio_path:
            QMessageBox.warning(self, "Warning", "No audio file to play!")
            return
        
        if self.audio_manager.load_file(self._current_audio_path):
            if self.audio_manager.play():
                self.stop_button.setEnabled(True)
            else:
                QMessageBox.critical(self, "Error", "Could not play audio file!")
        else:
            QMessageBox.critical(self, "Error", "Could not load audio file!")
    
    def _stop_audio(self) -> None:
        """Stop audio playback using audio manager"""
        self.audio_manager.stop()
        self.stop_button.setEnabled(False)
    
    def closeEvent(self, event) -> None:
        """Handle application close event"""
        # Save settings before closing
        self._save_current_settings()
        event.accept()
