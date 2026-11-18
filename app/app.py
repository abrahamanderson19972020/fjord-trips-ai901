"""Fjord Trips · home page. Run from the project folder:  streamlit run app/app.py"""
from pathlib import Path

import streamlit as st
import ui

st.set_page_config(page_title="Fjord Trips", page_icon="⛰️")
ui.style()
ui.hero("Norway · fjords · northern lights", "⛰️ Fjord Trips",
        "An AI travel assistant for a (fictional) Norwegian travel agency, built in Microsoft Foundry.",
        photo="lofoten.jpg", small=False)
ui.notice("You're using an AI assistant. A travel advisor confirms all bookings.")

PAGES = Path(__file__).parent / "pages"
SECTIONS = {
    "For travellers": [
        ("1_Chat.py", "Chat with the trip agent", "💬", "Ask about trips, prices, dates and the weather.", "geiranger.jpg"),
        ("3_Voice.py", "Ask with your voice (English or Norwegian)", "🎙️", "Speak your question and hear the answer.", "flam.jpg"),
        ("4_Photo.py", "Where is this? Identify a photo", "📷", "Upload a photo from Norway and find the place.", "bergen-bryggen.jpg"),
        ("5_Postcard.py", "Make a postcard", "🖼️", "Create your own AI postcard from Norway.", "lofoten.jpg"),
    ],
    "For staff": [
        ("2_Review_insights.py", "Review insights", "📊", "What travellers say, analysed with Azure Language.", None),
        ("6_Staff_documents.py", "Read bookings and receipts", "📄", "Extract fields from bookings and receipts.", None),
    ],
}
NOTES = {"For travellers": "plan your trip", "For staff": "behind the scenes"}
# Each module adds a page; only show the pages that exist so far.
for section, pages in SECTIONS.items():
    pages = [p for p in pages if (PAGES / p[0]).exists()]
    if not pages:
        continue
    ui.section(section, NOTES[section])
    cols = st.columns(2)
    for i, (file, label, icon, text, photo) in enumerate(pages):
        with cols[i % 2]:
            with st.container(border=True):
                ui.card_top(text, photo, icon)
                st.page_link(f"pages/{file}", label=label, icon=icon)
ui.sidebar_note()
ui.footer()
