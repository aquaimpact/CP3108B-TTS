from google.cloud import texttospeech
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import langcodes

@dataclass
class VoiceInfo:
    """Information about a TTS voice"""
    name: str
    language_code: str
    gender: str
    voice_type: str  # Standard, WaveNet, Neural2, etc.
    display_name: str

class VoiceDataManager:
    """Logic manager for fetching and managing voice data from Google TTS"""
    
    def __init__(self, tts_service_manager):
        self.tts_service = tts_service_manager
        self._languages_cache: Optional[List[Tuple[str, str]]] = None
        self._voices_cache: Dict[str, List[VoiceInfo]] = {}
    
    def get_available_languages(self) -> List[Tuple[str, str]]:
        """Get list of available languages from Google TTS"""
        if not self.tts_service.is_available:
            return []
        
        if self._languages_cache is not None:
            return self._languages_cache
        
        try:
            # Get all voices to extract unique languages
            voices = self.tts_service.get_available_voices()
            
            # Extract unique language codes and create display names
            language_set = set()
            for voice in voices:
                language_set.add(voice.language_codes[0])
            
            # Create language list with display names
            languages = []
            for lang_code in sorted(language_set):
                display_name = langcodes.get(lang_code).display_name()
                languages.append((lang_code, display_name))
            
            self._languages_cache = languages
            return languages
            
        except Exception as e:
            print(f"Failed to fetch languages from Google TTS: {e}")
            return []
    
    def get_voices_for_language(self, language_code: str) -> List[VoiceInfo]:
        """Get available voices for a specific language"""
        if not self.tts_service.is_available:
            return []
        
        # Check cache first
        if language_code in self._voices_cache:
            return self._voices_cache[language_code]
        
        try:
            # Get voices for specific language
            voices = self.tts_service.get_available_voices(language_code)
            
            voice_infos = []
            for voice in voices:
                # Extract voice type from name (e.g., "en-US-Wavenet-A" -> "Wavenet")
                voice_type = self._extract_voice_type(voice.name)
                
                # Create display name
                display_name = self._create_voice_display_name(voice.name, voice_type)
                
                voice_info = VoiceInfo(
                    name=voice.name,
                    language_code=voice.language_codes[0],
                    gender=voice.ssml_gender.name,
                    voice_type=voice_type,
                    display_name=display_name
                )
                voice_infos.append(voice_info)
            
            # Sort voices by type and name
            voice_infos.sort(key=lambda v: (v.voice_type, v.name))
            
            # Cache the results
            self._voices_cache[language_code] = voice_infos
            return voice_infos
            
        except Exception as e:
            print(f"Failed to fetch voices for {language_code}: {e}")
            return []
    
    def clear_cache(self) -> None:
        """Clear cached voice data"""
        self._languages_cache = None
        self._voices_cache.clear()
    
    def refresh_data(self) -> None:
        """Refresh voice data from Google TTS"""
        self.clear_cache()
        self.get_available_languages()
    
    def _extract_voice_type(self, voice_name: str) -> str:
        """Extract voice type from voice name"""
        if "Neural2" in voice_name:
            return "Neural2"
        elif "Wavenet" in voice_name or "WaveNet" in voice_name:
            return "WaveNet"
        elif "Standard" in voice_name:
            return "Standard"
        elif "Studio" in voice_name:
            return "Studio"
        elif "Polyglot" in voice_name:
            return "Polyglot"
        else:
            return "Standard"
    
    def _create_voice_display_name(self, voice_name: str, voice_type: str) -> str:
        """Create a user-friendly display name for the voice"""
        # Extract the voice identifier (e.g., "A", "B", "C")
        parts = voice_name.split('-')
        if len(parts) >= 3:
            voice_id = parts[-1]
            return f"{voice_type}-{voice_id}"
        return voice_name
