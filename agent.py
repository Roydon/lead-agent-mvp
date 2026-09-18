"""Lead classification + response-drafting agent, backed by Groq's free-tier API."""

import json
import os

from groq import Groq

MODEL = "llama-3.1-8b-instant"

DIVISIONS = ["metal_trading", "real_estate", "unknown"]
CATEGORIES = ["quote_request", "general_inquiry", "urgent_complaint", "spam"]
URGENCIES = ["low", "medium", "high"]

SYSTEM_PROMPT = f"""You triage inbound leads for a company with two divisions: \
metal trading and real estate. For each lead, classify it and draft a short, \
professional reply.

Respond with ONLY a JSON object with these exact keys:
- "division": one of {DIVISIONS}
- "category": one of {CATEGORIES}
- "urgency": one of {URGENCIES}
- "draft_response": a 2-4 sentence professional reply to the lead

"spam" category applies to irrelevant or clearly non-business messages. \
"urgent_complaint" applies to existing customers reporting a problem that \
needs fast attention. "quote_request" applies to someone asking for pricing \
or availability. "general_inquiry" covers everything else business-relevant."""


def _get_api_key() -> str:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        try:
            import streamlit as st

            key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            key = None
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Export it as an environment variable "
            "locally, or add it to Streamlit Secrets when deployed. Get a "
            "free key at https://console.groq.com/keys"
        )
    return key


_client = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=_get_api_key())
    return _client


def classify_and_draft(lead_text: str, sender: str = "") -> dict:
    """Classify a lead and draft a response. Returns a dict with division,
    category, urgency, and draft_response."""
    client = _get_client()
    user_content = f"Sender: {sender}\nLead message:\n{lead_text}" if sender else lead_text

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    result = json.loads(completion.choices[0].message.content)

    if result.get("division") not in DIVISIONS:
        result["division"] = "unknown"
    if result.get("category") not in CATEGORIES:
        result["category"] = "general_inquiry"
    if result.get("urgency") not in URGENCIES:
        result["urgency"] = "low"
    result.setdefault("draft_response", "")

    return result
