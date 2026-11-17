import os, base64
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv(override=True)
project = AIProjectClient(endpoint=os.environ["AUDIO_PROJECT_ENTPOINT"], credential=DefaultAzureCredential())
client = project.get_openai_client()
with open("data/media/question.wav", "rb") as f:
    audio_in = base64.b64encode(f.read()).decode()
reply = client.chat.completions.create(
    model=os.environ["AUDIO_DEPLOYMENT"],
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {"role": "system", "content": "You are the Fjord Trips assistant. Answer in two short sentences."},
        {"role": "user", "content": [
            {"type": "text", "text": "Answer the traveller's spoken question."},
            {"type": "input_audio", "input_audio": {"data": audio_in, "format": "wav"}},
        ]},
    ],
)
print("MODEL:", reply.model)
a = reply.choices[0].message.audio
print("TRANSCRIPT:", a.transcript)
open("_test_answer.wav", "wb").write(base64.b64decode(a.data))
print("saved _test_answer.wav")
