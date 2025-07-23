from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QGroupBox, QPushButton
from PyQt5.QtCore import pyqtSignal, QThread
from models.tts_config import VoiceConfig
from logic.voice_data_manager import VoiceDataManager, VoiceInfo
from typing import List, Optional

class VoiceSettingsComponent(QWidget):
    """UI component for voice configuration settings with dynamic loading"""
    
    # Signals
    language_changed = pyqtSignal(str)  # language_code
    voice_changed = pyqtSignal(str)     # voice_name
    
    def __init__(self, voice_manager: VoiceDataManager, parent=None):
        super().__init__(parent)
        self.voice_manager = voice_manager
        self._current_voices: List[VoiceInfo] = []
        self._setup_ui()
        self._load_initial_data()
    
    def _setup_ui(self) -> None:
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Create group box
        group_box = QGroupBox("Voice Settings")
        group_layout = QVBoxLayout(group_box)
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Language:"))
        self.language_combo = QComboBox()
        self.language_combo.currentTextChanged.connect(self._on_language_changed)
        lang_layout.addWidget(self.language_combo)
        
        # Refresh button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self._refresh_data)
        self.refresh_button.setMaximumWidth(80)
        lang_layout.addWidget(self.refresh_button)
        
        group_layout.addLayout(lang_layout)
        
        # Voice selection
        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("Voice:"))
        self.voice_combo = QComboBox()
        self.voice_combo.currentTextChanged.connect(self._on_voice_changed)
        voice_layout.addWidget(self.voice_combo)
        group_layout.addLayout(voice_layout)
        
        # Gender selection (read-only, populated based on selected voice)
        gender_layout = QHBoxLayout()
        gender_layout.addWidget(QLabel("Gender:"))
        self.gender_combo = QComboBox()
        self.gender_combo.setEnabled(False)  # Read-only
        gender_layout.addWidget(self.gender_combo)
        group_layout.addLayout(gender_layout)
        
        # Voice type info
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Voice Type:"))
        self.type_label = QLabel("Standard")
        self.type_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        type_layout.addWidget(self.type_label)
        type_layout.addStretch()
        group_layout.addLayout(type_layout)
        
        layout.addWidget(group_box)
    
    def _load_initial_data(self) -> None:
        """Load initial language data"""
        self._populate_languages()
    
    def _populate_languages(self) -> None:
        """Populate language combo box"""
        self.language_combo.clear()
        try:
            languages = self.voice_manager.get_available_languages()
            
            for code, name in languages:
                self.language_combo.addItem(name, code)
                    
        except Exception as e:
            print(f"Failed to populate languages: {e}")
            # Add fallback option
            self.language_combo.addItem("English (US)", "en-US")
    
    def _on_language_changed(self) -> None:
        """Handle language selection change"""
        language_code = self.language_combo.currentData()
        if not language_code:
            return
        
        # Clear voice combo and show loading
        self.voice_combo.clear()
        self.voice_combo.addItem("Loading voices...")
        self.voice_combo.setEnabled(False)
        
        # Load voices in background thread
        self._load_voices_for_language(language_code)
        
        # Emit signal
        self.language_changed.emit(language_code)
    
    def _load_voices_for_language(self, language_code: str) -> None:
        """Load voices for selected language"""
        
        # Start new loading worker
        try:
            voices = self.voice_manager.get_voices_for_language(language_code)
            self._on_voices_loaded(voices)
        except Exception as e:
            self._on_voices_loading_failed(str(e))
    
    def _on_voices_loaded(self, voices: List[VoiceInfo]) -> None:
        """Handle successful voice loading"""
        self._current_voices = voices
        
        # Clear and populate voice combo
        self.voice_combo.clear()
        self.voice_combo.setEnabled(True)
        
        if not voices:
            self.voice_combo.addItem("No voices available")
            return
        
        # Group voices by type for better organization
        for voice in voices:
            display_text = f"{voice.display_name} ({voice.gender})"
            self.voice_combo.addItem(display_text, voice.name)
        
        # Select first voice by default
        if self.voice_combo.count() > 0:
            self.voice_combo.setCurrentIndex(0)
            self._update_voice_info()
    
    def _on_voices_loading_failed(self, error_message: str) -> None:
        """Handle voice loading failure"""
        self.voice_combo.clear()
        self.voice_combo.addItem("Failed to load voices")
        self.voice_combo.setEnabled(False)
        print(f"Voice loading failed: {error_message}")
    
    def _on_voice_changed(self) -> None:
        """Handle voice selection change"""
        self._update_voice_info()
        
        voice_name = self.voice_combo.currentData()
        if voice_name:
            self.voice_changed.emit(voice_name)
    
    def _update_voice_info(self) -> None:
        """Update voice information display"""
        voice_name = self.voice_combo.currentData()
        if not voice_name:
            return
        
        # Find selected voice info
        selected_voice = None
        for voice in self._current_voices:
            if voice.name == voice_name:
                selected_voice = voice
                break
        
        if selected_voice:
            # Update gender combo (read-only)
            self.gender_combo.clear()
            self.gender_combo.addItem(selected_voice.gender)
            
            # Update voice type label
            self.type_label.setText(selected_voice.voice_type)
            
            # Color code by voice type
            type_colors = {
                "Chirp3-HD": "#3eb78e",
                "WaveNet": "#f184b7",
                "Studio": "#4f9de4",
                "Standard": "#d7c227",
                "Neural2": "#a44abf",
                "Polyglot": "#F44336"
            }
            color = type_colors.get(selected_voice.voice_type, "#666666")
            self.type_label.setStyleSheet(f"font-weight: bold; color: {color};")
    
    def _refresh_data(self) -> None:
        """Refresh language and voice data"""
        self.refresh_button.setEnabled(False)
        self.refresh_button.setText("Refreshing...")
        
        try:
            # Clear cache and reload
            self.voice_manager.refresh_data()
            self._populate_languages()
            # Reload voices for current language
            current_language = self.language_combo.currentData()
            if current_language:
                self._load_voices_for_language(current_language)
                
        except Exception as e:
            print(f"Failed to refresh data: {e}")
        finally:
            self.refresh_button.setEnabled(True)
            self.refresh_button.setText("Refresh")
    
    def get_voice_config(self) -> VoiceConfig:
        """Get current voice configuration"""
        language_code = self.language_combo.currentData() or "en-US"
        voice_name = self.voice_combo.currentData() or "en-AU-Chirp3-HD-Achird"
        
        return VoiceConfig(
            language_code=language_code,
            voice_name=voice_name
        )
    
    def set_voice_config(self, config: VoiceConfig) -> None:
        """Set voice configuration"""
        # Find and set language
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == config.language_code:
                self.language_combo.setCurrentIndex(i)
                break
        
        # Voice will be set after language loads voices
        # Store the target voice to set after loading
        self._target_voice = config.voice_name
    
    def set_credentials_available(self, available: bool) -> None:
        """Enable/disable component based on credentials availability"""
        self.setEnabled(available)
        if not available:
            self.language_combo.clear()
            self.language_combo.addItem("Configure credentials first")
            self.voice_combo.clear()
            self.voice_combo.addItem("Configure credentials first")
