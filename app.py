"""End-to-End AI Work agents & Dashboard — MVP slice: lead classification + response drafting."""

import streamlit as st

from agent import classify_and_draft
from db import AGENTS, get_leads, insert_lead, seed_if_empty

st.set_page_config(page_title="Lead Agent — Demo", page_icon="\U0001F4E5", layout="wide")

CATEGORY_LABELS = {
    "quote_request": "Quote request",
    "general_inquiry": "General inquiry",
    "urgent_complaint": "Urgent complaint",
    "spam": "Spam",
}
URGENCY_COLORS = {"high": "\U0001F534", "medium": "\U0001F7E1", "low": "\U0001F7E2"}


def render_lead(lead: dict) -> None:
    urgency_dot = URGENCY_COLORS.get(lead["urgency"], "")
    category_label = CATEGORY_LABELS.get(lead["category"], lead["category"])
    title = f"{urgency_dot} [{lead['division']}] {category_label} — {lead['sender'] or 'unknown sender'}"
    with st.expander(title):
        st.caption(f"Received {lead['created_at']} · assigned to {lead['assigned_agent']}")
        st.markdown("**Lead message:**")
        st.write(lead["raw_text"])
        st.markdown("**Drafted response:**")
        st.write(lead["draft_response"])


def main() -> None:
    try:
        seed_if_empty(classify_and_draft)
    except RuntimeError as e:
        st.error(str(e))
        st.stop()

    st.title("Lead classification & response agent — demo")

    with st.sidebar:
        st.header("View as")
        role = st.radio("Role", ["Admin", "Sales Agent"], label_visibility="collapsed")
        agent_filter = None
        if role == "Sales Agent":
            agent_filter = st.selectbox("Sales agent", AGENTS)

        st.divider()
        st.header("Submit a new lead")
        with st.form("new_lead"):
            sender = st.text_input("Sender email")
            text = st.text_area("Lead message", height=120)
            assigned = st.selectbox("Assign to", AGENTS, key="assign_new")
            submitted = st.form_submit_button("Classify & draft")
        if submitted and text.strip():
            with st.spinner("Classifying and drafting response..."):
                classification = classify_and_draft(text, sender=sender)
                insert_lead(text, classification, sender=sender, assigned_agent=assigned)
            st.success("Lead classified and added to the queue.")
            st.rerun()

    leads = get_leads(assigned_agent=agent_filter)

    st.subheader(f"{'All leads' if role == 'Admin' else f'Leads assigned to {agent_filter}'} ({len(leads)})")

    if not leads:
        st.info("No leads yet.")
        return

    for lead in leads:
        render_lead(lead)


if __name__ == "__main__":
    main()
