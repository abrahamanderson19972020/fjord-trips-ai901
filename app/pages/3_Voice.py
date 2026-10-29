"""Module 10 · Voice: ask a question out loud, hear the answer."""
import tempfile
from pathlib import Path

import streamlit as st
from agent_client import new_conversation, ask_agent
from speech import listen, speak

st.set_page_config(page_title="Fjord Trips · Voice", page_icon="🎙️")
st.title("Ask with your voice")
st.info("You're talking to an AI assistant. A travel advisor confirms all bookings.")

LANGUAGES = {"English": "en-US", "हिन्दी (Hindi)": "hi-IN"}
language = LANGUAGES[st.radio("Language", list(LANGUAGES), horizontal=True)]

recording = st.audio_input("Record your question")
if recording:
    folder = Path(tempfile.mkdtemp())
    question_file, answer_file = folder / "question.wav", folder / "answer.wav"
    question_file.write_bytes(recording.getvalue())
    with st.spinner("Listening..."):
        question = listen(language, wav_file=str(question_file))
    st.write(f"**You said:** {question or '(nothing recognised, please try again)'}")
    if question:
        if "conv" not in st.session_state:
            st.session_state.conv = new_conversation()
        prompt = question if language == "en-US" else question + "\n(Answer in Hindi.)"
        with st.spinner("Thinking..."):
            answer = ask_agent(st.session_state.conv, prompt)
        st.write(f"**Assistant:** {answer}")
        speak(answer, language, out_file=str(answer_file))
        st.audio(answer_file.read_bytes(), format="audio/wav", autoplay=True)
