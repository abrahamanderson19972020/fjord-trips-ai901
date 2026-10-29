"""Module 9 · Text analysis with Azure Language: sentiment, key phrases, places and a summary.

Test it:  python app/language.py
"""
import os, csv
from collections import Counter
from dotenv import load_dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()
client = TextAnalyticsClient(
    endpoint=os.environ["LANGUAGE_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["LANGUAGE_KEY"]),
)

def load_reviews(path="data/reviews.csv"):
    with open(path, encoding="utf-8") as f:
        return [row["text"] for row in csv.DictReader(f)]

def in_batches(items, size=10):
    for i in range(0, len(items), size):
        yield items[i:i + size]

def analyse(reviews):
    sentiments, phrases, places = Counter(), Counter(), Counter()
    for batch in in_batches(reviews):
        for doc in client.analyze_sentiment(batch):
            sentiments[doc.sentiment] += 1
        for doc in client.extract_key_phrases(batch):
            phrases.update(p.lower() for p in doc.key_phrases)
        for doc in client.recognize_entities(batch):
            places.update(e.text for e in doc.entities if e.category == "Location")
    return sentiments, phrases.most_common(8), places.most_common(5)

def summarise(reviews):
    poller = client.begin_abstract_summary([" ".join(reviews[:20])])
    for doc in poller.result():
        return doc.summaries[0].text

if __name__ == "__main__":
    reviews = load_reviews()
    s, p, l = analyse(reviews)
    print("Sentiment:", dict(s))
    print("Top topics:", p)
    print("Top places:", l)
    print("Summary:", summarise(reviews))
