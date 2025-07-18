from ui.tts_input_section import InputSelection
from ui.file_save_section import FileSave
from ui.results_section import Results
from ui.error_dialog import ErrorDialog
from PyQt5.QtWidgets import QMainWindow, QPushButton, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SpeechGen")
        self.setGeometry(100, 100, 600, 400)

        # Initialize the input variables
        self.tts_creds_path = "";
        self.language = "";
        self.voice = "";
        self.textToConvert = "";
        self.audioFileName = "";

        try:
            # Create the main layout
            layout = QVBoxLayout()

            self.tts_input_section = InputSelection(self)
            self.output_file_section = FileSave(self)
            self.results_section = Results(self)

            # Add all layouts to the main vertical layout
            layout.addLayout(self.tts_input_section.layout)
            layout.addLayout(self.output_file_section.layout)
            layout.addLayout(self.results_section.results_layout)
        except Exception as e:
            dlg = ErrorDialog()
            dlg.setWindowTitle("HELLO!")
            dlg.exec()

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)