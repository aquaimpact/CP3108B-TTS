from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QComboBox, QSlider, QGroupBox)
from PyQt5.QtCore import Qt
from models.tts_config import AudioConfig

class AudioProfiles:
    Profiles = {
        'wearable-class-device': 'Smart watches or wearables',
        'handset-class-device': 'Smartphones',
        'headphone-class-device': 'Earbuds or headphones',
        'small-bluetooth-speaker-class-device': 'Small home speakers',
        'medium-bluetooth-speaker-class-device': 'Smart home speakers',
        'large-home-entertainment-class-device': 'Home entertainment systems or smart TVs',
        'large-automotive-class-device': 'Car speakers',
        'telephony-class-application': 'Interactive Voice Response (IVR) system'
    }

class AudioSettingsComponent(QWidget):
    """UI component for audio configuration settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._load_initial_data()
    
    def _setup_ui(self) -> None:
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Create group box
        group_box = QGroupBox("Audio Settings")
        group_layout = QVBoxLayout(group_box)
        
        # Audio format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Audio Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP3", "WAV", "OGG"])
        format_layout.addWidget(self.format_combo)
        group_layout.addLayout(format_layout)
        
        # Speaking rate
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Speaking Rate:"))
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.setRange(25, 400)
        self.rate_slider.setValue(100)
        self.rate_label = QLabel("1.0x")
        self.rate_slider.valueChanged.connect(self._update_rate_label)
        rate_layout.addWidget(self.rate_slider)
        rate_layout.addWidget(self.rate_label)
        group_layout.addLayout(rate_layout)
        
        # Pitch
        pitch_layout = QHBoxLayout()
        pitch_layout.addWidget(QLabel("Pitch:"))
        self.pitch_slider = QSlider(Qt.Horizontal)
        self.pitch_slider.setRange(-20, 20)
        self.pitch_slider.setValue(0)
        self.pitch_label = QLabel("0.0")
        self.pitch_slider.valueChanged.connect(self._update_pitch_label)
        pitch_layout.addWidget(self.pitch_slider)
        pitch_layout.addWidget(self.pitch_label)
        group_layout.addLayout(pitch_layout)

        # Audio Profile
        audio_profile_layout = QHBoxLayout()
        audio_profile_layout.addWidget(QLabel("Audio Profile:"))
        self.audio_profile_combo = QComboBox()
        audio_profile_layout.addWidget(self.audio_profile_combo)
        group_layout.addLayout(audio_profile_layout)

        layout.addWidget(group_box)
    
    def _update_rate_label(self, value: int) -> None:
        """Update speaking rate label"""
        rate = value / 100.0
        self.rate_label.setText(f"{rate:.1f}x")
    
    def _update_pitch_label(self, value: int) -> None:
        """Update pitch label"""
        self.pitch_label.setText(f"{value}.0")
    
    def get_audio_config(self) -> AudioConfig:
        """Get current audio configuration"""
        return AudioConfig(
            format=self.format_combo.currentText(),
            speaking_rate=self.rate_slider.value() / 100.0,
            pitch=float(self.pitch_slider.value()),
            effects_profile_id=[self.audio_profile_combo.currentData()]
        )
    
    def set_audio_config(self, config: AudioConfig) -> None:
        """Set audio configuration"""
        # Set format
        format_index = self.format_combo.findText(config.format)
        if format_index >= 0:
            self.format_combo.setCurrentIndex(format_index)
        
        # Set speaking rate
        self.rate_slider.setValue(int(config.speaking_rate * 100))
        
        # Set pitch
        self.pitch_slider.setValue(int(config.pitch))

    def _load_initial_data(self) -> None:
        """Load initial audio profile data"""
        self._populate_audio_profiles()
    
    def _populate_audio_profiles(self) -> None:
        self.audio_profile_combo.clear()
        for code, name in AudioProfiles.Profiles.items():
            self.audio_profile_combo.addItem(name, code)
