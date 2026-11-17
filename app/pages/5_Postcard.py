"""Module 11 · Make a postcard with an image generation model."""
import streamlit as st
from vision import make_postcard

st.set_page_config(page_title="Fjord Trips · Postcard", page_icon="🖼️")
st.title("Make a postcard")
st.caption("AI-generated image. Describe a place, add your name, and a new postcard is created.")

place = st.text_input("Place in Norway", "Lofoten")
name = st.text_input("Traveller's name", "Maria")

if st.button("Generate postcard", type="primary"):
    with st.spinner("Creating your postcard... (10–30 seconds)"):
        image = make_postcard(place, name)
    st.image(image, caption=f"Greetings from {place}")
    st.download_button("Download postcard", image, file_name="fjord_trips_postcard.png", mime="image/png")
