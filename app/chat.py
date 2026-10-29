"""Module 6 · Your first AI app: a trip planner chat in the terminal.

Run from the project folder:  python app/chat.py
"""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
client = project.get_openai_client()

INSTRUCTIONS = open("prompts/trip_planner.txt", encoding="utf-8").read()

previous_id = None
print("Fjord Trips planner. Type 'quit' to stop.")
while True:
    question = input("You: ")
    if question.lower() == "quit":
        break
    response = client.responses.create(
        model=os.environ["CHAT_DEPLOYMENT"],
        instructions=INSTRUCTIONS,
        input=question,
        previous_response_id=previous_id,
    )
    previous_id = response.id
    print("Planner:", response.output_text)
    print(f"(tokens in: {response.usage.input_tokens}, out: {response.usage.output_tokens})")
