"""Module 14 · Quick evaluation: ask trip-agent every question in data/eval-set.csv and grade the answers.

Run:  python tests/run_eval.py
"""
import csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from agent_client import client, new_conversation, ask_agent  # noqa: E402

GRADER = os.environ.get("CHAT_DEPLOYMENT", "gpt-5-mini")
GRADER_INSTRUCTIONS = (
    "You are a strict grader. Reply with only PASS or FAIL. "
    "PASS if the answer contains all the expected facts (same numbers and names), even in different words. "
    "FAIL if a fact is missing or wrong."
)


def grade(question, expected, answer):
    response = client.responses.create(
        model=GRADER,
        instructions=GRADER_INSTRUCTIONS,
        input=f"Question: {question}\nExpected facts: {expected}\nAnswer: {answer}",
    )
    return response.output_text.strip().upper().startswith("PASS")


def run_quality():
    rows = list(csv.DictReader(open("data/eval-set.csv", encoding="utf-8")))
    failures = []
    for i, row in enumerate(rows, 1):
        answer = ask_agent(new_conversation(), row["query"])
        ok = grade(row["query"], row["ground_truth"], answer)
        print(f"{i:2}/{len(rows)} {'PASS' if ok else 'FAIL'}  {row['query']}")
        if not ok:
            failures.append((row["query"], row["ground_truth"], answer))
    print(f"\nQuality: {len(rows) - len(failures)}/{len(rows)} passed")
    for q, expected, answer in failures:
        print(f"\n- {q}\n  expected: {expected}\n  answer:   {answer[:300]}")
    return not failures


if __name__ == "__main__":
    run_quality()
