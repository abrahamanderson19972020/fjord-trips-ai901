"""Module 11 · Vision (photo in, words out) and image generation (words in, new image out).

Run:  python app/vision.py   (uses data/media/photos/geiranger.jpg: add your own photo first)
"""
import os, base64
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.projects import AIProjectClient
from openai import AzureOpenAI

load_dotenv()
credential = DefaultAzureCredential()

# Chat model (gpt-5-mini) lives in our main project
chat_client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=credential
).get_openai_client()

# Image model (gpt-image-1-mini) lives in the image project (another region)
# Image model (gpt-image-1-mini) lives in the image project (another region).
# Image generation uses the resource's Azure OpenAI endpoint, not the project client.
image_resource = os.environ["IMAGE_PROJECT_ENDPOINT"].split("/api/projects")[0]
image_client = AzureOpenAI(
    azure_endpoint=image_resource,
    azure_ad_token_provider=get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    ),
    api_version="2025-04-01-preview",
)

def where_is_this(image_bytes, mime="image/jpeg"):
    data_url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
    response = chat_client.responses.create(
        model=os.environ["CHAT_DEPLOYMENT"],
        instructions="Identify the place in Norway and suggest one Fjord Trips trip. Max 80 words.",
        input=[
            {"role": "user", "content": [
                {"type": "input_text", "text": "Where is this?"},
                {"type": "input_image", "image_url": data_url},
            ]}
        ],
    )
    return response.output_text

def make_postcard(place, traveller_name):
    prompt = (
        f"A vintage travel postcard of {place}, Norway, bright colours, "
        f"with the text 'Greetings from Fjord Trips, {traveller_name}!'"
    )
    image = image_client.images.generate(
        model=os.environ["IMAGE_DEPLOYMENT"],
        prompt=prompt, size="1024x1024", n=1,
    )
    return base64.b64decode(image.data[0].b64_json)

if __name__ == "__main__":
    with open("data/media/photos/geiranger.jpg", "rb") as f:
        print(where_is_this(f.read()))
    with open("postcard.png", "wb") as f:
        f.write(make_postcard("Geirangerfjord", "Priya"))
    print("Saved postcard.png")