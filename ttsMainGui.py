import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (
    QWidget, QComboBox,
    QApplication, QMainWindow, 
    QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit,
    QFileDialog
)

from ttsCore import *


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.language = "";
        self.voice = "";
        self.textToConvert = "";
        self.audioFileName = "";

        self.setWindowTitle("Text-to-Speech GUI")
        vertical_layout = QVBoxLayout()

        languageLayout = QHBoxLayout()
        languageLayout.addWidget(QLabel("TTS Language:"))
        languageInput = QLineEdit()
        languageInput.returnPressed.connect(self.onSearchButtonPushed)
        languageInput.textChanged.connect(self.onLanguageChanged)
        languageLayout.addWidget(languageInput)

        voiceLayout = QHBoxLayout()
        voiceLayout.addWidget(QLabel("TTS Voice:"))
        self.voiceChooser = QComboBox()
        self.voiceChooser.currentTextChanged.connect(self.onVoiceChanged)
        voiceLayout.addWidget(self.voiceChooser)

        textConvertLayout = QHBoxLayout()
        textConvertLayout.addWidget(QLabel("Text to convert:"))
        self.textConvertInput = QLineEdit()
        self.textConvertInput.setPlaceholderText("Enter text to convert to speech")
        self.textConvertInput.textChanged.connect(self.onTextConvertInputChanged)
        textConvertLayout.addWidget(self.textConvertInput)

        audioFileLayout = QHBoxLayout()
        audioFileLayout.addWidget(QLabel("Audio File Name:"))
        self.audioFileNameInput = QLineEdit()
        self.audioFileNameInput.setPlaceholderText("output file name")
        self.audioFileNameInput.textChanged.connect(self.onAudioFileNameChanged)
        audioFileLayout.addWidget(self.audioFileNameInput)

        self.convertBtn = QPushButton("Convert Text to Speech")
        self.convertBtn.clicked.connect(self.onConvertButtonPushed)

        vertical_layout.addLayout(languageLayout)
        vertical_layout.addLayout(voiceLayout)
        vertical_layout.addLayout(textConvertLayout)
        vertical_layout.addLayout(audioFileLayout)
        vertical_layout.addWidget(self.convertBtn)

        widget = QWidget()
        widget.setLayout(vertical_layout)
        self.setCentralWidget(widget)

    def onSearchButtonPushed(self):
        self.voiceChooser.clear()
        self.voiceChooser.addItems(list_voices(language_code=self.language))

    def onLanguageChanged (self, text):
        self.language = text

    def onVoiceChanged(self, text):
        self.voice = text
    
    def onTextConvertInputChanged(self, text):
        self.textToConvert = text
    
    def onAudioFileNameChanged(self, text):
        self.audioFileName = text
    
    def onConvertButtonPushed(self):
        if not self.voice or not self.textToConvert or not self.audioFileName:
            print("Please fill in all fields before converting.")
            return
        
        result = text_to_wav(self.voice, self.textToConvert, filename=self.audioFileName)
        if result[0] == 1:
            print(f"Audio saved as {self.audioFileName}.wav")
        else:
            print("Failed to generate audio.")
        
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()