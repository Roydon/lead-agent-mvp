# End-to-End AI Work agents & Dashboard — MVP slice (lead classification agent)

![CI](https://github.com/Roydon/lead-agent-mvp/actions/workflows/ci.yml/badge.svg)

## What this is

A narrow, honest first slice of a much bigger client ask (Freelancer.com
project [40718977](https://www.freelancer.com/projects/ai-chatbot-development/End-End-Work-agents-Dashboard)):
just the lead-classification-and-response agent, as a single Streamlit
app, deployable free. See `docs/DECISIONS.md` for what's in and out of
scope.

## 60-second quickstart

```bash
pip install -r requirements.txt
export GROQ_API_KEY=your-key-here   # free key: https://console.groq.com/keys
make demo                           # runs 5 sample leads end-to-end, prints results
streamlit run app.py                # launches the full app locally
```

## What it does

- Classifies inbound leads (metal-trading or real-estate division; quote
  request / general inquiry / urgent complaint / spam; urgency) using the
  Groq API (free tier, `llama-3.1-8b-instant`).
- Drafts a short reply for each lead.
- Stores everything in SQLite (`leads.db`).
- Two-role view toggle in the sidebar: **Admin** sees every lead, **Sales
  Agent** sees only leads assigned to them.

## Live demo

Not deployed yet — see `DEPLOY.md`. Once live, put the URL here and in
the bid message.
