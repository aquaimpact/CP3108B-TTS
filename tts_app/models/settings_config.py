from dataclasses import dataclass
from typing import Optional

@dataclass
class GoogleCredentialsConfig:
    """Configuration for Google Cloud credentials"""
    credentials_path: Optional[str] = None
    project_id: Optional[str] = None
    service_account_email: Optional[str] = None
    is_valid: bool = False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'credentials_path': self.credentials_path,
            'project_id': self.project_id,
            'service_account_email': self.service_account_email,
            'is_valid': self.is_valid
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GoogleCredentialsConfig':
        """Create from dictionary"""
        return cls(
            credentials_path=data.get('credentials_path'),
            project_id=data.get('project_id'),
            service_account_email=data.get('service_account_email'),
            is_valid=data.get('is_valid', False)
        )

@dataclass
class AppSettings:
    """Application settings configuration"""
    google_credentials: GoogleCredentialsConfig
    last_output_directory: Optional[str] = None
    remember_settings: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'google_credentials': self.google_credentials.to_dict(),
            'last_output_directory': self.last_output_directory,
            'remember_settings': self.remember_settings
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AppSettings':
        """Create from dictionary"""
        return cls(
            google_credentials=GoogleCredentialsConfig.from_dict(
                data.get('google_credentials', {})
            ),
            last_output_directory=data.get('last_output_directory'),
            remember_settings=data.get('remember_settings', True)
        )
    
    @classmethod
    def default(cls) -> 'AppSettings':
        """Create default settings"""
        return cls(
            google_credentials=GoogleCredentialsConfig()
        )
