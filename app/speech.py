"""Module 10 · Azure Speech: listen (speech to text) and speak (text to speech).

Run:  python app/speech.py   (speak into your microphone)
"""
import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()
config = speechsdk.SpeechConfig(subscription=os.environ["SPEECH_KEY"],
                                region=os.environ["SPEECH_REGION"])
VOICES = {"en-US": "en-US-AvaMultilingualNeural", "hi-IN": "hi-IN-SwaraNeural"}

def listen(language="en-US", wav_file=None):
    config.speech_recognition_language = language
    audio = (speechsdk.audio.AudioConfig(filename=wav_file) if wav_file
             else speechsdk.audio.AudioConfig(use_default_microphone=True))
    result = speechsdk.SpeechRecognizer(config, audio).recognize_once_async().get()
    return result.text

def speak(text, language="en-US", out_file=None):
    config.speech_synthesis_voice_name = VOICES[language]
    audio = (speechsdk.audio.AudioOutputConfig(filename=out_file) if out_file
             else speechsdk.audio.AudioOutputConfig(use_default_speaker=True))
    speechsdk.SpeechSynthesizer(config, audio).speak_text_async(text).get()

if __name__ == "__main__":
    from agent_client import new_conversation, ask_agent
    question = listen("en-US")
    print("You said:", question)
    answer = ask_agent(new_conversation(), question)
    print("Agent:", answer)
    speak(answer, "en-US")
