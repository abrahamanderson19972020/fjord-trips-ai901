"""Module 10 · Azure Speech: listen (speech to text) and speak (text to speech).

Run:  python app/speech.py   (speak into your microphone)
"""
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

config = speechsdk.SpeechConfig(subscription=os.environ["SPEECH_KEY"],
                                region=os.environ["SPEECH_REGION"]
                                )

VOICES = {"en-US": "en-US-AvaMultilingualNeural", "nb-NO": "nb-NO-PernilleNeural"}

def listen(language="en-US", wav_file=None):
    config.speech_recognition_language = language
    audio = (speechsdk.audio.AudioConfig(filename=wav_file) 
             if wav_file
             else speechsdk.audio.AudioConfig(use_default_microphone=True))
    recongizer = speechsdk.SpeechRecognizer(speech_config=config, audio_config=audio)
    result = recongizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    if result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech recognized. Speak clearly, right after 'Listening'...")
    elif result.reason == speechsdk.ResultReason.Canceled:
        details = result.cancellation_details
        print("Speech cancelled:", details.reason, details.error_details)
    return ""

def speak(text, language="en-US", out_file=None):
    config.speech_synthesis_voice_name = VOICES[language]
    audio = (speechsdk.audio.AudioOutputConfig(filename=out_file) 
             if out_file
             else speechsdk.audio.AudioOutputConfig(use_default_speaker=True))
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=audio)
    synthesizer.speak_text_async(text=text).get()

if __name__ == "__main__":
    from agent_client import new_conversation, ask_agent
    print("Listening... ask your question now.")
    question = listen("nb-NO")
    if not question:
        raise SystemExit("Nothing to send to the agent.")
    print("You said:", question)
    answer = ask_agent(new_conversation(), question)
    print("Agent:", answer)
    speak(answer, "nb-NO")
