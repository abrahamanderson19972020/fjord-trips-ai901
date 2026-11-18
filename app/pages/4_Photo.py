"""Module 11 · Where is this? Upload a photo of Norway."""
import streamlit as st
import ui
from vision import where_is_this

st.set_page_config(page_title="Fjord Trips · Where is this?", page_icon="📷")
ui.style()
ui.hero("Photo", "Where is this?", "Upload a photo from Norway. A multimodal model identifies the place and suggests a trip.",
        photo="bergen-bryggen.jpg")

photo = st.file_uploader("Photo", type=["jpg", "jpeg", "png"])

if photo:
    left, right = st.columns([1, 1], gap="large")
    left.image(photo, use_container_width=True)
    with right:
        with st.spinner("Looking at your photo..."):
            st.write(where_is_this(photo.getvalue(), photo.type))
ui.sidebar_note()
