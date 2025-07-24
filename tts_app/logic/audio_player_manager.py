import pygame
import os
from typing import Optional

class AudioPlayerManager:
    """Logic manager for audio playback operations"""
    
    def __init__(self):
        self._initialized = False
        self._current_file: Optional[str] = None
        self._initialize_pygame()
    
    def _initialize_pygame(self) -> None:
        """Initialize pygame mixer"""
        try:
            pygame.mixer.init()
            self._initialized = True
        except Exception as e:
            print(f"Failed to initialize audio player: {e}")
            self._initialized = False
    
    @property
    def is_available(self) -> bool:
        """Check if audio player is available"""
        return self._initialized
    
    def load_file(self, file_path: str) -> bool:
        """Load an audio file"""
        if not self.is_available or not os.path.exists(file_path):
            return False
        
        try:
            pygame.mixer.music.load(file_path)
            self._current_file = file_path
            return True
        except Exception as e:
            print(f"Failed to load audio file: {e}")
            return False
    
    def play(self) -> bool:
        """Play the loaded audio file"""
        if not self.is_available or not self._current_file:
            return False
        
        try:
            pygame.mixer.music.play()
            return True
        except Exception as e:
            print(f"Failed to play audio: {e}")
            return False
    
    def stop(self) -> None:
        """Stop audio playback"""
        if self.is_available:
            pygame.mixer.music.stop()
    
    def is_playing(self) -> bool:
        """Check if audio is currently playing"""
        if not self.is_available:
            return False
        return pygame.mixer.music.get_busy()
