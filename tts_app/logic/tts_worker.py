from PyQt5.QtCore import QThread, pyqtSignal
from models.tts_config import TTSRequest
from logic.tts_service_manager import TTSServiceManager

class TTSWorker(QThread):
    """Worker thread for TTS conversion to prevent UI blocking"""
    
    # Signals
    progress_updated = pyqtSignal(int)
    conversion_finished = pyqtSignal(str)  # output_path
    conversion_failed = pyqtSignal(str)    # error_message
    
    def __init__(self, tts_request: TTSRequest, tts_service: TTSServiceManager):
        super().__init__()
        self._request = tts_request
        self._service = tts_service

    def run(self) -> None:
        """Execute the TTS conversion"""
        try:
            # Validate request
            is_valid, error_msg = self._request.is_valid()
            if not is_valid:
                self.conversion_failed.emit(error_msg)
                return
            
            self.progress_updated.emit(25)
            
            # Convert voice and audio configs
            voice = self._request.voice_config.to_google_voice()
            audio_config = self._request.audio_config.to_google_audio_config()
            
            self.progress_updated.emit(50)
            
            # Synthesize speech
            audio_content = self._service.synthesize_speech(
                self._request.text, voice, audio_config
            )
            
            self.progress_updated.emit(75)
            
            # Save audio file
            self._service.save_audio(audio_content, self._request.output_path)
            
            self.progress_updated.emit(100)
            self.conversion_finished.emit(self._request.output_path)
            
        except Exception as e:
            self.conversion_failed.emit(str(e))
