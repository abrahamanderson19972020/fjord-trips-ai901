"""Module 12 · Information extraction with Content Understanding.

Uses the custom analyzer `fjord-booking` (created in the Foundry portal) and the prebuilt receipt analyzer.
Run:  python app/extract.py
"""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput

load_dotenv()
client = ContentUnderstandingClient(
    endpoint=os.environ["CU_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
# Public URL of the data folder in your GitHub repo (Content Understanding reads files by URL).
REPO = os.environ.get(
    "DATA_BASE_URL",
    "https://raw.githubusercontent.com/abrahamanderson19972020/fjord-trips-ai901/main/data",
)

def extract(file_url, analyzer_id="fjord-booking"):
    poller = client.begin_analyze(analyzer_id=analyzer_id,
                                  inputs=[AnalysisInput(url=file_url)])
    result = poller.result()
    fields = result.contents[0].fields
    return {name: (f.value, f.confidence) for name, f in fields.items()}

def extract_bytes(data, analyzer_id="fjord-booking", content_type="application/octet-stream"):
    """Same as extract(), for an uploaded file instead of a URL."""
    poller = client.begin_analyze_binary(analyzer_id=analyzer_id, binary_input=data,
                                         content_type=content_type)
    fields = poller.result().contents[0].fields
    return {name: (f.value, f.confidence) for name, f in fields.items()}

if __name__ == "__main__":
    for name, (value, conf) in extract(f"{REPO}/bookings/booking-1042.pdf").items():
        flag = "  <- check" if conf is not None and conf < 0.8 else ""
        print(f"{name}: {value} ({conf:.2f}){flag}" if conf is not None else f"{name}: {value}")
    print(extract(f"{REPO}/receipts/receipt-01.jpg", "prebuilt-receipt"))
