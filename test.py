import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QPushButton, QLabel, QLineEdit, QTextEdit, 
                           QComboBox, QSlider, QSpinBox, QMessageBox, QFileDialog,
                           QGroupBox, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from google.cloud import texttospeech
import pygame
import io

class TTSWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, client, text, voice, audio_config, output_path):
        super().__init__()
        self.client = client
        self.text = text
        self.voice = voice
        self.audio_config = audio_config
        self.output_path = output_path
    
    def run(self):
        try:
            self.progress.emit(25)
            
            # Create synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=self.text)
            
            self.progress.emit(50)
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=self.voice,
                audio_config=self.audio_config
            )
            
            self.progress.emit(75)
            
            # Save the audio file
            with open(self.output_path, "wb") as out:
                out.write(response.audio_content)
            
            self.progress.emit(100)
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(str(e))

class GoogleTTSUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.client = None
        self.current_audio_path = None
        self.init_ui()
        self.init_tts_client()
        
    def init_ui(self):
        self.setWindowTitle("Google Text-to-Speech Converter")
        self.setGeometry(100, 100, 800, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Google Text-to-Speech Converter")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Voice Settings Group
        voice_group = QGroupBox("Voice Settings")
        voice_layout = QVBoxLayout(voice_group)
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Language:"))
        self.language_combo = QComboBox()
        self.populate_languages()
        lang_layout.addWidget(self.language_combo)
        voice_layout.addLayout(lang_layout)
        
        # Voice selection
        voice_layout_h = QHBoxLayout()
        voice_layout_h.addWidget(QLabel("Voice:"))
        self.voice_combo = QComboBox()
        self.populate_voices()
        voice_layout_h.addWidget(self.voice_combo)
        voice_layout.addLayout(voice_layout_h)
        
        # Gender selection
        gender_layout = QHBoxLayout()
        gender_layout.addWidget(QLabel("Gender:"))
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["NEUTRAL", "MALE", "FEMALE"])
        gender_layout.addWidget(self.gender_combo)
        voice_layout.addLayout(gender_layout)
        
        main_layout.addWidget(voice_group)
        
        # Audio Settings Group
        audio_group = QGroupBox("Audio Settings")
        audio_layout = QVBoxLayout(audio_group)
        
        # Audio format
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Audio Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["MP3", "WAV", "OGG"])
        format_layout.addWidget(self.format_combo)
        audio_layout.addLayout(format_layout)
        
        # Speaking rate
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("Speaking Rate:"))
        self.rate_slider = QSlider(Qt.Horizontal)
        self.rate_slider.setRange(25, 400)
        self.rate_slider.setValue(100)
        self.rate_label = QLabel("1.0x")
        self.rate_slider.valueChanged.connect(self.update_rate_label)
        rate_layout.addWidget(self.rate_slider)
        rate_layout.addWidget(self.rate_label)
        audio_layout.addLayout(rate_layout)
        
        # Pitch
        pitch_layout = QHBoxLayout()
        pitch_layout.addWidget(QLabel("Pitch:"))
        self.pitch_slider = QSlider(Qt.Horizontal)
        self.pitch_slider.setRange(-20, 20)
        self.pitch_slider.setValue(0)
        self.pitch_label = QLabel("0.0")
        self.pitch_slider.valueChanged.connect(self.update_pitch_label)
        pitch_layout.addWidget(self.pitch_slider)
        pitch_layout.addWidget(self.pitch_label)
        audio_layout.addLayout(pitch_layout)
        
        main_layout.addWidget(audio_group)
        
        # Text Input Group
        text_group = QGroupBox("Text Input")
        text_layout = QVBoxLayout(text_group)
        
        text_layout.addWidget(QLabel("Enter text to convert:"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter the text you want to convert to speech...")
        self.text_input.setMaximumHeight(150)
        text_layout.addWidget(self.text_input)
        
        # Character count
        self.char_count_label = QLabel("Characters: 0/5000")
        self.text_input.textChanged.connect(self.update_char_count)
        text_layout.addWidget(self.char_count_label)
        
        main_layout.addWidget(text_group)
        
        # File Settings Group
        file_group = QGroupBox("File Settings")
        file_layout = QVBoxLayout(file_group)
        
        # Output file name
        filename_layout = QHBoxLayout()
        filename_layout.addWidget(QLabel("Save as:"))
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("output_audio")
        filename_layout.addWidget(self.filename_input)
        
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_save_location)
        filename_layout.addWidget(self.browse_button)
        
        file_layout.addLayout(filename_layout)
        main_layout.addWidget(file_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.convert_button = QPushButton("Convert to Speech")
        self.convert_button.clicked.connect(self.convert_text_to_speech)
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
        
        self.play_button = QPushButton("Play Audio")
        self.play_button.clicked.connect(self.play_audio)
        self.play_button.setEnabled(False)
        
        self.stop_button = QPushButton("Stop Audio")
        self.stop_button.clicked.connect(self.stop_audio)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.convert_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)
        
        main_layout.addLayout(button_layout)
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
    def init_tts_client(self):
        try:
            # Initialize the TTS client
            # Make sure you have set up Google Cloud credentials
            self.client = texttospeech.TextToSpeechClient()
        except Exception as e:
            QMessageBox.warning(self, "Warning", 
                              f"Could not initialize Google TTS client: {str(e)}\n"
                              "Please ensure you have set up Google Cloud credentials.")
    
    def populate_languages(self):
        # Common language codes
        languages = [
            ("en-US", "English (US)"),
            ("en-GB", "English (UK)"),
            ("es-ES", "Spanish (Spain)"),
            ("es-US", "Spanish (US)"),
            ("fr-FR", "French"),
            ("de-DE", "German"),
            ("it-IT", "Italian"),
            ("pt-BR", "Portuguese (Brazil)"),
            ("ru-RU", "Russian"),
            ("ja-JP", "Japanese"),
            ("ko-KR", "Korean"),
            ("zh-CN", "Chinese (Simplified)"),
            ("zh-TW", "Chinese (Traditional)"),
            ("hi-IN", "Hindi"),
            ("ar-XA", "Arabic"),
        ]
        
        for code, name in languages:
            self.language_combo.addItem(name, code)
    
    def populate_voices(self):
        # This is a simplified list. In a real application, you might want to
        # fetch available voices from the API based on the selected language
        voices = [
            "Standard-A", "Standard-B", "Standard-C", "Standard-D",
            "Wavenet-A", "Wavenet-B", "Wavenet-C", "Wavenet-D",
            "Neural2-A", "Neural2-B", "Neural2-C", "Neural2-D"
        ]
        
        for voice in voices:
            self.voice_combo.addItem(voice)
    
    def update_rate_label(self, value):
        rate = value / 100.0
        self.rate_label.setText(f"{rate:.1f}x")
    
    def update_pitch_label(self, value):
        self.pitch_label.setText(f"{value}.0")
    
    def update_char_count(self):
        text = self.text_input.toPlainText()
        count = len(text)
        self.char_count_label.setText(f"Characters: {count}/5000")
        
        if count > 5000:
            self.char_count_label.setStyleSheet("color: red;")
        else:
            self.char_count_label.setStyleSheet("color: black;")
    
    def browse_save_location(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Save Audio File", 
            self.filename_input.text() or "output_audio",
            "Audio Files (*.mp3 *.wav *.ogg);;All Files (*)"
        )
        
        if file_path:
            # Remove extension from the path for the filename input
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            directory = os.path.dirname(file_path)
            self.filename_input.setText(os.path.join(directory, base_name))
    
    def convert_text_to_speech(self):
        if not self.client:
            QMessageBox.critical(self, "Error", "TTS client not initialized!")
            return
        
        text = self.text_input.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter some text to convert!")
            return
        
        if len(text) > 5000:
            QMessageBox.warning(self, "Warning", "Text is too long! Maximum 5000 characters allowed.")
            return
        
        filename = self.filename_input.text().strip()
        if not filename:
            filename = "output_audio"
        
        # Get selected format
        audio_format = self.format_combo.currentText().lower()
        
        # Add extension if not present
        if not filename.endswith(f'.{audio_format}'):
            filename += f'.{audio_format}'
        
        # Prepare voice settings
        language_code = self.language_combo.currentData()
        voice_name = f"{language_code}-{self.voice_combo.currentText()}"
        
        # Map format to Google TTS format
        format_mapping = {
            'mp3': texttospeech.AudioEncoding.MP3,
            'wav': texttospeech.AudioEncoding.LINEAR16,
            'ogg': texttospeech.AudioEncoding.OGG_OPUS
        }
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, self.gender_combo.currentText())
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=format_mapping[audio_format],
            speaking_rate=self.rate_slider.value() / 100.0,
            pitch=self.pitch_slider.value()
        )
        
        # Disable convert button and show progress
        self.convert_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start conversion in separate thread
        self.worker = TTSWorker(self.client, text, voice, audio_config, filename)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.error.connect(self.on_conversion_error)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.start()
        
        self.current_audio_path = filename
    
    def on_conversion_finished(self):
        self.convert_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.play_button.setEnabled(True)
        
        QMessageBox.information(self, "Success", 
                              f"Audio file saved successfully as:\n{self.current_audio_path}")
    
    def on_conversion_error(self, error_message):
        self.convert_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        QMessageBox.critical(self, "Error", f"Conversion failed:\n{error_message}")
    
    def play_audio(self):
        if self.current_audio_path and os.path.exists(self.current_audio_path):
            try:
                pygame.mixer.music.load(self.current_audio_path)
                pygame.mixer.music.play()
                self.stop_button.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not play audio:\n{str(e)}")
        else:
            QMessageBox.warning(self, "Warning", "No audio file to play!")
    
    def stop_audio(self):
        pygame.mixer.music.stop()
        self.stop_button.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = GoogleTTSUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()