# Deployment checklist

1. Upload this folder to a GitHub repository.
2. Deploy `app.py` on Streamlit Community Cloud.
3. Open **Settings → Secrets** and paste the secrets from `.streamlit/secrets.toml.example` with real values.
4. Restart/redeploy after changing secrets.
5. Open **About → Gemini connection diagnostic → Test Gemini Connection**.
6. Confirm **AI CONNECTED** appears in the sidebar.

If Gemini still fails, the About page now displays the actual provider error with the key redacted. This is more useful than the old generic `NO_API_KEY` message.
