from dataclasses import dataclass
from typing import Optional
from google.cloud import texttospeech

@dataclass
class VoiceConfig:
    """Configuration for voice settings"""
    language_code: str = "en-US"
    voice_name: str = "en-AU-Chirp3-HD-Achird"
    # gender: str = "NEUTRAL"
    
    def to_google_voice(self) -> texttospeech.VoiceSelectionParams:
        """Convert to Google TTS VoiceSelectionParams"""
        return texttospeech.VoiceSelectionParams(
            language_code=self.language_code,
            name=self.voice_name
        )

@dataclass
class AudioConfig:
    """Configuration for audio settings"""
    format: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    
    def to_google_audio_config(self) -> texttospeech.AudioConfig:
        """Convert to Google TTS AudioConfig"""
        format_mapping = {
            'MP3': texttospeech.AudioEncoding.MP3,
            'WAV': texttospeech.AudioEncoding.LINEAR16,
            'OGG': texttospeech.AudioEncoding.OGG_OPUS
        }
        
        return texttospeech.AudioConfig(
            audio_encoding=format_mapping[self.format],
            speaking_rate=self.speaking_rate,
            pitch=self.pitch
        )

@dataclass
class TTSRequest:
    """Complete TTS request configuration"""
    text: str
    voice_config: VoiceConfig
    audio_config: AudioConfig
    output_path: str
    
    def is_valid(self) -> tuple[bool, Optional[str]]:
        """Validate the TTS request"""
        if not self.text.strip():
            return False, "Text cannot be empty"
        
        if len(self.text) > 5000:
            return False, "Text exceeds 5000 character limit"
        
        if not self.output_path.strip():
            return False, "Output path cannot be empty"
        
        return True, None
