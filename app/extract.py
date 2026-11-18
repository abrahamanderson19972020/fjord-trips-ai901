"""Module 12 Â· Information extraction with Content Understanding.

Uses our custom analyzer `fjordbooking` (built in Content Understanding Studio)
and the prebuilt receipt analyzer.
Run:  python app/extract.py
"""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput

load_dotenv(override=True)   # .env wins over old values in the terminal
REPO = os.environ["DATA_BASE_URL"]          # public data folder on GitHub

client = ContentUnderstandingClient(
    endpoint=os.environ["CU_ENDPOINT"],      # Sweden Central resource
    credential=DefaultAzureCredential(),     # your az login, no key
)

def _fields(result):
    fields = result.contents[0].fields or {}
    return {name: (field.value, field.confidence) for name, field in fields.items()}

def extract(file_url, analyzer_id="fjordbooking"):
    """Analyze a file that Azure can download from a URL."""
    poller = client.begin_analyze(analyzer_id=analyzer_id, 
                                  inputs=[AnalysisInput(url=file_url)])
    return _fields(poller.result())

def extract_bytes(data, analyzer_id="fjordbooking", content_type="application/pdf"):
    """Analyze a file you already have in memory for an upload."""
    poller = client.begin_analyze_binary(analyzer_id=analyzer_id, 
                                         binary_input=data, content_type=content_type)
    return _fields(poller.result())

def show(title, fields):
    print(f"\n{title}")
    for name, (value, conf) in fields.items():
        if isinstance(value, (list, dict)):   # skip tables such as receipt line items
            continue
        score = "n/a" if conf is None else f"{conf:.2f}"
        flag = "  <- check" if conf is not None and conf < 0.8 else ""
        print(f"  {name}: {value} ({score}){flag}")

if __name__ == "__main__":
    show("Booking 1042", extract(f"{REPO}/bookings/booking-1042.pdf"))
    show("Booking 1043", extract(f"{REPO}/bookings/booking-1043.pdf"))
    show("Receipt 01", extract(f"{REPO}/receipts/receipt-01.jpg", "prebuilt-receipt"))
