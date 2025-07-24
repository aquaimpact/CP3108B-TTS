from enum import Enum

class Voices(Enum):
    Chirp3HD = {"voice_type": "Chirp3-HD", "ssml_support": False}
    Studio = {"voice_type": "Studio", "ssml_support": True}
    Neural2 = {"voice_type": "Neural2", "ssml_support": True}
    WaveNet = {"voice_type": "WaveNet", "ssml_support": True}
    Standard = {"voice_type": "Standard", "ssml_support": True}
    Polyglot = {"voice_type": "Polyglot", "ssml_support": True}
    News = {"voice_type": "News", "ssml_support": True}