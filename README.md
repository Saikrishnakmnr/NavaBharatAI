# NavaBharat AI — RacharlaGPT

Production release 13.0.0: pure HTML/CSS/JavaScript frontend + Supabase Edge Functions. No Streamlit runtime is shipped.

Brand: NavaBharat AI, a product of RacharlaGPT.
Developer: Saikrishna Racharla.
Contact: racharlagpt@gmail.com · Karimnagar, Telangana, India.
YouTube: https://youtube.com/@racharlagpt

## Start here

1. Read `FINAL_AUDIT_MATRIX.md`.
2. Read `SUPABASE_SETUP.md`.
3. Put the contents of this package at the GitHub repository root.
4. Put only the Supabase URL + browser key in `config.js`.
5. Keep Gemini, ACE-Step, APIFrame, Razorpay and admin secrets in Supabase Edge Function secrets.

### Provider-key clarification

ACE-Step requires only the existing ACE-Step API key. APIFrame requires only the existing APIFrame API key. The release does not require `ACESTEP_BASE_URL`, `ACESTEP_MODEL`, or `APIFRAME_BASE_URL` secrets.
