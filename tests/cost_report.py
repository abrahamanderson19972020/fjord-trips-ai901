"""Module 16 · Cost per conversation for two models.

Runs 10 typical traveller conversations with each deployment, adds up the tokens,
and multiplies by the price per million tokens.
CHECK THE PRICES: copy the current prices for your region from the Azure OpenAI pricing page
(azure.microsoft.com/pricing/details/cognitive-services/openai-service/). They change.
Run:  python tests/cost_report.py
"""
import csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from agent_client import client  # noqa: E402

# USD per 1 million tokens: (input, output). Example values: replace with today's prices.
PRICES = {
    os.environ.get("CHAT_DEPLOYMENT", "gpt-5-mini"): (0.25, 2.00),
    os.environ.get("CHEAP_DEPLOYMENT", "gpt-5-nano"): (0.05, 0.40),
}
BROCHURE = open("data/brochure.txt", encoding="utf-8").read()
INSTRUCTIONS = open("prompts/trip_planner.txt", encoding="utf-8").read() + \
    "\nUse only this brochure for trips, prices and policies:\n" + BROCHURE
GRADER = os.environ.get("CHAT_DEPLOYMENT", "gpt-5-mini")

rows = list(csv.DictReader(open("data/eval-set.csv", encoding="utf-8")))[:10]


def passes(question, expected, answer):
    r = client.responses.create(
        model=GRADER,
        instructions="Reply only PASS or FAIL. PASS if the answer contains all expected facts.",
        input=f"Question: {question}\nExpected facts: {expected}\nAnswer: {answer}",
    )
    return r.output_text.strip().upper().startswith("PASS")


print(f"{'Deployment':<16}{'Tokens in':>11}{'Tokens out':>12}{'Cost/conv (USD)':>17}{'Per 1,000 conv':>16}{'Pass rate':>11}")
for deployment, (price_in, price_out) in PRICES.items():
    tokens_in = tokens_out = passed = 0
    for row in rows:
        r = client.responses.create(model=deployment, instructions=INSTRUCTIONS, input=row["query"])
        tokens_in += r.usage.input_tokens
        tokens_out += r.usage.output_tokens
        passed += passes(row["query"], row["ground_truth"], r.output_text)
    cost = (tokens_in * price_in + tokens_out * price_out) / 1_000_000 / len(rows)
    print(f"{deployment:<16}{tokens_in // len(rows):>11}{tokens_out // len(rows):>12}{cost:>17.5f}{cost * 1000:>16.2f}{passed:>8}/{len(rows)}")
