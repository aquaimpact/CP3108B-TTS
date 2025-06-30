def synthesize_ssml_SE_concept():
    """
    Generate an audio file explaining SE concept
    using Google Cloud Text-to-Speech with SSML.
    """
    from google.cloud import texttospeech

    ssml = """
        <speak>
            <p>
                <s><prosody rate="x-fast">Hello!</prosody> <break time="300ms"/> In this short explanation, I’ll walk you through a key phase in software development that is 
                <phoneme alphabet="ipa" ph="ˈsɪs.təm">System</phoneme> 
                <phoneme alphabet="ipa" ph="ˈtɛs.tɪŋ">Testing</phoneme>.
                </s>
            </p>
            
            <break time="600ms"/>

            <p>
                <s>
                <phoneme alphabet="ipa" ph="ˈsɪs.təm">System</phoneme> testing is where we take the entire system and test it against the system 
                <phoneme alphabet="ipa" ph="ˌspɛs.ɪ.fɪˈkeɪ.ʃən">specification</phoneme>.
                </s> <break time="300ms"/>
                <s>
                It’s typically the first time the system is tested as a whole, after all the modules have been integrated.
                </s>
            </p>

            <break time="500ms"/>

            <p>
                <s>
                This kind of testing is performed by a dedicated QA or testing team, not the developers.
                </s> <break time="300ms"/>
                <s>
                The goal is to verify whether the system behaves as expected from the user’s point of view.
                </s>
            </p>
            
            <break time="600ms"/>

            <p>
                <s>
                This level of testing is based on the system’s external behavior, not internal code, so it’s a form of black-box testing.
                </s> <break time="300ms"/>
                <s>
                Sometimes, system tests go beyond the specification to check how the system behaves under extreme or unexpected conditions.
                </s>
            </p>
            <break time="600ms"/>

            <p>
                <s>
                For example, imagine a browser designed to handle web pages with up to 5,000 characters.
                </s> <break time="300ms"/>
                <s>
                A test might try to load a page with more than 5,000 characters.
                </s> <break time="300ms"/>
                <s>
                The expected result is that the browser should stop loading and show a clear error message.
                </s> <break time="300ms"/>
                <s>
                If it crashes instead, that’s a failed system test because it didn’t fail <phoneme alphabet="ipa" ph="ˈɡreɪs.fə.li">gracefully</phoneme>.
                </s>
            </p>

            <break time="600ms"/>
            
            <p>
                <s>
                System testing also includes testing for non-functional requirements.
                </s>
                <s>
                For example, performance testing ensures that the system responds quickly under typical conditions. <break time="300ms"/>
                </s>
                <s>
                Load testing, which is sometimes called stress or scalability testing, checks how the system performs under heavy usage or demand. <break time="300ms"/>
                </s>
                <s>
                Security testing is used to identify any vulnerabilities and to evaluate how secure the system is from potential threats. <break time="300ms"/>
                </s>
                <s>
                Compatibility and interoperability testing help verify whether the system can work smoothly with other systems or software environments. <break time="300ms"/>
                </s>
                <s>
                Usability testing focuses on how intuitive and user-friendly the system is for its intended users. <break time="300ms"/>
                </s>
                <s>
                Finally, portability testing examines whether the system can function correctly across different platforms or devices.
                </s>
            </p>

            <break time="600ms"/>

            <p>
                <s>
                In summary, system testing helps ensure that your complete software system works not only under normal conditions but also in real-world and edge-case scenarios.
                </s> <break time="300ms"/>
                <s>
                It’s the final checkpoint before your product goes live!
                </s>
            </p>

            <break time="600ms"/>
            
            <s><prosody rate="1.5" volume="+3dB">Thanks for listening!</prosody></s>
        </speak>
    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Studio-O",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "sample.mp3"')

synthesize_ssml_SE_concept()
