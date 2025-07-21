from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QTextEdit, QGroupBox,
                           QFileDialog, QMessageBox, QCheckBox, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
import json
import os

class SettingsTabComponent(QWidget):
    """UI component for settings tab with Google credentials and app configuration"""
    
    # Signals
    credentials_updated = pyqtSignal(str)  # credentials_path
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._current_credentials_path = None
    
    def _setup_ui(self) -> None:
        """Setup the settings UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Google Credentials Section
        self._setup_credentials_section(layout)
        
        # App Settings Section
        self._setup_app_settings_section(layout)
        
        # Connection Test Section
        self._setup_connection_test_section(layout)
        
        # Action Buttons
        self._setup_action_buttons(layout)
        
        # Add stretch to push everything to top
        layout.addStretch()
    
    def _setup_credentials_section(self, layout: QVBoxLayout) -> None:
        """Setup Google credentials section"""
        creds_group = QGroupBox("Google Cloud Credentials")
        creds_layout = QVBoxLayout(creds_group)
        
        # Instructions
        instructions = QLabel(
            "To use Google Text-to-Speech, you need to provide a service account key file.\n"
            "1. Go to Google Cloud Console\n"
            "2. Create or select a project\n"
            "3. Enable the Text-to-Speech API\n"
            "4. Create a service account and download the JSON key file"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666; font-size: 11px; padding: 10px;")
        creds_layout.addWidget(instructions)
        
        # Credentials file selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Credentials File:"))
        
        self.credentials_path_input = QLineEdit()
        self.credentials_path_input.setPlaceholderText("Select Google Cloud service account JSON file...")
        self.credentials_path_input.setReadOnly(True)
        file_layout.addWidget(self.credentials_path_input)
        
        self.browse_credentials_button = QPushButton("Browse...")
        self.browse_credentials_button.clicked.connect(self._browse_credentials_file)
        file_layout.addWidget(self.browse_credentials_button)
        
        creds_layout.addLayout(file_layout)
        
        # Credentials info display
        self.credentials_info = QTextEdit()
        self.credentials_info.setMaximumHeight(120)
        self.credentials_info.setReadOnly(True)
        self.credentials_info.setPlaceholderText("Credentials information will appear here...")
        creds_layout.addWidget(self.credentials_info)
        
        # Status indicator
        status_layout = QHBoxLayout()
        self.status_label = QLabel("Status: Not configured")
        self.status_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        creds_layout.addLayout(status_layout)
        
        layout.addWidget(creds_group)
    
    def _setup_app_settings_section(self, layout: QVBoxLayout) -> None:
        """Setup application settings section"""
        app_group = QGroupBox("Application Settings")
        app_layout = QVBoxLayout(app_group)
        
        # Remember settings checkbox
        self.remember_settings_checkbox = QCheckBox("Remember settings between sessions")
        self.remember_settings_checkbox.setChecked(True)
        app_layout.addWidget(self.remember_settings_checkbox)
        
        # Default output directory
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Default Output Directory:"))
        
        self.output_dir_input = QLineEdit()
        self.output_dir_input.setPlaceholderText("Select default directory for audio files...")
        output_layout.addWidget(self.output_dir_input)
        
        self.browse_output_button = QPushButton("Browse...")
        self.browse_output_button.clicked.connect(self._browse_output_directory)
        output_layout.addWidget(self.browse_output_button)
        
        app_layout.addLayout(output_layout)
        
        layout.addWidget(app_group)
    
    def _setup_connection_test_section(self, layout: QVBoxLayout) -> None:
        """Setup connection test section"""
        test_group = QGroupBox("Connection Test")
        test_layout = QVBoxLayout(test_group)
        
        # Test button
        button_layout = QHBoxLayout()
        self.test_connection_button = QPushButton("Test Google TTS Connection")
        self.test_connection_button.clicked.connect(self._test_connection)
        self.test_connection_button.setEnabled(False)
        button_layout.addWidget(self.test_connection_button)
        button_layout.addStretch()
        test_layout.addLayout(button_layout)
        
        # Test results
        self.test_results = QTextEdit()
        self.test_results.setMaximumHeight(80)
        self.test_results.setReadOnly(True)
        self.test_results.setPlaceholderText("Connection test results will appear here...")
        test_layout.addWidget(self.test_results)
        
        layout.addWidget(test_group)
    
    def _setup_action_buttons(self, layout: QVBoxLayout) -> None:
        """Setup action buttons"""
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        button_layout = QHBoxLayout()
        
        # Save settings button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self._save_settings)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.save_button)
        
        # Reset settings button
        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.clicked.connect(self._reset_settings)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        button_layout.addWidget(self.reset_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def _browse_credentials_file(self) -> None:
        """Browse for Google credentials JSON file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Google Cloud Service Account Key",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        
        if file_path:
            self._load_credentials_file(file_path)
    
    def _load_credentials_file(self, file_path: str) -> None:
        """Load and validate credentials file"""
        try:
            with open(file_path, 'r') as f:
                creds = json.load(f)
            
            # Validate required fields
            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 
                             'client_email', 'client_id', 'auth_uri', 'token_uri']
            
            missing_fields = [field for field in required_fields if field not in creds]
            
            if missing_fields:
                QMessageBox.warning(
                    self, "Invalid Credentials File",
                    f"The selected file is missing required fields:\n{', '.join(missing_fields)}"
                )
                return
            
            # Update UI
            self.credentials_path_input.setText(file_path)
            self._current_credentials_path = file_path
            
            # Display credentials info
            info_text = f"Project ID: {creds.get('project_id', 'N/A')}\n"
            info_text += f"Service Account: {creds.get('client_email', 'N/A')}\n"
            info_text += f"Type: {creds.get('type', 'N/A')}"
            self.credentials_info.setPlainText(info_text)
            
            # Update status
            self.status_label.setText("Status: Valid credentials loaded")
            self.status_label.setStyleSheet("color: #388e3c; font-weight: bold;")
            
            # Enable test button
            self.test_connection_button.setEnabled(True)
            
            # Emit signal
            self.credentials_updated.emit(file_path)
            
        except json.JSONDecodeError:
            QMessageBox.critical(
                self, "Invalid File",
                "The selected file is not a valid JSON file."
            )
        except FileNotFoundError:
            QMessageBox.critical(
                self, "File Not Found",
                "The selected file could not be found."
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"An error occurred while loading the credentials file:\n{str(e)}"
            )
    
    def _browse_output_directory(self) -> None:
        """Browse for default output directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Default Output Directory",
            self.output_dir_input.text() or ""
        )
        
        if directory:
            self.output_dir_input.setText(directory)
    
    def _test_connection(self) -> None:
        """Test Google TTS connection"""
        if not self._current_credentials_path:
            self.test_results.setPlainText("No credentials file selected.")
            return
        
        self.test_connection_button.setEnabled(False)
        self.test_results.setPlainText("Testing connection...")
        
        try:
            # Import here to avoid circular imports
            from logic.tts_service_manager import TTSServiceManager
            
            manager = TTSServiceManager()
            success, message = manager.initialize_with_credentials(self._current_credentials_path)
            
            if success:
                # Test actual connection
                test_success, test_message = manager.test_connection()
                if test_success:
                    self.test_results.setPlainText(f"✓ {test_message}")
                    self.test_results.setStyleSheet("color: #388e3c;")
                else:
                    self.test_results.setPlainText(f"✗ {test_message}")
                    self.test_results.setStyleSheet("color: #d32f2f;")
            else:
                self.test_results.setPlainText(f"✗ {message}")
                self.test_results.setStyleSheet("color: #d32f2f;")
                
        except Exception as e:
            self.test_results.setPlainText(f"✗ Connection test failed: {str(e)}")
            self.test_results.setStyleSheet("color: #d32f2f;")
        
        finally:
            self.test_connection_button.setEnabled(True)
    
    def _save_settings(self) -> None:
        """Save current settings"""
        self.settings_changed.emit()
        QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully!")
    
    def _reset_settings(self) -> None:
        """Reset settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset Settings",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.credentials_path_input.clear()
            self.credentials_info.clear()
            self.output_dir_input.clear()
            self.remember_settings_checkbox.setChecked(True)
            self.test_results.clear()
            
            self.status_label.setText("Status: Not configured")
            self.status_label.setStyleSheet("color: #d32f2f; font-weight: bold;")
            
            self.test_connection_button.setEnabled(False)
            self._current_credentials_path = None
            
            self.settings_changed.emit()
    
    def load_settings_data(self, settings) -> None:
        """Load settings data into the UI"""
        if settings.google_credentials.credentials_path:
            self._load_credentials_file(settings.google_credentials.credentials_path)
        
        if settings.last_output_directory:
            self.output_dir_input.setText(settings.last_output_directory)
        
        self.remember_settings_checkbox.setChecked(settings.remember_settings)
    
    def get_settings_data(self) -> dict:
        """Get current settings data from UI"""
        return {
            'credentials_path': self._current_credentials_path,
            'output_directory': self.output_dir_input.text(),
            'remember_settings': self.remember_settings_checkbox.isChecked()
        }
    