# Decisions

## Scope

The client asked for a full multi-division platform: role-based dashboard,
three data pipelines, analytics/reporting, workflow automation, and four
AI agents (lead triage, price forecasting, executive summaries, anomaly
detection). Budget is ₹12,500–₹37,500 (≈USD 130–391), which cannot
realistically fund that scope.

This MVP bids only the highest-leverage slice: the lead-classification-
and-response agent. Everything else is scoped out as later phases — to be
filled in by Claude Code per PROMPT.md item 8, with a rough cost/timeline
note per phase:

- Price-forecasting agent — phase 2
- Executive-summary agent — phase 2
- Anomaly-detection agent — phase 2
- Full role-based access control (beyond the Admin/Sales-Agent toggle) — phase 2
- The three data-pipeline integrations (internal SQL/NoSQL, third-party APIs, spreadsheet uploads) — phase 2

## Architecture

- **LLM provider — Groq (free tier), not Ollama.** `PROMPT.md` originally
  specified Ollama as the default with OpenAI as a client-supplied-key
  fallback. In practice, Streamlit Community Cloud has no local Ollama
  daemon, so the deployed app needs a hosted API regardless. Groq's free
  tier (`llama-3.1-8b-instant`) avoids requiring the client (or us) to pay
  for an OpenAI key just to see the demo, which keeps the "zero paid
  spend" constraint intact end-to-end (local `make demo` and the deployed
  app use the same Groq path — no separate local/hosted branching).
- **Storage — SQLite (`leads.db`), single file, no server.** Sufficient
  for a demo-scale lead queue and needs no separate database
  provisioning, matching the free-hosting constraint.
- **Hosting — Streamlit Community Cloud only.** The Hugging Face Spaces
  fallback mentioned in the original prompt was dropped in favor of
  documenting one path well; Community Cloud requires a public GitHub
  repo (`github.com/Roydon/lead-agent-mvp`), which this project uses.
- **Role toggle** is a sidebar radio, not real auth — there's no login,
  just an Admin/Sales-Agent view filter. Real RBAC is explicitly phase 2
  (see below).
