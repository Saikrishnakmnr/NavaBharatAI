# NavaBharatAI eBook module — ONLY new files + index.html replacement

Based on **NavaBharatAI-main (14).zip**. Existing `app.js`, `marketplace.js`, music, payment, recovery and advertisement Edge Functions remain untouched.

## Exact order

1. Back up GitHub repository and Supabase database. Use a staging/test project and Razorpay **test** credentials for end-to-end tests. Do not test refunds with live customer money.
2. In existing Supabase SQL Editor, run **EBOOK_STORE_SETUP.sql once**. This creates only `nava_ebook*` tables and two storage buckets. It does not alter existing orders or pricing tables. Confirm success.
3. Check Storage: `nava-ebook-pdfs` **PRIVATE**, `nava-ebook-covers` **PUBLIC**. Do not create public PDF read policies. The service-role Edge Functions manage files. Bucket file limits: PDFs 50 MB, covers 5 MB.
4. Existing Supabase secrets should already include `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `ADMIN_API_TOKEN`. **Reuse** them. Never expose service-role or Razorpay secret in frontend. `config.js` has only public key ID and publishable Supabase key.
5. Deploy **new** Edge Functions `ebook-store` and `ebook-admin` from the respective `index.ts` files. For these two endpoints, configure JWT verification OFF if using Supabase publishable `sb_publishable_` keys (legacy JWT verification does not accept publishable keys). The functions implement their own action authorization; admin actions require `x-admin-token` checked against `ADMIN_API_TOKEN`. Keep existing functions/settings unchanged.
6. Upload new GitHub root files `ebooks.html`, `ebooks.css`, `ebooks.js`, `ebook-admin.html`, `ebook-admin.js`. Replace **only** root `index.html` to add an eBook Store link to the existing sidebar; the remainder of that file is preserved byte-for-byte except the small injected script.
7. Visit `/ebook-admin.html`, enter existing admin token, create book with PDF + cover, publish it. Then visit `/ebooks.html`. The new page uses the same domain and assets.
8. **Test in Razorpay test mode:** catalog, price changes, offer, order creation, receipt saving BEFORE payment, successful payment, failed/closed checkout, re-download on same and another browser with private code, wrong-code rejection, unpublished-book recovery, PDF privacy, refund and refund reconciliation. Only then use production credentials.

## Important boundaries and caveats

- eBook orders are separate (`nava_ebook_orders`), not mixed with song purchases. Recovery and receipts are separate.
- No public refund button. Admin refund attempts are one-per-order and become `refund_pending`; pending/refunded orders cannot download. **If a refund is pending, verify status in Razorpay dashboard.** If Razorpay API returned an uncertain error, do not retry automatically.
- `ebook-admin` accepts a shared admin token. This is the same existing token, not a new login. The browser keeps it only in page memory (not localStorage).
- PDFs are private; each successful recovery generates a 120-second signed URL. Anyone with that URL can access it until expiry. A downloaded PDF cannot be revoked after the fact.
- Recovery code is the purchase credential. A lost code cannot be recovered from the public UI. Save the receipt before paying.
- If your website has aggressive caching, hard-refresh after deploying; new pages are not listed in the existing service worker cache.
- **No SQL for old `nava_prices` or old `orders` tables is needed.**
- The new module is code-reviewed and browser JavaScript syntax checked, but **not live-deployed or end-to-end tested**. Use staging before production.
- If signed PDF upload fails, check Supabase Storage CORS and the signed upload URL in the browser network panel. Do not make the PDF bucket public as a workaround.
