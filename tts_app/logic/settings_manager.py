import json
import os
from typing import Optional
from models.settings_config import AppSettings

class SettingsManager:
    """Logic manager for application settings persistence"""
    
    def __init__(self, settings_file: str = "tts_settings.json"):
        self.settings_file = settings_file
        self._settings: Optional[AppSettings] = None
    
    def load_settings(self) -> AppSettings:
        """Load settings from file"""
        if self._settings is not None:
            return self._settings
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                self._settings = AppSettings.from_dict(data)
            except (json.JSONDecodeError, KeyError, FileNotFoundError):
                self._settings = AppSettings.default()
        else:
            self._settings = AppSettings.default()
        
        return self._settings
    
    def save_settings(self, settings: AppSettings) -> bool:
        """Save settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings.to_dict(), f, indent=2)
            self._settings = settings
            return True
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False
    
    def get_settings(self) -> AppSettings:
        """Get current settings"""
        if self._settings is None:
            return self.load_settings()
        return self._settings
    
    def update_google_credentials(self, credentials_path: str, 
                                project_id: str = None, 
                                service_account_email: str = None) -> bool:
        """Update Google credentials settings"""
        settings = self.get_settings()
        settings.google_credentials.credentials_path = credentials_path
        settings.google_credentials.project_id = project_id
        settings.google_credentials.service_account_email = service_account_email
        settings.google_credentials.is_valid = self._validate_credentials(credentials_path)
        
        return self.save_settings(settings)
    
    def _validate_credentials(self, credentials_path: str) -> bool:
        """Validate Google credentials file"""
        if not credentials_path or not os.path.exists(credentials_path):
            return False
        
        try:
            with open(credentials_path, 'r') as f:
                creds = json.load(f)
            
            # Check for required fields in service account key
            required_fields = ['type', 'project_id', 'private_key_id', 'private_key', 
                             'client_email', 'client_id', 'auth_uri', 'token_uri']
            
            return all(field in creds for field in required_fields)
        except (json.JSONDecodeError, FileNotFoundError):
            return False
    
    def clear_settings(self) -> bool:
        """Clear all settings"""
        self._settings = AppSettings.default()
        return self.save_settings(self._settings)
