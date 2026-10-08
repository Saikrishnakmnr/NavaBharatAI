# NavaBharat AI — fixes from the supplied working ZIP

This build is based only on the supplied `NavaBharatAI-main (2).zip`.

## Fixed
1. Generated song/ringtone asset persistence: repaired database grants/RLS and server-side asset flow.
2. Razorpay orders: transactional tables remain private; Edge Functions use the server role. Design orders now carry the generated asset.
3. Home/sidebar Music Generator route: explicit route mapping and mobile navigation close behavior retained.
4. Admin/catalog: authorized catalog fetch uses an identifying User-Agent and better server fallback behavior.
5. Live News / Current Affairs / Jobs: Google News RSS is primary; GDELT Article List is automatic fallback instead of exposing a Google 503.
6. RacharlaGPT Music Library: public published-library read permission is explicitly repaired.
7. MP3 extraction / Reel Builder: FFmpeg worker loading is rewritten to avoid the cross-origin worker-chunk failure; the core remains WebAssembly in the browser.
8. Design Studio: poster and 3D previews are now AI-generated through Gemini image generation on the server, not local canvas-only mockups.
9. Design purchase: generated design assets are stored privately; Razorpay order, payment verification, entitlement and signed download now use the same asset.
10. Customer-facing AI pages no longer advertise internal Supabase implementation details.
11. Frontend contains no service-role/provider secret. ACE-Step/APIFrame base URLs/models are not customer configuration variables.
12. Production URL corrected everywhere to `https://navabharatai.racharlgpt.in`.

## Required one-time database action

Run `PERMISSION_REPAIR.sql` in Supabase SQL Editor.

The SQL deliberately does **not** grant customers write access to `orders`, `download_entitlements`, or `generated_assets`. Payment/order/asset writes stay server-side.

## Edge Functions changed

- `generate-media`
- `create-payment`
- `verify-payment`
- `order-status`
- `create-download`
- `live-rss`
- `refresh-catalog`

All remain single-file Via Editor functions.

## Important

Keep the existing server secrets. Only these provider credentials are required for the migrated music flow:

- `ACESTEP_API_KEY`
- `APIFRAME_API_KEY`

Plus the existing Gemini, Razorpay, admin token, and Supabase server configuration already used by the application. Do not add ACE-Step/APIFrame base URL or model secrets.
