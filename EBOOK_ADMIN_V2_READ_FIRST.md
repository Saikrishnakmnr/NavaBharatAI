# eBook Admin V2 — incremental upgrade

Replace ONLY: ebook-admin.html, ebook-admin.js, ebooks.css, supabase/functions/ebook-admin/index.ts. Keep all other files untouched.

Deploy updated ebook-admin Edge Function after GitHub files or before; no new SQL is required if EBOOK_STORE_SETUP.sql was already run. If not, run the original EBOOK_STORE_SETUP.sql first.

Admin delete: allowed only when no order records exist; removes catalog row and its current PDF/cover objects. Previously replaced orphan files may require manual Storage cleanup. Books with ANY orders must be unpublished instead, preserving download/recovery and audit history.

Dashboard: counts books and orders, gross, processed refunds, pending refunds, estimated net before fees. Enter costs to calculate estimated profit/loss. No physical inventory for digital PDFs. Queries currently cap at 10,000 orders; implement paginated server-side aggregation before scaling.

Mobile: two-column cards on phones, one column on very narrow phones, responsive dashboard.

Test on staging with Razorpay test mode. Existing song, ringtone, advertisement, recovery and Razorpay functions are not modified.
