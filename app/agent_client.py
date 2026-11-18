"""Module 8 · Talk to the Foundry agent `trip-agent` from Python.

The agent's instructions and tools live in Foundry, not in this code.
Test it:  python app/agent_client.py
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
AGENT = {"agent_reference": {"name": os.environ["AGENT_NAME"], "type": "agent_reference"}}

def new_conversation():
    return client.conversations.create().id

def ask_agent(conversation_id, question):
    response = client.responses.create(
        conversation=conversation_id,
        input=question,
        extra_body=AGENT
    )
    return response.output_text

if __name__ == "__main__":
    conv = new_conversation()
    print(ask_agent(conv, "Which trips do you have in May?"))
    print(ask_agent(conv, "Which of those in"))