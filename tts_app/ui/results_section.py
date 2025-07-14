from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel, QLineEdit
from logic.tts_core import text_to_wav

class Results:
    def __init__(self, main_window):
        self.main_window = main_window
        self.results_layout = QVBoxLayout()
        
        self.convertBtn = QPushButton("Convert Text to Speech")
        self.convertBtn.clicked.connect(self.on_convert_button_pushed)
        self.results_layout.addWidget(self.convertBtn)

        # Create a label to display the results
        self.results_label = QLabel("Result/Output:")
        self.results_layout.addWidget(self.results_label)
        self.results_box = QLineEdit()
        self.results_layout.addWidget(self.results_box)
        self.results_box.setReadOnly(True)
        

    def update_results(self, text):
        """Update the results label with new text."""
        self.results_box.setText(text)
    
    def on_convert_button_pushed(self):
        mw = self.main_window
        print(mw.language, mw.voice, mw.textToConvert, mw.audioFileName)
        if not mw.language or not mw.voice or not mw.textToConvert or not mw.audioFileName:
            self.update_results("Please fill in all fields before converting.")
            return
        
        try:
            result = text_to_wav(mw.voice, mw.textToConvert, filename=mw.audioFileName)
            result_text = ""
            if result[0] == 1:
                result_text = f"Audio saved to: {result[1]}"
            else:
                result_text = str(result[1])
                print(result_text)
            self.update_results(result_text)
        except Exception as e:
            self.update_results(e)