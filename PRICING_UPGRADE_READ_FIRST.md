# Pricing and Offers Upgrade

1. Run `PRICING_ADMIN_SETUP.sql` in your existing Supabase project's SQL Editor.
2. Deploy the **new** `pricing-control` Edge Function and redeploy the **modified** `create-payment` and `ad-market` Edge Functions. Configure `pricing-control` with JWT verification disabled, consistent with the existing token-protected admin functions; privileged writes are checked against `ADMIN_API_TOKEN` server-side. Ensure SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, ADMIN_API_TOKEN are configured. Never put the service role key in frontend files.
3. Deploy the updated `app.js` and `marketplace.js` with the rest of the site; refresh the browser (clear service worker cache if required).
4. Open Admin, enter your existing admin token, then use **Pricing & Offers**. The song default is now ₹10; ringtone generator remains ₹10; catalog ringtone and ad defaults retain existing prices until changed.
5. Set regular price and offer price (offer price must not exceed regular), tick **Offer active**, then Save. With offers disabled the regular price applies. All amounts are INR; Razorpay receives paise.
6. Test a new song order, generated ringtone, library ringtone, and each ad format/placement/duration in Razorpay test mode before using live payments. Previously created orders retain their original amount.

Notes: Changes are not live until both site and Edge Functions are deployed. Ad package pricing is grouped as Home vs Other pages, matching the existing pricing model. The admin login UI stores a token in session storage; the server verifies it for price updates. Public pricing is readable, but writes require the admin token. This upgrade does not alter your Razorpay dashboard product prices or existing orders.
