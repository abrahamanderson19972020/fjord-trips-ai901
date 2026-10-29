"""Module 11 · Vision (photo in, words out) and image generation (words in, new image out).

Run:  python app/vision.py   (uses data/media/geiranger.jpg: add your own photo first)
"""
import os, base64
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
project = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
                          credential=DefaultAzureCredential())
client = project.get_openai_client()

def where_is_this(image_bytes, mime="image/jpeg"):
    data_url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
    response = client.responses.create(
        model=os.environ["CHAT_DEPLOYMENT"],
        instructions="Identify the place in Norway and suggest one Fjord Trips trip. Max 80 words.",
        input=[{"role": "user", "content": [
            {"type": "input_text", "text": "Where is this?"},
            {"type": "input_image", "image_url": data_url},
        ]}],
    )
    return response.output_text

def make_postcard(place, traveller_name):
    prompt = (f"A vintage travel postcard of {place}, Norway, bright colours, "
              f"with the text 'Greetings from Fjord Trips, {traveller_name}!'")
    image = client.images.generate(model=os.environ["IMAGE_DEPLOYMENT"],
                                   prompt=prompt, size="1024x1024", n=1)
    return base64.b64decode(image.data[0].b64_json)

if __name__ == "__main__":
    with open("data/media/geiranger.jpg", "rb") as f:
        print(where_is_this(f.read()))
    with open("postcard.png", "wb") as f:
        f.write(make_postcard("Geirangerfjord", "Priya"))
    print("Saved postcard.png")
