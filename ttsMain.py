from ttsCore import *

# This is the CLI version of the project
def main():
    print("Google Cloud Text-to-Speech API Test")
    print(("-" * 60) + "\n")
    
    print("Listing languages:")
    list_languages()
    
    language = input("\nSelect the language you want to use the voice for: ")

    print(f"\nListing voices for {language}:")
    list_voices(language_code=language)
    
    voice_name = input("\nSelect the voice you want to use: ")
    text = input("Enter the text you want to convert to speech: ");

    print(f"\nGenerating speech for voice '{voice_name}' with text: {text}...")
    text_to_wav(voice_name, text)
    

if __name__ == "__main__":
    main()