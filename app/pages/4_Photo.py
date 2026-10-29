"""Module 11 · Where is this? Upload a photo of Norway."""
import streamlit as st
from vision import where_is_this

st.set_page_config(page_title="Fjord Trips · Where is this?", page_icon="📷")
st.title("Where is this?")
st.caption("Upload a photo from Norway. A multimodal model identifies the place and suggests a trip.")

photo = st.file_uploader("Photo", type=["jpg", "jpeg", "png"])
if photo:
    st.image(photo, use_container_width=True)
    with st.spinner("Looking at your photo..."):
        st.write(where_is_this(photo.getvalue(), photo.type))
