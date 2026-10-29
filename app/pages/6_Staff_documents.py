"""Module 12 · Staff documents: read bookings and receipts automatically."""
import pandas as pd
import streamlit as st
from extract import extract, extract_bytes, REPO

st.set_page_config(page_title="Fjord Trips · Staff documents", page_icon="📄")
st.title("Staff · Documents")
st.caption("Content Understanding reads the document and fills in the fields. Values under 80% confidence are flagged for a human to check.")

SAMPLES = [f"bookings/booking-{n}.pdf" for n in range(1042, 1047)] + \
          [f"receipts/receipt-{n:02d}.jpg" for n in range(1, 6)]

source = st.radio("Document", ["Pick a sample", "Upload a file"], horizontal=True)
fields = None
if source == "Pick a sample":
    file = st.selectbox("Sample file", SAMPLES)
    analyzer = "prebuilt-receipt" if file.startswith("receipts") else "fjord-booking"
    if st.button("Extract fields", type="primary"):
        with st.spinner(f"Analysing with {analyzer}..."):
            fields = extract(f"{REPO}/{file}", analyzer)
else:
    upload = st.file_uploader("Booking PDF or receipt photo", type=["pdf", "jpg", "jpeg", "png"])
    if upload:
        analyzer = "fjord-booking" if upload.type == "application/pdf" else "prebuilt-receipt"
        with st.spinner(f"Analysing with {analyzer}..."):
            fields = extract_bytes(upload.getvalue(), analyzer, upload.type)

if fields:
    rows = [{"field": name,
             "value": str(value),
             "confidence": None if conf is None else round(conf, 2),
             "check": "⚠️ check" if conf is not None and conf < 0.8 else ""}
            for name, (value, conf) in fields.items()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
