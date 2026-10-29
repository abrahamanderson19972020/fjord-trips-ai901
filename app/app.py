import streamlit as st
from agent_client import new_conversation, ask_agent

st.set_page_config(page_title="Fjord Trips", page_icon="⛰️")
st.title("Fjord Trips assistant")
st.info("You're chatting with an AI assistant. A travel advisor confirms all bookings.")

if "conv" not in st.session_state:
    st.session_state.conv = new_conversation()
    st.session_state.messages = []

for role, text in st.session_state.messages:
    st.chat_message(role).write(text)

if question := st.chat_input("Ask about trips in Norway"):
    st.chat_message("user").write(question)
    answer = ask_agent(st.session_state.conv, question)
    st.chat_message("assistant").write(answer)
    st.session_state.messages += [("user", question), ("assistant", answer)]
