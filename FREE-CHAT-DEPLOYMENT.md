# NavaBharat AI 16.2 — Free Chat update

This is an update to the existing app, not a new website. It adds free General,
Student and Astro chat. No login or Pro plan is introduced. Existing music,
payments, purchase recovery, promotions and their prices are preserved.
No live deployment or DNS change has been made.

## Address: keep the working spelling

The CNAME, configuration and working app use **navabharatai.racharlagpt.in**,
with `ai` after `navabharat`. The address without `ai` returned a 502 in our browser.
Do not replace the existing CNAME accidentally.

## Deploy in this order, to the existing project

1. Keep the current Git commit/deployment as a rollback point.
2. Run only `supabase/FREE_CHAT_SETUP.sql` in the existing Supabase SQL Editor.
   It adds a private quota table and service-role-only function. No existing
   customer, order, music or advertising tables are altered or dropped.
3. Deploy only `supabase/functions/ai-text/index.ts` to the existing `ai-text`
   Edge Function, retaining its current `verify_jwt=false` setting. Keep all
   provider keys and the service-role key in Edge Function secrets.
   CLI option: `supabase functions deploy ai-text --project-ref YOUR_PROJECT_REF`.
   Dashboard option: replace the complete `ai-text` function code and deploy.
4. Check the new function in staging, including maintenance and quota behavior.
5. Upload the changed frontend files together at the existing repository root,
   beside index.html. Do not put the enclosing ZIP folder inside the root.
6. Let the existing hosting deployment finish. Refresh the app/service worker.
   Check `/?page=chat`, `/?page=solve` and `/?page=astro` on desktop and mobile.

The existing `nava_site_settings` row with id=1 must remain available; the new
chat reuses its maintenance flag. A missing gate or quota function fails closed
with CHAT_GATE_UNAVAILABLE. It does not silently make unbounded requests.

Do not redeploy older media/payment functions or rerun historical repair SQL for
this update. This guide takes precedence over older deployment notes in the ZIP.

## Exact change scope

| File | Change |
| --- | --- |
| chat.js, chat.css | New isolated messaging UI, history, language and exports |
| app.js | Add chat/astro routes; upgrade existing solve route to Student Chat |
| index.html | Load the two new frontend files |
| config.js | APP_VERSION only; existing public config preserved |
| version.json | Release 16.2.0 |
| sw.js | New assets; static-only cache, excluding APIs/maintenance/payments |
| supabase/functions/ai-text/index.ts | New chat types and bounded context; old task contract preserved |
| supabase/FREE_CHAT_SETUP.sql | New private atomic request counters |
| tests/free-chat.test.mjs | Reproducible tests without credentials |

The three new API tasks are `chat`, `student_chat`, `astro_chat`. They send real
conversation roles to providers. They use your existing Groq, OpenRouter and
Gemini secrets and AI_TEXT_PRIMARY preference. OpenRouter stays on `openrouter/free`.
The implementation never enables billing, but the operator must check actual
account/model free capacity. No new paid API key is required.

## Fair-use settings

Optional Supabase Edge Function secrets, positive integer values:

| Secret | Default |
| --- | ---: |
| CHAT_USER_PER_MINUTE | 6 |
| CHAT_USER_PER_DAY | 60 |
| CHAT_GLOBAL_PER_MINUTE | 20 |
| CHAT_GLOBAL_PER_DAY | 300 |

These are app limits, not claims about the provider's allowance. Set them to fit
the quota remaining after your other apps. New chat tasks have bounded provider
fallback time and output limits. A Gemini quota rejection does not rotate keys.
Existing legacy text tasks retain their behavior and are not covered by these
new chat-only quotas.

Per-visitor counters use a daily salted hash of a forwarded IP. Shared networks
may share an allowance. The global cap still applies if a header is spoofed.
Only bucket/count/expiry data is stored: no question text, birth details or raw IP.
SQL increments are atomic; an exceeded bucket rolls back all increments for the
request. Failed provider requests still count. Old counters are cleaned after
successful checks. Browser Stop cancels waiting; a provider may still complete
an already-started request and consume quota.

## What users receive

- Free General, Student and Astro chat without login or a payment gate.
- Telugu default; automatic input-language matching or selected answer language.
  An Other-language field supports languages outside the menu, subject to model quality.
- Subject/exam selection, Explain, Hints first, and one-question-at-a-time Practice.
- Optional birth details with an explicit time-unknown path; no claimed natal calculation.
- Chat, colorful notes and an answer-section mind map.
- Text export, PNG excerpt, browser Print / Save as PDF and share preview.
- Optional local history, clearable and disabled by default.

History is not encrypted or synced. It keeps up to ten conversations and the last
30 messages per conversation. Context sent to the provider is limited to the last
12 messages at 4,000 characters each; older context can be omitted. Current input
is limited to 6,000 characters. Replies come from configured external AI providers.
Birth form fields stay in memory and are sent with Astro requests; birth details
typed into a message follow the chat-history setting.

Mind map means a visual outline of up to 12 sections from the answer, not an
inferred knowledge graph. Notes are extracted, not regenerated with more AI calls.
PNG contains a labeled excerpt. Text/PDF include the full latest answer.
PDF uses the browser print dialog; Telugu rendering depends on available fonts.
Sharing never publishes a private transcript URL. LinkedIn shares the app link;
users can separately copy their selected answer text into a post.

No public community, website builder, OCR/photo solving, voice transcription,
live search, verified question bank, scored exam engine or calculated birth chart
is added in this focused release. Existing global ad scripts remain unchanged;
check third-party overlays before broadly promoting student pages.

## Short URL without a second application

The requested `one.racharlagot.in` uses a different root domain from your existing
`racharlagpt.in`. Confirm the spelling before changing DNS. The likely intended
address is `one.racharlagpt.in`.

For a short entry link, use a Cloudflare HTTPS redirect to the canonical app,
preserving path and query string (for example `/?page=astro`). Start with a
temporary redirect while checking, then make it permanent if desired.
Configure the matching proxied DNS record, certificate and Redirect Rule in your
own account. A CNAME alone is not an HTTP redirect and may fail if the host has
not accepted that extra hostname. No DNS change is included in this ZIP.

## Check and rollback

Run `node --test tests/free-chat.test.mjs` using Node 24+.
See FREE-CHAT-VERIFICATION.md for completed checks and remaining staging checks.

Rollback: restore the preceding frontend and ai-text versions, and use a fresh
service-worker cache name to refresh clients. The new private quota table may
remain unused. Do not drop any customer or purchase data.
