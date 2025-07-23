from typing import Dict, List, Optional, Tuple
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

class SSMLManager:
    """Manager for SSML (Speech Synthesis Markup Language) functionality"""
    
    # Voice types that support SSML
    SSML_SUPPORTED_VOICES = {
        'Chirp3-HD': False,
        'Standard': True,
        'WaveNet': True,
        'Neural2': True,
        'Studio': True,
        'Polyglot': False,  # Limited SSML support
    }
    
    # SSML tags and their descriptions
    SSML_TAGS = {
        'speak': 'Root element for SSML document',
        'break': 'Insert pauses in speech',
        'emphasis': 'Add emphasis to words or phrases',
        'prosody': 'Control rate, pitch, and volume',
        'say-as': 'Control how text is interpreted',
        'sub': 'Substitute pronunciation',
        'audio': 'Insert audio files',
        'mark': 'Insert markers for timing',
        'p': 'Paragraph break',
        's': 'Sentence break',
        'voice': 'Change voice characteristics',
        'audio': 'Supports insertion of recorded audio files other audio formats together with synthesized speech output.',
        'par': 'Allows you to play multiple media elements at once',
        'phoneme': 'Produce custom pronunciations of words inline',
        'lang': 'Include text in multiple languages'
    }
    
    # Common SSML examples
    SSML_EXAMPLES = {
        'Basic Pause': '<speak>Hello <break time="1s"/> world!</speak>',
        'Emphasis': '<speak>This is <emphasis level="strong">very important</emphasis>!</speak>',
        'Speed Control': '<speak><prosody rate="slow">Speak slowly</prosody> <prosody rate="fast">or speak fast</prosody></speak>',
        'Pitch Control': '<speak><prosody pitch="high">High pitch</prosody> <prosody pitch="low">low pitch</prosody></speak>',
        'Volume Control': '<speak><prosody volume="loud">Loud voice</prosody> <prosody volume="soft">soft voice</prosody></speak>',
        'Spell Out': '<speak>My phone number is <say-as interpret-as="telephone">123-456-7890</say-as></speak>',
        'Date': '<speak>Today is <say-as interpret-as="date" format="mdy">12/25/2023</say-as></speak>',
        'Substitution': '<speak>The <sub alias="World Wide Web">WWW</sub> is amazing!</speak>',
        'Audio': '<speak><audio src="cat_purr_close.ogg"><desc>a cat purring</desc>PURR (sound didn\'t load)</audio></speak>',
        'Parallel Media':'''<speak>
                                <par>
                                    <media xml:id="question" begin="0.5s">
                                        <speak>Who invented the Internet?</speak>
                                    </media>
                                    <media xml:id="answer" begin="question.end+2.0s">
                                        <speak>The Internet was invented by cats.</speak>
                                    </media>
                                    <media begin="answer.end-0.2s" soundLevel="-6dB">
                                        <audio src="https://actions.google.com/.../cartoon_boing.ogg"/>
                                    </media>
                                    <media repeatCount="3" soundLevel="+2.28dB"
                                        fadeInDur="2s" fadeOutDur="0.2s">
                                        <audio src="https://actions.google.com/.../cat_purr_close.ogg"/>
                                    </media>
                                </par>
                            </speak>
                        ''',

    }
    
    def __init__(self):
        self._validation_cache: Dict[str, Tuple[bool, str]] = {}
    
    def is_ssml_supported(self, voice_type: str) -> bool:
        """Check if SSML is supported for a voice type"""
        return self.SSML_SUPPORTED_VOICES.get(voice_type, False)
    
    def validate_ssml(self, ssml_text: str) -> Tuple[bool, str]:
        """Validate SSML markup"""
        # Check cache first
        if ssml_text in self._validation_cache:
            return self._validation_cache[ssml_text]
        
        try:
            # Basic structure check
            if not ssml_text.strip():
                result = (False, "SSML text cannot be empty")
                self._validation_cache[ssml_text] = result
                return result
            
            # Check if it's wrapped in <speak> tags
            if not ssml_text.strip().startswith('<speak'):
                result = (False, "SSML must be wrapped in <speak> tags")
                self._validation_cache[ssml_text] = result
                return result
            
            if not ssml_text.strip().endswith('</speak>'):
                result = (False, "SSML must end with </speak> tag")
                self._validation_cache[ssml_text] = result
                return result
            
            # Try to parse as XML
            try:
                ET.fromstring(ssml_text)
            except ET.ParseError as e:
                result = (False, f"Invalid XML structure: {str(e)}")
                self._validation_cache[ssml_text] = result
                return result
            
            # Check for unsupported tags (basic validation)
            unsupported_tags = self._find_unsupported_tags(ssml_text)
            if unsupported_tags:
                result = (False, f"Unsupported SSML tags: {', '.join(unsupported_tags)}")
                self._validation_cache[ssml_text] = result
                return result
            
            # Validation passed
            result = (True, "Valid SSML")
            self._validation_cache[ssml_text] = result
            return result
            
        except Exception as e:
            result = (False, f"Validation error: {str(e)}")
            self._validation_cache[ssml_text] = result
            return result
    
    def _find_unsupported_tags(self, ssml_text: str) -> List[str]:
        """Find unsupported SSML tags in the text"""
        # Extract all XML tags
        tag_pattern = r'</?(\w+)(?:\s[^>]*)?>'
        tags = re.findall(tag_pattern, ssml_text)
        
        # Check against supported tags
        unsupported = []
        for tag in set(tags):
            if tag not in self.SSML_TAGS:
                unsupported.append(tag)
        
        return unsupported
    
    def convert_plain_to_ssml(self, plain_text: str) -> str:
        """Convert plain text to basic SSML format"""
        if not plain_text.strip():
            return '<speak></speak>'
        
        # Escape XML special characters
        escaped_text = self._escape_xml(plain_text)
        
        # Wrap in speak tags
        return f'<speak>{escaped_text}</speak>'
    
    def _escape_xml(self, text: str) -> str:
        """Escape XML special characters"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text
    
    def format_ssml(self, ssml_text: str) -> str:
        """Format SSML text for better readability"""
        try:
            # Parse and pretty print
            root = ET.fromstring(ssml_text)
            rough_string = ET.tostring(root, 'unicode')
            reparsed = minidom.parseString(rough_string)
            return reparsed.toprettyxml(indent="  ").split('\n', 1)[1]  # Remove XML declaration
        except:
            return ssml_text
    
    def get_ssml_examples(self) -> Dict[str, str]:
        """Get SSML examples for user reference"""
        return self.SSML_EXAMPLES.copy()
    
    def get_ssml_help(self) -> Dict[str, str]:
        """Get SSML tag descriptions"""
        return self.SSML_TAGS.copy()
    
    def extract_plain_text(self, ssml_text: str) -> str:
        """Extract plain text from SSML markup"""
        try:
            # Parse SSML
            root = ET.fromstring(ssml_text)
            
            # Extract all text content
            def extract_text(element):
                text = element.text or ''
                for child in element:
                    text += extract_text(child)
                    text += child.tail or ''
                return text
            
            return extract_text(root).strip()
            
        except:
            # Fallback: remove all XML tags
            return re.sub(r'<[^>]+>', '', ssml_text).strip()
    
    def get_character_count(self, ssml_text: str, count_markup: bool = False) -> int:
        """Get character count for SSML text"""
        if count_markup:
            return len(ssml_text)
        else:
            # Count only the spoken text
            plain_text = self.extract_plain_text(ssml_text)
            return len(plain_text)
    
    def clear_validation_cache(self) -> None:
        """Clear the validation cache"""
        self._validation_cache.clear()
