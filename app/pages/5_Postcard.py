"""Module 11 · Make a postcard with an image generation model."""
import streamlit as st
from vision import make_postcard

st.set_page_config(page_title="Fjord Trips · Postcard", page_icon="🖼️")
st.title("Make a postcard")
st.caption("AI-generated image. Describe a place, add your name, and a new postcard is created.")

place = st.text_input("Place in Norway", "Geirangerfjord")
name = st.text_input("Your name", "Priya")
if st.button("Generate postcard", type="primary"):
    with st.spinner("Creating your postcard (about 20 seconds)..."):
        image = make_postcard(place, name)
    st.image(image, caption=f"AI-generated postcard of {place}")
    st.download_button("Download postcard", image, file_name="fjord-trips-postcard.png", mime="image/png")
