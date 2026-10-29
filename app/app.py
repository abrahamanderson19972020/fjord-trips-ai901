"""Fjord Trips · home page. Run from the project folder:  streamlit run app/app.py"""
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Fjord Trips", page_icon="⛰️")
st.title("⛰️ Fjord Trips")
st.write("An AI travel assistant for a (fictional) Norwegian travel agency, built in Microsoft Foundry.")
st.info("You're using an AI assistant. A travel advisor confirms all bookings.")

PAGES = Path(__file__).parent / "pages"
SECTIONS = {
    "For travellers": [
        ("1_Chat.py", "Chat with the trip agent", "💬"),
        ("3_Voice.py", "Ask with your voice (English or Hindi)", "🎙️"),
        ("4_Photo.py", "Where is this? Identify a photo", "📷"),
        ("5_Postcard.py", "Make a postcard", "🖼️"),
    ],
    "For staff": [
        ("2_Review_insights.py", "Review insights", "📊"),
        ("6_Staff_documents.py", "Read bookings and receipts", "📄"),
    ],
}
# Each module adds a page; only show the pages that exist so far.
for section, pages in SECTIONS.items():
    st.subheader(section)
    for file, label, icon in pages:
        if (PAGES / file).exists():
            st.page_link(f"pages/{file}", label=label, icon=icon)
