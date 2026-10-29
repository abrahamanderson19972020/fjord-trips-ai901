"""Module 3 · Count tokens.

Shows how a model splits text into tokens.
Run:  python concepts/tokens.py "Plan a trip to Bergen"
"""
import sys

import tiktoken

# o200k_base is the tokenizer used by the GPT-4o and GPT-5 model families.
encoding = tiktoken.get_encoding("o200k_base")

text = " ".join(sys.argv[1:]) or "Plan a trip to Bergen"
tokens = encoding.encode(text)

print(f"Text:   {text[:80]}{'...' if len(text) > 80 else ''}")
print(f"Tokens: {len(tokens)}")
print(f"Words:  {len(text.split())}")
print("Pieces:", " | ".join(encoding.decode([t]) for t in tokens[:40]))
if len(tokens) > 40:
    print(f"... and {len(tokens) - 40} more tokens")
