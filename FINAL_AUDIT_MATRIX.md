# NavaBharat AI — Final Feature / Function / Dependency Audit

Release candidate: **13.0.0**  
Audit date: **2026-10-07**

## Audit scope

Compared the original working Streamlit application (`NavaBharatAI-updated(1).zip`, `app.py` ~3,650 lines) against the no-Streamlit HTML/CSS/JavaScript + Supabase migration.

The audit covered page-level features, important helper functions, provider calls, payment paths, storage paths, admin paths, mobile behavior, analytics/ads, and deployment artifacts.

### Result

- **Streamlit runtime:** removed from production package.
- **Frontend:** pure HTML/CSS/JavaScript; no React/npm build required.
- **Supabase Edge Functions:** 15 deployed-function directories, including the added live RSS function.
- **ACE-Step:** API key only from the customer/admin. Provider URL and model are internal defaults; no `ACESTEP_BASE_URL` or `ACESTEP_MODEL` secret is required.
- **APIFrame:** API key only. Provider URL is an internal default; no `APIFRAME_BASE_URL` secret is required.
- **Razorpay:** server-side Payment Links, verification, entitlement and signed download flow.
- **Known runtime limitation:** actual third-party provider/payment execution can only be finally verified after the user's real Supabase secrets are deployed. No secret was copied into this package.

## Feature matrix

| Area | Original behavior | Release 13 implementation | Status |
|---|---|---|---|
| Home | Main product dashboard | Responsive web dashboard | PASS |
| AI Solve | Gemini answer/solution | `ai-text` solve | PASS |
| Science | Specialized science help | `ai-text` science | PASS |
| Translator | Multi-language translation | `ai-text` translator | PASS |
| Music Generator | Lyrics/idea, style, duration, vocals | ACE-Step → Gemini Lyria → APIFrame fallback | PASS |
| Music lyrics AI | Generate original lyrics | `ai-text` lyrics | PASS |
| Music preview | Free preview | Signed generated-audio preview | PASS |
| Song download payment | ₹19 Razorpay | Server Payment Link + verification + entitlement | PASS |
| Generated ringtone | Idea/lyrics → preview | Same music provider chain, ringtone kind | PASS |
| Ringtone improvement | AI improve idea | `ai-text` ringtone_idea | PASS |
| Ringtone payment | ₹10 minimum/offer | ₹10 generated ringtone download | PASS |
| Ringtone library | Search/listen/download | Supabase catalog + preview + Razorpay | PASS |
| Ringtone regular/offer price | Regular ₹20 / offer ₹10 | DB-controlled prices, min ₹10 | PASS |
| Ringtone rights | Admin source/license | Rights checkbox + license reference | PASS |
| Movie ringtone legality | Old app had local files | Migration does not scrape/rehost unlicensed recordings | INTENTIONAL SAFETY/LEGAL BOUNDARY |
| Authorized catalog refresh | RSS/feed/local sources | `refresh-catalog` | PASS |
| RacharlaGPT Music Library | Local audio library | Supabase published library | PASS |
| Admin music upload | Upload/delete tracks | Protected upload/unpublish | PASS |
| Admin ringtone upload | Upload/delete ringtones | Protected upload/deactivate | PASS |
| Admin provider tests | ACE/Gemini/APIFrame test buttons | Protected `admin_test` generation | PASS |
| Search | Google search | Google result opening | PASS |
| Search AI summary | Gemini grounded/fallback answer | Gemini `search` + live RSS | PASS |
| Search live results | Google News RSS cards | `live-rss` | PASS |
| Search mind map | Visual image | Browser-generated visual | PASS |
| Search infographic | Visual image | Browser-generated visual | PASS |
| Search notes | Downloadable image | Browser-generated PNG | PASS |
| Search share | WhatsApp/social share | Share links + visual share | PASS |
| Live Information | Weather/time + RSS | Weather/time + live RSS | PASS |
| Current Affairs | RSS by language/category/count | Live RSS + category filtering | PASS |
| Current Affairs quiz | Gemini quiz | `makeCurrentQuiz` | PASS |
| Jobs & Exams | Grounded Gemini + RSS fallback | AI + RSS fallback | PASS |
| Creator Studio | Platform content generation | `ai-text` creator | PASS |
| Design poster | Multiple social formats/themes/photo | Browser canvas | PASS |
| Design 3D text | 3D poster | Browser 3D-style renderer | PASS |
| Design free preview | Watermarked | Watermarked preview | PASS |
| Design HD | ₹9 no-watermark | Razorpay ₹9 + post-payment render | PASS |
| Video MP3 extraction | FFmpeg MP3 | FFmpeg WebAssembly in browser | PASS |
| Reel Builder | Images + optional audio → 1080×1920 MP4 | FFmpeg WebAssembly | PASS |
| Premium/support tips | Razorpay tips | Payment Links | PASS |
| Personalised song request | Name/WhatsApp/message + payment | Razorpay order with customer data | PASS |
| Order recovery | Order ID | `order-status` + Razorpay check | PASS |
| Purchased file retention | Source files not deleted after 30 days | Cleanup deletes expired entitlements/unpaid orders only | PASS |
| Signed downloads | Paid-only | Server entitlement + signed URL | PASS |
| Customer login | Not required | Not required | PASS |
| Mobile sidebar | Auto-close after selection | `go()` closes sidebar | PASS |
| PWA | Service worker/update | Manifest + SW + version check | PASS |
| SEO | Metadata/canonical | Root index metadata | PASS |
| GA4 | `G-39MNX1V7XK` | Root index GA4 | PASS |
| Monetag | Zone `11941649` | Original Monetag zone script retained | PASS |
| AdSense | Ready/optional | Placeholder/config ready | PASS |
| About | Brand/developer | About page | PASS |
| Privacy | Privacy info | Privacy page | PASS |
| Contact | Contact info | Contact page | PASS |

## Provider matrix

| Provider | Required customer secret | Additional ACE/APIFrame secret required? | Internal default |
|---|---|---|---|
| Gemini text | `GEMINI_API_KEY` and optional `GEMINI_API_KEY_2/3` | No | Gemini model fallback chain in `_shared.ts` |
| Gemini Lyria | Same Gemini key pool | No | `lyria-3.5` |
| ACE-Step | `ACESTEP_API_KEY` (also accepts legacy `ACE_API_KEY` / `ACE_APP_KEY`) | **No** | `https://api.acemusic.ai`, `acemusic/acestep-v1.5-turbo` |
| APIFrame | `APIFRAME_API_KEY` | **No** | `https://api.apiframe.ai/v2`, Suno provider |
| Razorpay | `RAZORPAY_KEY_ID` + `RAZORPAY_KEY_SECRET` | No | Razorpay Payment Links API |

The ACE-Step/APIFrame URL/model defaults are implementation details. **Do not create secrets for them.**

## Supabase function matrix

| Function | Purpose | Public/admin |
|---|---|---|
| `ai-text` | Text AI tools | Public |
| `generate-media` | Songs/ringtones + provider fallback | Public; `admin_test` requires admin token |
| `create-payment` | Razorpay order/payment link | Public |
| `verify-payment` | Verify Razorpay payment + entitlement | Public |
| `order-status` | Recovery/status | Public |
| `create-download` | Paid signed download | Public endpoint, server-side payment/entitlement checks |
| `preview-ringtone` | Free ringtone preview | Public |
| `live-rss` | Google News RSS proxy | Public |
| `admin-list` | Admin library listing | Admin token |
| `admin-upload` | Admin music/ringtone upload | Admin token |
| `admin-delete-music` | Unpublish music | Admin token |
| `admin-delete-ringtone` | Deactivate ringtone | Admin token |
| `refresh-catalog` | Authorized catalog import | Admin token |
| `cleanup` | Expired entitlement/unpaid-order cleanup | Admin token |

## Storage matrix

| Bucket | Public? | Use |
|---|---:|---|
| `music-library` | Yes | Published RacharlaGPT music playback |
| `ringtone-full` | No | Paid ringtone files |
| `ringtone-preview` | No | Signed free previews |
| `generated-audio` | No | Generated song/ringtone files |

## Payment matrix

| Product | Amount | Download entitlement |
|---|---:|---|
| Generated song | ₹19 | 30 days from payment; source file remains stored |
| Generated ringtone | ₹10 | 30 days from payment; source file remains stored |
| Library ringtone | DB price, minimum ₹10 | 30 days from payment; source file remains stored |
| Design HD | ₹9 | Payment unlocks local no-watermark rendering |
| Support | ₹19/₹49/₹99/₹199 | No file entitlement |
| Personalised song | ₹499 in current web flow | No automatic generated-file download; order/customer details retained |

## Deployment verification required after secrets are installed

These cannot be truthfully marked as live-tested inside this audit because they require the user's private provider/payment credentials:

1. ACE-Step real generation with the user's key.
2. Gemini/Lyria real generation with the user's key.
3. APIFrame real generation with the user's key/credits.
4. Razorpay test/live Payment Link completion and return callback.
5. Supabase storage signed URLs in the user's project.
6. Google News RSS availability from the deployed Edge Function.
7. FFmpeg WebAssembly download/load in the user's GitHub Pages + Cloudflare environment.
8. GA4/Monetag reporting in their live domain.

The code paths and contracts for these are included and statically checked; the final live check is intentionally a deployment verification, not a hidden claim that private services were tested without credentials.
