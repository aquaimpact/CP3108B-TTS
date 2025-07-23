from PyQt5.QtWidgets import QCheckBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QGroupBox
from PyQt5.QtCore import pyqtSignal, Qt

class TextInputComponent(QWidget):
    """UI component for text input with character counting"""
    
    text_changed = pyqtSignal(str)  # Emitted when text changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._max_chars = 5000
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Create group box
        group_box = QGroupBox("Text Input")
        group_layout = QVBoxLayout(group_box)
        
        # Instructions and SSML converter
        grp_label_layout = QHBoxLayout()
        grp_label_layout.addWidget(QLabel("Enter text to convert:"))
        self.use_ssml_checkbox = QCheckBox(text="SSML")
        grp_label_layout.addWidget(self.use_ssml_checkbox, alignment=Qt.AlignRight)
        group_layout.addLayout(grp_label_layout)
        
        # Text input
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Enter the text you want to convert to speech...")
        self.text_input.setMaximumHeight(150)
        self.text_input.textChanged.connect(self._on_text_changed)
        group_layout.addWidget(self.text_input)
        
        # Character count
        self.char_count_label = QLabel(f"Characters: 0/{self._max_chars}")
        group_layout.addWidget(self.char_count_label)
        
        layout.addWidget(group_box)
    
    def _on_text_changed(self) -> None:
        """Handle text change events"""
        text = self.text_input.toPlainText()
        char_count = len(text)
        
        # Update character count label
        self.char_count_label.setText(f"Characters: {char_count}/{self._max_chars}")
        
        # Change color if over limit
        if char_count > self._max_chars:
            self.char_count_label.setStyleSheet("color: red;")
        else:
            self.char_count_label.setStyleSheet("color: black;")
        
        # Emit signal
        self.text_changed.emit(text)
    
    def get_text(self) -> str:
        """Get current text"""
        return self.text_input.toPlainText()
    
    def set_text(self, text: str) -> None:
        """Set text content"""
        self.text_input.setPlainText(text)
    
    def clear_text(self) -> None:
        """Clear text content"""
        self.text_input.clear()
    
    @property
    def is_text_valid(self) -> bool:
        """Check if current text is valid"""
        text = self.get_text().strip()
        return bool(text) and len(text) <= self._max_chars

    def get_checkbox_status(self) -> bool:
        return self.use_ssml_checkbox.isChecked()

    def enable_ssml(self) -> None:
        self.use_ssml_checkbox.setChecked(False)
        self.use_ssml_checkbox.setDisabled(False)
    
    def disable_ssml(self) -> None:
        self.use_ssml_checkbox.setChecked(False)
        self.use_ssml_checkbox.setDisabled(True)