# NavaBharat AI V16 — replacement deployment

Source: the user's latest `NavaBharatAI-main (3).zip`. No older project is merged.

## 1. Supabase SQL — do this first
Run `V16_REPAIR.sql` once in Supabase SQL Editor.

Do not delete existing tables, functions, orders, or storage files.

## 2. GitHub frontend replacement
Replace these files in the existing repository:
- `app.js`
- `index.html`
- `styles.css`
- `config.js`
- `sw.js`
- `version.json`

## 3. Via Editor — replace the listed single-file functions
Each folder contains one `index.ts` and can be pasted directly into the matching Supabase Edge Function.

Replace:
- `create-payment`
- `verify-payment`
- `order-status`
- `create-download`
- `generate-media`
- `ai-text`
- `live-rss`
- `preview-ringtone`
- `admin-list`
- `admin-upload`
- `admin-delete-ringtone`
- `admin-delete-music`
- `refresh-catalog`

The admin CORS fix is included in the admin functions.

## 4. Secrets
Keep the existing server-side secrets. V16 does not add ACE-Step/APIFrame base-URL secrets.

Required:
- `SUPABASE_SERVICE_ROLE_KEY`
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`
- `GEMINI_API_KEY`
- `GEMINI_API_KEY_2`
- `ACESTEP_API_KEY`
- `APIFRAME_API_KEY`
- `ADMIN_API_TOKEN`
- `SITE_URL=https://navabharatai.racharlgpt.in`

## 5. Razorpay change
V16 no longer creates Razorpay Payment Links and no longer sends `callback_url`.
It creates a Razorpay Order and opens Razorpay Checkout in the browser.
Payment success is verified server-side using the Razorpay signature and order status.

## 6. Customer audio protection
Generated song/ringtone previews remain playable for free, but:
- native download controls are hidden
- preview sharing is removed
- paid download is returned only after verified payment
- paid download URLs are short-lived signed URLs

This cannot make an audio stream mathematically impossible to copy, but it removes the normal browser download path and keeps the source file private.

## 7. Poster / 3D
Poster and 3D previews are generated server-side with Gemini image generation.
The API key never goes to the browser.
The preview is generated at 2K and the paid download unlocks the private asset.

## 8. News
Live RSS tries Google News, then GDELT, then Gemini web-grounded search.
Current Affairs and Jobs also have AI web-search fallbacks.

## 9. Browser video tools
FFmpeg's 814 worker is converted to a same-origin Blob Worker to avoid the cross-origin Worker error.
The service worker also returns a real offline Response instead of an undefined value.

## 10. After deployment
Hard-refresh once (Ctrl+Shift+R) or open the app in an incognito window. V16 changes the service-worker cache name.
