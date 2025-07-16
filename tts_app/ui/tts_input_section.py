from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QLineEdit, QTextEdit, QPushButton, QFileDialog
from logic.tts_core import list_languages, list_voices
import platform


class InputSelection:
    def __init__(self, main_window):
        self.main_window = main_window

        self.layout = QVBoxLayout()

        tts_credentials_layout = QHBoxLayout()
        tts_credentials_layout.addWidget(QLabel("Google TTS credentials:"))
        self.tts_credentials_input = QLineEdit()
        self.tts_credentials_input.setPlaceholderText("Path to the TTS credentials JSON file")
        self.tts_credentials_input.textChanged.connect(self.on_tts_cred_input_change)

        os_name = platform.system()
        if os_name == "Windows":
            print("TODO:")
            # self.tts_credentials_input.setText("%APPDATA%\gcloud\application_default_credentials.json")
        else:
            self.tts_credentials_input.setText("~/.config/gcloud/application_default_credentials.json")
            
        tts_credentials_layout.addWidget(self.tts_credentials_input)

        self.tts_button = QPushButton("Open File")
        self.tts_button.clicked.connect(self.open_tts_creds_file)
        tts_credentials_layout.addWidget(self.tts_button)

        self.layout.addLayout(tts_credentials_layout)

        language_layout = QHBoxLayout()
        language_layout.addWidget(QLabel("TTS Language:"))
        language_input = QLineEdit()
        language_input.returnPressed.connect(self.on_search_button_pushed)
        language_input.textChanged.connect(self.on_language_change)
        language_layout.addWidget(language_input)
        self.layout.addLayout(language_layout)

        voice_layout = QHBoxLayout()
        voice_layout.addWidget(QLabel("TTS Voice:"))
        self.voice_chooser = QComboBox()
        self.voice_chooser.currentTextChanged.connect(self.on_voice_change)
        voice_layout.addWidget(self.voice_chooser)
        self.layout.addLayout(voice_layout)

        text_convert_layout = QHBoxLayout()
        text_convert_layout.addWidget(QLabel("Text to convert:"))
        self.text_convert_input = QTextEdit()
        self.text_convert_input.setPlaceholderText("Enter text to convert to speech")
        self.text_convert_input.textChanged.connect(self.on_text_convert_input_change)
        text_convert_layout.addWidget(self.text_convert_input)
        self.layout.addLayout(text_convert_layout)

    def on_search_button_pushed(self):
        self.voice_chooser.clear()
        self.voice_chooser.addItems(list_voices(language_code=self.main_window.language))

    def on_language_change(self, language):
        self.main_window.language = language

    def on_voice_change(self, voice):
        self.main_window.voice = voice

    def on_text_convert_input_change(self):
        text = self.text_convert_input.toPlainText()
        self.main_window.textToConvert = text

    def on_tts_cred_input_change(self):
        text = self.tts_credentials_input.text()
        self.main_window.tts_creds_path = text
        print("current file path:", text)

    def open_tts_creds_file(self):
        file_dialog = QFileDialog(self.main_window)
        file_dialog.setWindowTitle("Select TTS credentials file")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.tts_credentials_input.setText(selected_file)
              