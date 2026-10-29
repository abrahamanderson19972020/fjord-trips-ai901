"""Module 9 · Review insights: what travellers say about Fjord Trips."""
import pandas as pd
import streamlit as st
from language import load_reviews, analyse, summarise

st.set_page_config(page_title="Fjord Trips · Review insights", page_icon="📊")
st.title("Review insights")
st.caption("Staff page · 50 traveller reviews analysed with Azure Language")


@st.cache_data(show_spinner="Analysing reviews with Azure Language...")
def run():
    reviews = load_reviews()
    sentiments, phrases, places = analyse(reviews)
    return len(reviews), dict(sentiments), phrases, places, summarise(reviews)


count, sentiments, phrases, places, summary = run()

cols = st.columns(4)
for col, label in zip(cols, ["positive", "neutral", "negative", "mixed"]):
    col.metric(label.capitalize(), sentiments.get(label, 0))

st.subheader("Top topics")
st.bar_chart(pd.DataFrame(phrases, columns=["topic", "mentions"]).set_index("topic"))

st.subheader("Most mentioned places")
st.write(", ".join(f"{name} ({n})" for name, n in places))

st.subheader("Summary for the team")
st.write(summary)
