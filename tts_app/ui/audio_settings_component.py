from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QComboBox, QSlider, QGroupBox)
from PyQt5.QtCore import Qt
from models.tts_config import AudioConfig

class AudioSettingsComponent(QWidget):
    """UI component for audio configuration settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
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
            pitch=float(self.pitch_slider.value())
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
