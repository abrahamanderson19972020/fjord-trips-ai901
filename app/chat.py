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

response = client.responses.create(
    model=os.environ["CHAT_DEPLOYMENT"],
    input="Plan 3 days in Bergen in May on a budget.",
)
print(response.output_text)
