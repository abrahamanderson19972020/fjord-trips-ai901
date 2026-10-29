"""Module 10 · A spoken prompt to a multimodal model (audio in, text out).

Needs an audio-capable chat deployment (AUDIO_DEPLOYMENT in .env).
Run:  python app/audio_prompt.py
"""
import os, base64
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
project = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                          credential=DefaultAzureCredential())
client = project.get_openai_client()

with open("data/media/question.wav", "rb") as f:
    audio = base64.b64encode(f.read()).decode()

reply = client.chat.completions.create(
    model=os.environ["AUDIO_DEPLOYMENT"],
    modalities=["text"],
    messages=[
        {"role": "system", "content": "You are the Fjord Trips assistant. Answer briefly."},
        {"role": "user", "content": [
            {"type": "text", "text": "Answer the traveller's spoken question."},
            {"type": "input_audio", "input_audio": {"data": audio, "format": "wav"}},
        ]},
    ],
)
print(reply.choices[0].message.content)
