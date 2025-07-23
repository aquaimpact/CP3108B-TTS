from dataclasses import dataclass
from typing import Optional
from google.cloud import texttospeech

@dataclass
class VoiceConfig:
    """Configuration for voice settings"""
    language_code: str = "en-US"
    voice_name: str = "en-AU-Chirp3-HD-Achird"
    
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
class SSMLConfig:
    """Configuration for SSML settings"""
    enabled: bool = False
    ssml_text: str = ""
    
    def is_valid(self) -> tuple[bool, Optional[str]]:
        """Validate SSML configuration"""
        if not self.enabled:
            return True, None
        
        if not self.ssml_text.strip():
            return False, "SSML is enabled but no content provided"
        
        return True, None

@dataclass
class TTSRequest:
    """Complete TTS request configuration"""
    text: str
    voice_config: VoiceConfig
    audio_config: AudioConfig
    output_path: str
    ssml_config: Optional[SSMLConfig] = None
    
    def is_valid(self) -> tuple[bool, Optional[str]]:
        """Validate the TTS request"""
        # Check SSML configuration first
        if self.ssml_config:
            ssml_valid, ssml_error = self.ssml_config.is_valid()
            if not ssml_valid:
                return False, ssml_error
            
            # If SSML is enabled, validate SSML text instead of plain text
            if self.ssml_config.enabled:
                if not self.ssml_config.ssml_text.strip():
                    return False, "SSML content cannot be empty"
                
                # For SSML, we count the spoken characters
                from logic.ssml_manager import SSMLManager
                ssml_manager = SSMLManager()
                spoken_chars = ssml_manager.get_character_count(self.ssml_config.ssml_text, count_markup=False)
                
                if spoken_chars > 5000:
                    return False, f"SSML spoken text exceeds 5000 character limit ({spoken_chars} characters)"
                
                # Validate SSML syntax
                is_valid, error_msg = ssml_manager.validate_ssml(self.ssml_config.ssml_text)
                if not is_valid:
                    return False, f"Invalid SSML: {error_msg}"
                
                # Skip plain text validation for SSML
                if not self.output_path.strip():
                    return False, "Output path cannot be empty"
                
                return True, None
        
        # Standard plain text validation
        if not self.text.strip():
            return False, "Text cannot be empty"
        
        if len(self.text) > 5000:
            return False, "Text exceeds 5000 character limit"
        
        if not self.output_path.strip():
            return False, "Output path cannot be empty"
        
        return True, None
    
    def get_synthesis_input(self) -> texttospeech.SynthesisInput:
        """Get the appropriate synthesis input (text or SSML)"""
        if self.ssml_config and self.ssml_config.enabled:
            return texttospeech.SynthesisInput(ssml=self.ssml_config.ssml_text)
        else:
            return texttospeech.SynthesisInput(text=self.text)
