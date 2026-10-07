# NavaBharat AI — Supabase production setup

## 1. Create/open the Supabase project

Use the project that will serve `navabhratai.racharlgpt.in`.

## 2. Run the database/storage SQL

Open **Supabase → SQL Editor** and run the complete file:

`supabase/schema.sql`

Do not run only selected statements.

## 3. Frontend Supabase values

Edit `config.js`:

- `SUPABASE_URL` = your Supabase project URL
- `SUPABASE_ANON_KEY` = your Supabase publishable/anon key

These two values are allowed in the browser. **Never put provider secrets in `config.js`.**

## 4. Required Edge Function secrets

Set these in **Supabase → Edge Functions → Secrets** (or with the Supabase CLI):

```text
SUPABASE_SERVICE_ROLE_KEY=<your server-side service role key>
RAZORPAY_KEY_ID=<your Razorpay key id>
RAZORPAY_KEY_SECRET=<your Razorpay secret>
GEMINI_API_KEY=<your Gemini key>
GEMINI_API_KEY_2=<your second Gemini key, if available>
ACESTEP_API_KEY=<your existing ACE-Step key>
APIFRAME_API_KEY=<your existing APIFrame key>
ADMIN_API_TOKEN=<long random admin token>
SITE_URL=https://navabhratai.racharlgpt.in
```

### Optional

```text
GEMINI_API_KEY_3=<optional third Gemini key>
MUSIC_PROVIDER_ORDER=acestep,gemini,apiframe
GEMINI_MODEL=<optional Gemini text model override>
```

### Important ACE-Step/APIFrame clarification

You **do not** need to provide:

```text
ACESTEP_BASE_URL
ACESTEP_MODEL
APIFRAME_BASE_URL
```

The application contains the provider defaults internally. Your existing API keys are sufficient for the migrated provider configuration.

## 5. Deploy all Edge Functions

From the project root, after linking the Supabase project, deploy every function under `supabase/functions/`.

The included `supabase/config.toml` sets `verify_jwt=false` because the customer flow deliberately has no customer login. Admin functions still require `x-admin-token`.

## 6. Admin token

Choose a long random value and set it as `ADMIN_API_TOKEN`.

Enter that value only in the Admin page when you need to:

- upload RacharlaGPT music
- upload authorized ringtones
- deactivate/unpublish items
- refresh authorized catalog
- test ACE-Step/Gemini/APIFrame

Do not put the admin token in GitHub or `config.js`.

## 7. Razorpay

Use the Razorpay credentials in Supabase secrets only.

The application creates Payment Links server-side and returns the customer to:

`https://navabhratai.racharlgpt.in/?payment=done&order_id=...`

The server verifies the Payment Link with Razorpay before issuing a download entitlement.

## 8. Cleanup

`cleanup` is protected by `ADMIN_API_TOKEN`.

Schedule it daily using Supabase scheduled infrastructure or another trusted scheduler. It:

- removes expired download entitlements
- removes old unpaid orders
- does **not** delete purchased ringtone/song source files after 30 days

## 9. GitHub Pages

Upload the **contents** of the release ZIP to the repository root. `index.html` must be at repository root, not inside `web/`.

Enable GitHub Pages from the `main` branch/root.

The ZIP includes:

- `CNAME` → `navabhratai.racharlgpt.in`
- `index.html`
- `styles.css`
- `app.js`
- `config.js`
- `manifest.webmanifest`
- `sw.js`
- `assets/`
- `supabase/`

## 10. Cloudflare

Create the DNS record for the exact host:

`navabhratai.racharlgpt.in`

Point it to the GitHub Pages hostname used by your repository. Keep DNS-only while GitHub verifies the custom domain; enable proxying afterward only if desired and compatible with your Pages setup.

## 11. First production test order

1. Open the domain and confirm the Home page.
2. Open every navigation page.
3. Run AI Solve.
4. Generate original lyrics.
5. Test each music provider from Admin.
6. Generate a short ringtone and confirm preview.
7. Generate a song and confirm preview.
8. Create a Razorpay test payment for a generated asset.
9. Confirm payment return and automatic download.
10. Recover the order by Order ID in Premium.
11. Upload one authorized ringtone and test preview/payment/download.
12. Upload one RacharlaGPT music track and test playback.
13. Test Design preview → Razorpay ₹9 → no-watermark HD export.
14. Test Video Studio MP3 extraction and Reel Builder.
15. Test Current Affairs RSS and quiz.
16. Test Jobs/Exam AI and RSS fallback.
17. Test mobile sidebar and refresh/update bar.
18. Check GA4 Realtime and Monetag after the live domain is serving.
