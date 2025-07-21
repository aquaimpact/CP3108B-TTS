from google.cloud import texttospeech
from typing import Optional, List
import os

class TTSServiceManager:
    """Logic manager for Google Text-to-Speech operations"""
    
    def __init__(self):
        self._client: Optional[texttospeech.TextToSpeechClient] = None
        self._credentials_path: Optional[str] = None
        self._is_initialized = False
    
    def initialize_with_credentials(self, credentials_path: str) -> tuple[bool, str]:
        """Initialize TTS client with specific credentials"""
        try:
            # Set environment variable for Google credentials
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
            
            # Create new client
            self._client = texttospeech.TextToSpeechClient()
            self._credentials_path = credentials_path
            self._is_initialized = True
            
            return True, "TTS service initialized successfully"
            
        except Exception as e:
            self._client = None
            self._credentials_path = None
            self._is_initialized = False
            return False, f"Failed to initialize TTS service: {str(e)}"
    
    def initialize_default(self) -> tuple[bool, str]:
        """Initialize with default credentials (environment variable)"""
        try:
            self._client = texttospeech.TextToSpeechClient()
            self._is_initialized = True
            return True, "TTS service initialized with default credentials"
        except Exception as e:
            self._client = None
            self._is_initialized = False
            return False, f"Failed to initialize with default credentials: {str(e)}"
    
    @property
    def is_available(self) -> bool:
        """Check if the TTS service is available"""
        return self._client is not None and self._is_initialized
    
    @property
    def credentials_path(self) -> Optional[str]:
        """Get current credentials path"""
        return self._credentials_path
    
    def test_connection(self) -> tuple[bool, str]:
        """Test the TTS service connection"""
        if not self.is_available:
            return False, "TTS service not initialized"
        
        try:
            # Try to list voices as a connection test
            voices = self._client.list_voices()
            voice_count = len(voices.voices)
            return True, f"Connection successful. {voice_count} voices available."
        except Exception as e:
            return False, f"Connection test failed: {str(e)}"
    
    def get_available_voices(self, language_code: str = None) -> List:
        """Get available voices for a language"""
        if not self.is_available:
            raise RuntimeError("TTS service is not available")
        
        try:
            if language_code:
                voices = self._client.list_voices(language_code=language_code)
            else:
                voices = self._client.list_voices()
            return voices.voices
        except Exception as e:
            raise RuntimeError(f"Failed to get voices: {str(e)}")
    
    def synthesize_speech(self, text: str, voice: texttospeech.VoiceSelectionParams, 
                         audio_config: texttospeech.AudioConfig) -> bytes:
        """Synthesize speech from text"""
        if not self.is_available:
            raise RuntimeError("TTS service is not available")
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        response = self._client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        return response.audio_content
    
    def save_audio(self, audio_content: bytes, output_path: str) -> None:
        """Save audio content to file"""
        directory = os.path.dirname(output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(output_path, "wb") as out:
            out.write(audio_content)
