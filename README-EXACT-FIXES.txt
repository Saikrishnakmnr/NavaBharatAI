NavaBharat AI — TARGETED FIXES FROM UPLOADED ZIP

BASELINE:
NavaBharatAI-main from the uploaded ZIP only.

IMPORTANT:
This is NOT a full-project replacement.
Replace ONLY the files in this package. Keep every other file from the uploaded project unchanged.
Do NOT run new SQL.
Do NOT add new secrets.
Do NOT add ACESTEP_BASE_URL, ACESTEP_MODEL, or APIFRAME_BASE_URL.

FILES TO REPLACE:
1. app.js
2. supabase/functions/ai-text/index.ts
3. supabase/functions/live-rss/index.ts
4. supabase/functions/generate-media/index.ts
5. supabase/functions/admin-list/index.ts
6. supabase/functions/create-payment/index.ts

WHAT IS PRESERVED:
- ACE-Step provider and API key path
- Lyria 3.5 provider and Gemini API key path
- APIFrame provider and API key path
- existing music/ringtone generation flow
- Video Studio MP3 extraction
- Reel rendering
- Admin upload/manage/catalog features
- all other files and features from the uploaded ZIP

FIXES:
- AI/news/jobs calls no longer wait through long unauthenticated provider loops.
- Live RSS gets hard timeouts and Google RSS -> GDELT -> Gemini fallback.
- Lyria request uses the documented Lyria 3.5 interaction shape (no unsupported response_format field).
- ACE 502/503/504 gateway errors get one controlled retry; provider/model is not changed.
- Personalised Song price is ₹99, not ₹499.
- Razorpay description identifies it as “Personalised Song Gift ₹99”.
- Razorpay order notes include customer name, WhatsApp and message.
- Admin order list shows recent customer orders/details.
- Admin Studio polls orders every 30 seconds and can show a browser notification when a new order arrives while Admin Studio is open.

IMPORTANT EXTERNAL STATUS:
A Gemini 401 ACCESS_TOKEN_TYPE_UNSUPPORTED response is an authentication/key acceptance problem at Google's API layer, not a frontend model-name fix. The code keeps the Gemini model/provider architecture from the uploaded ZIP and uses x-goog-api-key. If Google rejects the configured key, the provider itself must accept that key before Gemini-dependent tools can work.

APIFrame HTTP 402 means the APIFrame account/provider is refusing the request for payment/credit/quota reasons.
ACE HTTP 504 is a provider gateway timeout; this patch retries it once but does not replace ACE.

The localhost:37857 / localhost:7071 resource errors were searched for in the uploaded ZIP and are NOT present in the project files, so they were intentionally not changed.
