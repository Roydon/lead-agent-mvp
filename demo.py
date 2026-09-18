"""Runs the 5 sample leads end-to-end and prints classification + draft response.
Used by `make demo`. Does not touch the Streamlit app's leads.db."""

from agent import classify_and_draft
from db import SAMPLE_LEADS


def main() -> None:
    for i, lead in enumerate(SAMPLE_LEADS, start=1):
        print(f"\n=== Lead {i}: {lead['sender']} ===")
        print(f"Message: {lead['text']}")
        result = classify_and_draft(lead["text"], sender=lead["sender"])
        print(f"Division:  {result['division']}")
        print(f"Category:  {result['category']}")
        print(f"Urgency:   {result['urgency']}")
        print(f"Draft response: {result['draft_response']}")


if __name__ == "__main__":
    main()
