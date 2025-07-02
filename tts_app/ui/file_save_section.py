from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit

class FileSave:
    def __init__(self, main_window):
        self.main_window = main_window

        # Create the layout for the file save section
        self.layout = QHBoxLayout()

        # Create and add the label and input field for audio file name
        self.input = QLineEdit()
        self.input.setPlaceholderText("Output file name")
        self.input.textChanged.connect(self.on_audio_file_name_changed)

        self.layout.addWidget(QLabel("Audio File Name:"))
        self.layout.addWidget(self.input)

    def on_audio_file_name_changed(self, text):
        self.main_window.audioFileName = text
