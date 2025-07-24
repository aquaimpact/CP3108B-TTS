from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFileDialog, QGroupBox)
import os

class FileSettingsComponent(QWidget):
    """UI component for file output settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Create group box
        group_box = QGroupBox("File Settings")
        group_layout = QVBoxLayout(group_box)
        
        # Output file name
        filename_layout = QHBoxLayout()
        filename_layout.addWidget(QLabel("Save as:"))
        
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("output_audio")
        filename_layout.addWidget(self.filename_input)
        
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self._browse_save_location)
        filename_layout.addWidget(self.browse_button)
        
        group_layout.addLayout(filename_layout)
        layout.addWidget(group_box)
    
    def _browse_save_location(self) -> None:
        """Open file dialog to select save location"""
        current_filename = self.filename_input.text() or "output_audio"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Audio File",
            current_filename,
            "Audio Files (*.mp3 *.wav *.ogg);;All Files (*)"
        )
        
        if file_path:
            # Remove extension from the path for the filename input
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            directory = os.path.dirname(file_path)
            self.filename_input.setText(os.path.join(directory, base_name))
    
    def get_output_path(self, audio_format: str) -> str:
        """Get complete output path with extension"""
        filename = self.filename_input.text().strip()
        if not filename:
            filename = "output_audio"
        
        # Add extension if not present
        extension = f".{audio_format.lower()}"
        if not filename.endswith(extension):
            filename += extension
        
        return filename
    
    def set_filename(self, filename: str) -> None:
        """Set filename"""
        self.filename_input.setText(filename)
