"""Module 11 · Make a postcard with an image generation model."""
import streamlit as st
import ui
from vision import make_postcard

st.set_page_config(page_title="Fjord Trips · Postcard", page_icon="🖼️")
ui.style()
ui.hero("Postcard", "Make a postcard", "AI-generated image. Describe a place, add your name, and a new postcard is created.",
        photo="lofoten.jpg")

left, right = st.columns(2)
place = left.text_input("Place in Norway", "Lofoten")
name = right.text_input("Traveller's name", "Maria")

if st.button("Generate postcard", type="primary"):
    with st.spinner("Creating your postcard... (10–30 seconds)"):
        image = make_postcard(place, name)
    st.image(image, caption=f"Greetings from {place}")
    st.download_button("Download postcard", image, file_name="fjord_trips_postcard.png", mime="image/png")
ui.sidebar_note()
