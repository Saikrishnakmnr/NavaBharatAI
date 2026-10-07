# NavaBharat AI — no Streamlit deployment

1. Upload the CONTENTS of this folder to the GitHub Pages repository root. Do not put them in `web/`.
2. Keep `supabase/` in the repository because it contains the SQL and Edge Functions.
3. GitHub Pages: Settings → Pages → Deploy from branch → `main` → `/root`.
4. Custom domain: `navabhratai.racharlgpt.in`. The included `CNAME` already contains this hostname.
5. Cloudflare DNS: CNAME `navabhratai` → your GitHub Pages hostname. Start DNS-only while GitHub verifies the custom domain.
6. In `config.js`, put only the Supabase project URL and anon/public key. Never put Razorpay secret, Gemini, ACE or APIFrame keys here.
7. In Supabase, run `supabase/schema.sql` and create storage buckets: `generated-audio`, `ringtone-full`, `ringtone-preview`. Keep full files private.
8. Deploy every folder under `supabase/functions/` as a Supabase Edge Function.
9. Set the secrets from `supabase/SECRETS.example` in Supabase Edge Functions. Keys stay server-side.
10. Run `refresh-catalog` only for sources you are legally allowed to redistribute.
11. Schedule `cleanup` daily. It removes expired entitlements and old unpaid orders; it does NOT delete purchased source ringtones.
12. Use `SUPABASE_SETUP.md` for the complete setup and verification sequence. The release includes the full feature audit in `FINAL_AUDIT_MATRIX.md`.

Important: the package intentionally contains no Streamlit runtime, `.streamlit` directory, `requirements.txt`, or `app.py`.


## Admin controls
Set `ADMIN_API_TOKEN` as a Supabase Edge Function secret. Open the Admin page in the app, enter that token only when managing your own content, then upload music/ringtones, set ringtone price (minimum ₹10), refresh the authorized catalog, or deactivate/unpublish items. Never place the token in `config.js`.

## Razorpay navigation
Payment creation now navigates the current browser tab directly to the Razorpay payment link after the server creates it, avoiding mobile popup blockers.


FINAL v13 CHECK: Deploy Supabase functions with the included supabase/config.toml. This file sets verify_jwt=false per function because the public customer flow has no Supabase Auth login. Admin endpoints additionally require x-admin-token. Do not turn JWT verification back on for these endpoints unless the app is redesigned for authenticated customers.
