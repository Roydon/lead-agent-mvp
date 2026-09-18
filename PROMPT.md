# Claude Code build prompt

Paste the block below into Claude Code, run inside this directory
(`~/freelancer-ai/mvp/40718977-end-end-work-agents-dashboard/`).

---

Build an MVP for one slice of a multi-agent business dashboard (lead classification + response drafting), scoped deliberately narrow given the budget and structured for free hosting:

1. A single Streamlit app (no separate backend) that classifies inbound leads/quotes (LLM-driven — Ollama by default, or OpenAI if the client supplies a key) into categories and drafts a response.
2. SQLite storage of leads with classification and drafted response.
3. A simple two-role view toggle within the same app (Admin sees all, Sales Agent sees assigned) showing the lead queue.
4. A `make demo` that runs 5 sample leads locally end-to-end and prints classification + draft response for each.
5. `requirements.txt` plus a `.streamlit/config.toml` (and a Hugging Face Spaces README header as an alternative) set up for one-click free-tier deployment, with both deploy paths documented in the README.
6. A README with a 60-second quickstart and the live public demo URL once deployed (see DEPLOY.md in this directory for the deploy steps).
7. A CI badge.
8. `docs/DECISIONS.md` explicitly scoping out the rest of the client's ask (data pipelines, forecasting agent, anomaly detection, full RBAC, executive summaries) as later phases, with a rough cost/timeline note for each.

Zero paid spend required — free-tier hosting only.

---

## Context for whoever (or whatever) picks this up

- **Client project:** https://www.freelancer.com/projects/ai-chatbot-development/End-End-Work-agents-Dashboard (id 40718977)
- **Client's full ask:** a web dashboard for two business divisions (metal trading, real estate) with role-based views, three data pipelines, analytics/reporting, workflow automation, and four AI agents (lead triage, price forecasting, executive summaries, anomaly detection).
- **What we're actually bidding:** only the lead-classification-and-response agent, as an honest first slice — the budget (₹12,500–₹37,500, ≈USD 130–391) can't fund the full platform. See `../../daily/2026-09-18.md` entry 3 for the full score card, budget-realism reasoning, and bid message.
- **Sample data:** none provided by the client yet — invent 5 plausible sample leads (a mix of metal-trading and real-estate inquiries) for the demo and `make demo`.
