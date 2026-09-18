# Deploying free, for the client to test live

Streamlit Community Cloud is the default and only path documented here —
it needs a public GitHub repo, which this project has
(`github.com/Roydon/lead-agent-mvp`).

## Streamlit Community Cloud

1. Go to https://share.streamlit.io, sign in with GitHub.
2. "New app" → repo `Roydon/lead-agent-mvp`, branch `main`, main file
   `app.py`.
3. Before/after deploying, open the app's "Secrets" panel and add:
   ```toml
   GROQ_API_KEY = "your-key-here"
   ```
   Get a free key at https://console.groq.com/keys.
4. Deploy. You get a `*.streamlit.app` URL — that's the link to paste
   into the bid message and into `README.md`'s "Live demo" section.

## Before sending the link to the client

- Confirm the two-role toggle and the 5 seeded sample leads all show up
  correctly against the *deployed* app, not just locally — Streamlit
  Cloud's Python version and package resolution can differ from your
  local env.
- Update `README.md`'s "Live demo" line with the confirmed URL.
