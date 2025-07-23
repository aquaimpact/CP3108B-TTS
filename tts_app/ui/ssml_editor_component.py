from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QTextEdit, QPushButton, QComboBox, QCheckBox,
                           QGroupBox, QSplitter, QListWidget, QMessageBox,
                           QFrame, QScrollArea)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
import re
from logic.ssml_manager import SSMLManager
from typing import Optional, Tuple

class SSMLSyntaxHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for SSML markup"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_highlighting_rules()
    
    def _setup_highlighting_rules(self):
        """Setup syntax highlighting rules"""
        # XML tags
        self.tag_format = QTextCharFormat()
        self.tag_format.setForeground(QColor("#2196F3"))  # Blue
        self.tag_format.setFontWeight(QFont.Bold)
        
        # Attributes
        self.attribute_format = QTextCharFormat()
        self.attribute_format.setForeground(QColor("#4CAF50"))  # Green
        
        # Attribute values
        self.value_format = QTextCharFormat()
        self.value_format.setForeground(QColor("#FF9800"))  # Orange
        
        # Comments
        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#9E9E9E"))  # Gray
        self.comment_format.setFontItalic(True)
    
    def highlightBlock(self, text):
        """Highlight a block of text"""
        # Highlight XML tags
        tag_pattern = r'<[^>]+>'
        for match in re.finditer(tag_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.tag_format)
        
        # Highlight attributes
        attr_pattern = r'\b\w+(?=\s*=)'
        for match in re.finditer(attr_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.attribute_format)
        
        # Highlight attribute values
        value_pattern = r'"[^"]*"'
        for match in re.finditer(value_pattern, text):
            self.setFormat(match.start(), match.end() - match.start(), self.value_format)

class SSMLEditorComponent(QWidget):
    """UI component for SSML editing with syntax highlighting and validation"""
    
    # Signals
    ssml_changed = pyqtSignal(str)  # SSML text
    ssml_enabled_changed = pyqtSignal(bool)  # SSML enabled/disabled
    
    def __init__(self, ssml_manager: SSMLManager, parent=None):
        super().__init__(parent)
        self.ssml_manager = ssml_manager
        self._is_ssml_supported = True
        self._setup_ui()
        self._setup_connections()
    
    def _setup_ui(self) -> None:
        """Setup the user interface"""
        layout = QVBoxLayout(self)
        
        # Create group box
        group_box = QGroupBox("Text Editor")
        group_layout = QVBoxLayout(group_box)
        
        # SSML toggle and info
        self._setup_ssml_header(group_layout)
        
        # Main editor area (splitter)
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side: Editor
        self._setup_editor_panel(splitter)
        
        # Right side: Help and examples
        self._setup_help_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([400, 300])
        group_layout.addWidget(splitter)
        
        # Validation status
        self._setup_validation_status(group_layout)
        
        layout.addWidget(group_box)
    
    def _setup_ssml_header(self, layout: QVBoxLayout) -> None:
        """Setup SSML header with compatibility info"""
        header_layout = QHBoxLayout()
        
        # Mode indicator label
        self.mode_label = QLabel("Text Mode")
        self.mode_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.mode_label.setStyleSheet("color: #666; padding: 2px 8px; border-radius: 3px; background-color: #f0f0f0;")
        header_layout.addWidget(self.mode_label)
        
        # Voice compatibility info
        self.compatibility_label = QLabel("Configure voice to see SSML availability")
        self.compatibility_label.setStyleSheet("color: #666; font-size: 11px; margin-left: 10px;")
        header_layout.addWidget(self.compatibility_label)
        
        header_layout.addStretch()
        
        # SSML tools (hidden by default)
        self.ssml_tools_widget = QWidget()
        ssml_tools_layout = QHBoxLayout(self.ssml_tools_widget)
        ssml_tools_layout.setContentsMargins(0, 0, 0, 0)
        
        # Format button
        self.format_button = QPushButton("Format")
        self.format_button.setMaximumWidth(80)
        self.format_button.setToolTip("Format SSML for better readability")
        ssml_tools_layout.addWidget(self.format_button)
        
        # Convert button
        self.convert_button = QPushButton("Plain → SSML")
        self.convert_button.setMaximumWidth(100)
        self.convert_button.setToolTip("Convert plain text to SSML")
        ssml_tools_layout.addWidget(self.convert_button)
        
        header_layout.addWidget(self.ssml_tools_widget)
        self.ssml_tools_widget.setVisible(False)  # Hidden by default
        
        layout.addLayout(header_layout)
    
    def _setup_editor_panel(self, splitter: QSplitter) -> None:
        """Setup the main editor panel"""
        editor_widget = QWidget()
        editor_layout = QVBoxLayout(editor_widget)
        
        # Editor label
        editor_layout.addWidget(QLabel("Content:"))
        
        # Text editor with syntax highlighting
        self.ssml_editor = QTextEdit()
        self.ssml_editor.setPlaceholderText("Enter your SSML markup here or use plain text...")
        self.ssml_editor.setFont(QFont("Consolas", 10))
        self.ssml_editor.setMinimumHeight(200)
        
        # Apply syntax highlighter
        #self.highlighter = SSMLSyntaxHighlighter(self.ssml_editor.document())
        
        editor_layout.addWidget(self.ssml_editor)
        
        # Character count
        self.char_count_label = QLabel("Characters: 0 (0 spoken)")
        self.char_count_label.setStyleSheet("font-size: 11px; color: #666;")
        editor_layout.addWidget(self.char_count_label)
        
        splitter.addWidget(editor_widget)
    
    def _setup_help_panel(self, splitter: QSplitter) -> None:
        """Setup the help and examples panel"""
        # Create help widget but make it hideable
        self.help_widget = QWidget()
        help_layout = QVBoxLayout(self.help_widget)
        
        # Examples section
        help_layout.addWidget(QLabel("SSML Examples:"))
        
        self.examples_list = QListWidget()
        self.examples_list.setMaximumHeight(150)
        
        # Populate examples
        examples = self.ssml_manager.get_ssml_examples()
        for name, ssml in examples.items():
            self.examples_list.addItem(name)
        
        help_layout.addWidget(self.examples_list)
        
        # Insert example button
        self.insert_example_button = QPushButton("Insert Example")
        self.insert_example_button.setMaximumWidth(120)
        help_layout.addWidget(self.insert_example_button)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        help_layout.addWidget(separator)
        
        # SSML tags help
        help_layout.addWidget(QLabel("Common SSML Tags:"))
        
        # Scrollable help area
        help_scroll = QScrollArea()
        help_scroll.setMaximumHeight(200)
        help_scroll.setWidgetResizable(True)
        
        help_content = QWidget()
        help_content_layout = QVBoxLayout(help_content)
        
        # Add tag descriptions
        tags_help = self.ssml_manager.get_ssml_help()
        for tag, description in tags_help.items():
            tag_label = QLabel(f"<{tag}>")
            tag_label.setFont(QFont("Consolas", 9, QFont.Bold))
            tag_label.setStyleSheet("color: #2196F3;")
            
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Arial", 8))
            desc_label.setStyleSheet("color: #666; margin-bottom: 5px;")
            desc_label.setWordWrap(True)
            
            help_content_layout.addWidget(tag_label)
            help_content_layout.addWidget(desc_label)
        
        help_content_layout.addStretch()
        help_scroll.setWidget(help_content)
        help_layout.addWidget(help_scroll)
        
        splitter.addWidget(self.help_widget)
        self.help_widget.setVisible(False)  # Hidden by default
    
    def _setup_validation_status(self, layout: QVBoxLayout) -> None:
        """Setup validation status display"""
        self.validation_label = QLabel("Ready")
        self.validation_label.setStyleSheet("""
            QLabel {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: #f9f9f9;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.validation_label)
    
    def _setup_connections(self) -> None:
        """Setup signal connections"""
        self.ssml_editor.textChanged.connect(self._on_text_changed)
        self.format_button.clicked.connect(self._format_ssml)
        self.convert_button.clicked.connect(self._convert_to_ssml)
        self.insert_example_button.clicked.connect(self._insert_example)
        self.examples_list.itemDoubleClicked.connect(self._insert_example)
    
    def _on_ssml_enabled_changed(self, enabled: bool) -> None:
        """Handle SSML enabled/disabled"""
        # Enable/disable editor components
        #self.ssml_editor.setEnabled(enabled and self._is_ssml_supported)
        #self.format_button.setEnabled(enabled and self._is_ssml_supported)
        #self.convert_button.setEnabled(enabled and self._is_ssml_supported)
        #self.examples_list.setEnabled(enabled and self._is_ssml_supported)
        #self.insert_example_button.setEnabled(enabled and self._is_ssml_supported)
        
        # Update placeholder text
        #if enabled and self._is_ssml_supported:
        #    self.ssml_editor.setPlaceholderText("Enter your SSML markup here...")
        #elif not self._is_ssml_supported:
        #    self.ssml_editor.setPlaceholderText("SSML not supported for this voice type")
        #else:
        #    self.ssml_editor.setPlaceholderText("SSML disabled - using plain text")
        
        # Emit signal
        #self.ssml_enabled_changed.emit(enabled and self._is_ssml_supported)
        
        # Validate current content
        #self._validate_current_content()
        pass
    
    def _on_text_changed(self) -> None:
        """Handle text changes in editor"""
        self._update_character_count()
        self._validate_current_content()
        
        # Emit signal if SSML is enabled
        if self.is_ssml_enabled():
            self.ssml_changed.emit(self.get_ssml_text())
    
    def _update_character_count(self) -> None:
        """Update character count display"""
        text = self.ssml_editor.toPlainText()
        
        if self.is_ssml_enabled() and text.strip():
            total_chars = len(text)
            spoken_chars = self.ssml_manager.get_character_count(text, count_markup=False)
            self.char_count_label.setText(f"Characters: {total_chars} ({spoken_chars} spoken)")
        else:
            char_count = len(text)
            self.char_count_label.setText(f"Characters: {char_count}")
    
    def _validate_current_content(self) -> None:
        """Validate current content based on mode"""
        text = self.ssml_editor.toPlainText().strip()
        
        if not self._is_ssml_supported:
            # Text mode validation
            if not text:
                self.validation_label.setText("Enter text content")
                self.validation_label.setStyleSheet("""
                    QLabel {
                        padding: 5px;
                        border: 1px solid #ddd;
                        border-radius: 3px;
                        background-color: #f9f9f9;
                        color: #666;
                        font-size: 11px;
                    }
                """)
            elif len(text) > 5000:
                self.validation_label.setText(f"✗ Text too long: {len(text)}/5000 characters")
                self.validation_label.setStyleSheet("""
                    QLabel {
                        padding: 5px;
                        border: 1px solid #f44336;
                        border-radius: 3px;
                        background-color: #FFEBEE;
                        color: #C62828;
                        font-size: 11px;
                    }
                """)
            else:
                self.validation_label.setText(f"✓ Ready for conversion ({len(text)} characters)")
                self.validation_label.setStyleSheet("""
                    QLabel {
                        padding: 5px;
                        border: 1px solid #4CAF50;
                        border-radius: 3px;
                        background-color: #E8F5E8;
                        color: #2E7D32;
                        font-size: 11px;
                    }
                """)
            return
        
        # SSML mode validation
        if not text:
            self.validation_label.setText("Enter text or SSML content")
            self.validation_label.setStyleSheet("""
                QLabel {
                    padding: 5px;
                    border: 1px solid #ddd;
                    border-radius: 3px;
                    background-color: #f9f9f9;
                    color: #666;
                    font-size: 11px;
                }
            """)
            return
        
        # Check if it looks like SSML
        if text.strip().startswith('<speak') and text.strip().endswith('</speak>'):
            # Validate as SSML
            is_valid, message = self.ssml_manager.validate_ssml(text)
            
            if is_valid:
                spoken_chars = self.ssml_manager.get_character_count(text, count_markup=False)
                self.validation_label.setText(f"✓ Valid SSML ({spoken_chars} spoken characters)")
                self.validation_label.setStyleSheet("""
                    QLabel {
                        padding: 5px;
                        border: 1px solid #4CAF50;
                        border-radius: 3px;
                        background-color: #E8F5E8;
                        color: #2E7D32;
                        font-size: 11px;
                    }
                """)
            else:
                self.validation_label.setText(f"✗ Invalid SSML: {message}")
                self.validation_label.setStyleSheet("""
                    QLabel {
                        padding: 5px;
                        border: 1px solid #f44336;
                        border-radius: 3px;
                        background-color: #FFEBEE;
                        color: #C62828;
                        font-size: 11px;
                    }
                """)
        else:
            # Treat as plain text in SSML mode
            if len(text) > 5000:
                self.validation_label.setText(f"✗ Text too long: {len(text)}/5000 characters")
                self.validation_label.setStyleSheet("""
                    QLabel {
                        padding: 5px;
                        border: 1px solid #f44336;
                        border-radius: 3px;
                        background-color: #FFEBEE;
                        color: #C62828;
                        font-size: 11px;
                    }
                """)
            else:
                self.validation_label.setText(f"✓ Plain text ready ({len(text)} characters) - Convert to SSML for advanced features")
                self.validation_label.setStyleSheet("""
                    QLabel {
                        padding: 5px;
                        border: 1px solid #2196F3;
                        border-radius: 3px;
                        background-color: #E3F2FD;
                        color: #1565C0;
                        font-size: 11px;
                    }
                """)
    
    def _format_ssml(self) -> None:
        """Format SSML for better readability"""
        text = self.ssml_editor.toPlainText().strip()
        if not text:
            return
        
        try:
            formatted = self.ssml_manager.format_ssml(text)
            self.ssml_editor.setPlainText(formatted)
        except Exception as e:
            QMessageBox.warning(self, "Format Error", f"Could not format SSML:\n{str(e)}")
    
    def _convert_to_ssml(self) -> None:
        """Convert plain text to SSML"""
        text = self.ssml_editor.toPlainText().strip()
        if not text:
            return
        
        # Check if it's already SSML
        if text.startswith('<speak'):
            QMessageBox.information(self, "Already SSML", "The text appears to already be in SSML format.")
            return
        
        # Convert to SSML
        ssml = self.ssml_manager.convert_plain_to_ssml(text)
        self.ssml_editor.setPlainText(ssml)
    
    def _insert_example(self) -> None:
        """Insert selected example into editor"""
        current_item = self.examples_list.currentItem()
        if not current_item:
            return
        
        example_name = current_item.text()
        examples = self.ssml_manager.get_ssml_examples()
        
        if example_name in examples:
            # Insert at cursor position
            cursor = self.ssml_editor.textCursor()
            cursor.insertText(examples[example_name])
    
    def set_voice_type_compatibility(self, voice_type: str) -> None:
        """Set voice type and update SSML compatibility"""
        self._is_ssml_supported = self.ssml_manager.is_ssml_supported(voice_type)
        
        # Update mode and UI based on compatibility
        if self._is_ssml_supported:
            # SSML Mode
            self.mode_label.setText("SSML Mode")
            self.mode_label.setStyleSheet("color: #4CAF50; padding: 2px 8px; border-radius: 3px; background-color: #E8F5E8; font-weight: bold;")
            
            self.compatibility_label.setText(f"✓ SSML supported for {voice_type} voices")
            self.compatibility_label.setStyleSheet("color: #4CAF50; font-size: 11px; margin-left: 10px;")
            
            # Show SSML tools and help
            self.ssml_tools_widget.setVisible(True)
            self.help_widget.setVisible(True)
            
            # Enable syntax highlighting
            if not hasattr(self, 'highlighter') or self.highlighter is None:
                self.highlighter = SSMLSyntaxHighlighter(self.ssml_editor.document())
            
            # Update placeholder
            self.ssml_editor.setPlaceholderText("Enter text or SSML markup here...\nExample: <speak>Hello <break time=\"1s\"/> world!</speak>")
        
        else:
            # Text Mode
            self.mode_label.setText("Text Mode")
            self.mode_label.setStyleSheet("color: #FF9800; padding: 2px 8px; border-radius: 3px; background-color: #FFF3E0; font-weight: bold;")
            
            self.compatibility_label.setText(f"SSML not supported for {voice_type} voices - using plain text")
            self.compatibility_label.setStyleSheet("color: #FF9800; font-size: 11px; margin-left: 10px;")
            
            # Hide SSML tools and help
            self.ssml_tools_widget.setVisible(False)
            self.help_widget.setVisible(False)
            
            # Disable syntax highlighting
            if hasattr(self, 'highlighter') and self.highlighter is not None:
                self.highlighter.setParent(None)
                self.highlighter = None
            
            # Update placeholder
            self.ssml_editor.setPlaceholderText("Enter the text you want to convert to speech...")
        
        # Update validation
        self._validate_current_content()
        
        # Emit signal about mode change
        self.ssml_enabled_changed.emit(self._is_ssml_supported)
    
    def is_ssml_enabled(self) -> bool:
        """Check if SSML is enabled (based on voice compatibility)"""
        return self._is_ssml_supported
    
    def get_ssml_text(self) -> str:
        """Get SSML text from editor"""
        return self.ssml_editor.toPlainText()
    
    def set_ssml_text(self, text: str) -> None:
        """Set SSML text in editor"""
        self.ssml_editor.setPlainText(text)
    
    def get_plain_text(self) -> str:
        """Get plain text (extracted from SSML if enabled)"""
        if self.is_ssml_enabled():
            ssml_text = self.get_ssml_text()
            if ssml_text.strip():
                return self.ssml_manager.extract_plain_text(ssml_text)
        
        return self.ssml_editor.toPlainText()
    
    def clear_content(self) -> None:
        """Clear editor content"""
        self.ssml_editor.clear()
    
    def validate_current_ssml(self) -> Tuple[bool, str]:
        """Validate current SSML content"""
        if not self.is_ssml_enabled():
            return True, "SSML disabled"
        
        text = self.get_ssml_text().strip()
        if not text:
            return False, "SSML content is empty"
        
        return self.ssml_manager.validate_ssml(text)

    def get_content_for_tts(self) -> tuple[str, bool]:
        """Get content for TTS conversion"""
        text = self.ssml_editor.toPlainText().strip()
        
        if not self._is_ssml_supported:
            # Return plain text
            return text, False
        
        # Check if it's SSML format
        if text.startswith('<speak') and text.endswith('</speak>'):
            return text, True
        else:
            # Return as plain text even in SSML mode
            return text, False

    def validate_content_for_tts(self) -> tuple[bool, str]:
        """Validate content for TTS conversion"""
        text = self.ssml_editor.toPlainText().strip()
        
        if not text:
            return False, "Please enter some text to convert"
        
        if not self._is_ssml_supported:
            # Plain text validation
            if len(text) > 5000:
                return False, f"Text is too long: {len(text)}/5000 characters"
            return True, "Valid text"
        
        # SSML mode validation
        if text.startswith('<speak') and text.endswith('</speak>'):
            # Validate SSML
            is_valid, message = self.ssml_manager.validate_ssml(text)
            if not is_valid:
                return False, f"Invalid SSML: {message}"
            
            # Check spoken character count
            spoken_chars = self.ssml_manager.get_character_count(text, count_markup=False)
            if spoken_chars > 5000:
                return False, f"SSML spoken text is too long: {spoken_chars}/5000 characters"
            
            return True, "Valid SSML"
        else:
            # Plain text in SSML mode
            if len(text) > 5000:
                return False, f"Text is too long: {len(text)}/5000 characters"
            return True, "Valid text"
