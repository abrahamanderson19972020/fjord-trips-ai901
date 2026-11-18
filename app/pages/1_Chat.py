"""Chat with trip-agent (Module 8, moved to its own page in Module 9)."""
import streamlit as st
import ui
from agent_client import new_conversation, ask_agent

st.set_page_config(page_title="Fjord Trips · Chat", page_icon="⛰️")
ui.style()
ui.hero("Trip agent", "Fjord Trips assistant", "Ask about our trips, prices, dates and what to expect in Norway.", photo="geiranger.jpg")
ui.notice("You're chatting with an AI assistant. A travel advisor confirms all bookings.")

if "conv" not in st.session_state:
    st.session_state.conv = new_conversation()
    st.session_state.messages = []

AVATARS = {"user": "🧑", "assistant": "⛰️"}
if not st.session_state.messages:
    ui.tips(["Which trips do you have in May?", "Compare the Northern Lights Week and Lofoten Light",
             "What's included in the Fjord Explorer?"])

for role, text in st.session_state.messages:
    st.chat_message(role, avatar=AVATARS[role]).write(text)

if question := st.chat_input("Ask about trips in Norway"):
    st.chat_message("user", avatar=AVATARS["user"]).write(question)
    with st.spinner("Thinking..."):
        answer = ask_agent(st.session_state.conv, question)
    st.chat_message("assistant", avatar=AVATARS["assistant"]).write(answer)
    st.session_state.messages += [("user", question), ("assistant", answer)]
ui.sidebar_note()
