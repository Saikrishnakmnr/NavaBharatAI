import io
import os
import re
import time
import html
import hmac
import math
import wave
import struct
import tempfile
import subprocess
import shutil
import uuid
import urllib.parse
import json
import base64
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# AUTOMATIC HTML HEAD INJECTION (GA4 & MONETAG FROM SECRETS)
# ============================================================

def inject_tracking_scripts():
    """
    Best-effort server-side patch for environments where Streamlit's packaged
    index.html is writable. Also injects verification meta tags when supplied.
    For hosted Streamlit deployments, the deployer's real root HTML/domain may
    still be required by third-party verification crawlers.
    """
    try:
        def _early_secret(name, default=""):
            try:
                value = st.secrets.get(name)
                if value:
                    return str(value).strip()
            except Exception:
                pass
            return os.getenv(name, default).strip()
        ga_id = _early_secret("GA_MEASUREMENT_ID", "G-39MNX1V7XK")
        monetag_id = _early_secret("MONETAG_ZONE_ID", "11941649")
        google_verification = _early_secret("GOOGLE_SITE_VERIFICATION", "google3e42fef32ee1bbbd.html")
        monetag_verification_tag = _early_secret("MONETAG_VERIFICATION_TAG")
        monetag_verification_legacy = _early_secret("MONETAG_VERIFICATION_META")

        streamlit_path = Path(st.__path__[0])
        index_path = streamlit_path / "static" / "index.html"
        if not index_path.exists():
            return

        html_text = index_path.read_text(encoding="utf-8")

        head_parts = []
        if ga_id and ga_id not in html_text:
            head_parts.append(f"""
<!-- NavaBharat AI: GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={html.escape(ga_id)}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', '{html.escape(ga_id)}', {{
  send_page_view: true,
  transport_type: 'beacon'
}});
</script>
""")

        if monetag_id and monetag_id not in html_text:
            head_parts.append(f"""
<!-- NavaBharat AI: Monetag zone -->
<script src="https://3nbf4.com/act/files/tag.min.js?z={html.escape(monetag_id)}" data-cfasync="false" async></script>
""")

        if google_verification and "google-site-verification" not in html_text:
            head_parts.append(
                f'<meta name="google-site-verification" content="{html.escape(google_verification, quote=True)}">'
            )

        if monetag_verification_tag and "monetag" not in html_text.lower():
            # IMPORTANT: Monetag requires the exact verification tag generated
            # in its dashboard. Do not invent/modify the meta name or content.
            head_parts.append(monetag_verification_tag)
        elif monetag_verification_legacy and "monetag-verification" not in html_text:
            # Backward-compatible option if the user supplied only a token.
            head_parts.append(
                f'<meta name="monetag-verification" content="{html.escape(monetag_verification_legacy, quote=True)}">'
            )

        if head_parts and "<head>" in html_text:
            updated_html = html_text.replace("<head>", "<head>\n" + "\n".join(head_parts), 1)
            index_path.write_text(updated_html, encoding="utf-8")
    except Exception:
        # Read-only/hosted Streamlit packages should not break the app.
        pass


inject_tracking_scripts()


# ============================================================
# NAVABHARAT AI
# POWERED BY RACHARLAGPT
# Created & Developed by Racharla Saikrishna
# ============================================================

APP_NAME = "NavaBharat AI"
APP_VERSION = "8.0.0"
CREATOR = "Racharla Saikrishna"
BRAND = "RacharlaGPT"
TAGLINE = "POWERED BY RACHARLAGPT"
CHANNEL_URL = "https://www.youtube.com/@racharlagpt"

MAX_UPLOAD_MB = 250
MUSIC_DIR = Path("music_library")
MUSIC_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="NavaBharat AI — RacharlaGPT",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PREMIUM UI STYLES
# ============================================================

st.markdown(
    """
<style>

html, body, [class*="css"] {
    font-family:
        Inter,
        system-ui,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 10% 10%, rgba(99,102,241,.10), transparent 28%),
        radial-gradient(circle at 90% 10%, rgba(236,72,153,.10), transparent 28%),
        radial-gradient(circle at 50% 90%, rgba(14,165,233,.08), transparent 32%),
        linear-gradient(135deg,#f8fbff 0%,#f7f3ff 48%,#fff7fb 100%);
}

[data-testid="stHeader"] {
    background: rgba(255,255,255,.84);
}

[data-testid="stSidebar"] {
    min-width: 310px;
    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #1e1b4b 42%,
            #312e81 72%,
            #4c1d95 100%
        );
}

[data-testid="stSidebarContent"] {
    padding: 16px 13px 24px 13px;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}


/* BRAND */

.sidebar-brand {
    padding: 18px 15px;
    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.20),
            rgba(255,255,255,.06)
        );

    border:
        1px solid rgba(255,255,255,.20);

    box-shadow:
        0 16px 45px rgba(0,0,0,.28);

    margin-bottom: 15px;
}

.sidebar-brand .mark {
    font-size: 42px;
    line-height: 1;
    margin-bottom: 8px;
}

.sidebar-brand .name {
    font-size: 25px;
    font-weight: 950;
    letter-spacing: -1px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #ffd6e7,
            #c4b5fd,
            #a7f3d0
        );

    -webkit-background-clip: text;
    background-clip: text;

    color: transparent !important;
}

.sidebar-brand .tag {
    font-size: 10px;
    opacity: .76;
    letter-spacing: 1.5px;
    margin-top: 4px;
}


/* SIDEBAR RADIO NAVIGATION */

.nav-caption {
    margin:
        16px 8px 8px;

    font-size: 10px;
    font-weight: 900;
    letter-spacing: 1.8px;
    text-transform: uppercase;

    opacity: .60;
}

[data-testid="stSidebar"] [role="radiogroup"] {
    gap: 7px;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    min-height: 48px;

    padding:
        8px 10px;

    border-radius: 15px;

    border:
        1px solid rgba(255,255,255,.08);

    background:
        linear-gradient(
            100deg,
            rgba(255,255,255,.055),
            rgba(255,255,255,.025)
        );

    transition:
        transform .16s ease,
        background .16s ease,
        box-shadow .16s ease;
}

[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    transform: translateX(3px);

    background:
        linear-gradient(
            100deg,
            rgba(124,58,237,.52),
            rgba(37,99,235,.34),
            rgba(236,72,153,.28)
        );

    box-shadow:
        0 8px 24px rgba(0,0,0,.18);
}

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background:
        linear-gradient(
            100deg,
            #7c3aed,
            #2563eb,
            #db2777
        );

    border-color:
        rgba(255,255,255,.30);

    box-shadow:
        0 10px 28px rgba(124,58,237,.38);
}


/* MAIN HERO */

.hero {
    padding: 34px;

    border-radius: 30px;

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.96),
            rgba(255,255,255,.70)
        );

    border:
        1px solid rgba(255,255,255,.90);

    box-shadow:
        0 20px 65px rgba(54,47,100,.12);

    margin-bottom: 22px;

    overflow: visible;
}

.hero h1 {
    margin: 0;

    font-size:
        clamp(32px, 5vw, 58px);

    line-height: 1.05;

    letter-spacing: -2px;

    word-break: normal;
    overflow-wrap: anywhere;

    background:
        linear-gradient(
            90deg,
            #111827,
            #6d28d9,
            #db2777,
            #0891b2
        );

    -webkit-background-clip: text;
    background-clip: text;

    color: transparent;
}

.hero p {
    color: #475569;

    font-size: 16px;

    line-height: 1.65;

    margin:
        12px 0 0;
}


/* CARDS */

.card {
    padding: 22px;

    min-height: 150px;

    border-radius: 25px;

    background:
        rgba(255,255,255,.86);

    border:
        1px solid rgba(148,163,184,.20);

    box-shadow:
        0 15px 42px rgba(30,41,59,.08);

    margin-bottom: 16px;
}

.card h3 {
    margin: 0 0 8px;

    color: #111827;
}

.card p {
    color: #475569;

    line-height: 1.55;
}


/* BUTTONS */

.stButton > button,
.stDownloadButton > button,
.stLinkButton > a,
.stFormSubmitButton > button {
    border: 0 !important;
    border-radius: 16px !important;
    min-height: 46px !important;
    padding: 9px 16px !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    text-shadow: 0 1px 2px rgba(0,0,0,.25) !important;
    background: linear-gradient(120deg,#7c3aed,#2563eb,#0891b2,#db2777) !important;
    background-size: 260% 260% !important;
    box-shadow: 0 9px 27px rgba(37,99,235,.22) !important;
    transition: transform .18s ease, box-shadow .18s ease, filter .18s ease !important;
}

.stButton:nth-of-type(6n+1) > button,
.stFormSubmitButton:nth-of-type(6n+1) > button {
    background: linear-gradient(120deg,#7c3aed,#db2777,#f43f5e) !important;
}
.stButton:nth-of-type(6n+2) > button,
.stFormSubmitButton:nth-of-type(6n+2) > button {
    background: linear-gradient(120deg,#2563eb,#0891b2,#06b6d4) !important;
}
.stButton:nth-of-type(6n+3) > button,
.stFormSubmitButton:nth-of-type(6n+3) > button {
    background: linear-gradient(120deg,#059669,#10b981,#84cc16) !important;
}
.stButton:nth-of-type(6n+4) > button,
.stFormSubmitButton:nth-of-type(6n+4) > button {
    background: linear-gradient(120deg,#ea580c,#f59e0b,#f97316) !important;
}
.stButton:nth-of-type(6n+5) > button,
.stFormSubmitButton:nth-of-type(6n+5) > button {
    background: linear-gradient(120deg,#be123c,#e11d48,#9333ea) !important;
}
.stButton:nth-of-type(6n) > button,
.stFormSubmitButton:nth-of-type(6n) > button {
    background: linear-gradient(120deg,#0f766e,#14b8a6,#2563eb) !important;
}

.stDownloadButton > button {
    background: linear-gradient(120deg,#334155,#475569,#0f172a) !important;
}
.stLinkButton > a {
    background: linear-gradient(120deg,#4f46e5,#7c3aed,#ec4899) !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover,
.stLinkButton > a:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-3px) scale(1.01);
    filter: brightness(1.08) saturate(1.15);
    box-shadow: 0 16px 34px rgba(37,99,235,.34) !important;
}

.stButton > button p,
.stDownloadButton > button p,
.stLinkButton > a p,
.stFormSubmitButton > button p,
.stLinkButton > a div {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 900 !important;
}

.home-card-1 { background: linear-gradient(135deg,rgba(239,246,255,.98),rgba(219,234,254,.94),rgba(224,231,255,.92)) !important; }
.home-card-2 { background: linear-gradient(135deg,rgba(250,245,255,.98),rgba(243,232,255,.94),rgba(252,231,243,.92)) !important; }
.home-card-3 { background: linear-gradient(135deg,rgba(236,253,245,.98),rgba(209,250,229,.94),rgba(207,250,254,.92)) !important; }
.home-card-4 { background: linear-gradient(135deg,rgba(255,247,237,.98),rgba(254,215,170,.90),rgba(254,240,138,.84)) !important; }
.home-card-5 { background: linear-gradient(135deg,rgba(239,246,255,.98),rgba(224,242,254,.94),rgba(233,213,255,.92)) !important; }
.home-card-6 { background: linear-gradient(135deg,rgba(253,242,248,.98),rgba(252,231,243,.94),rgba(244,114,182,.12)) !important; }
.home-card-7 { background: linear-gradient(135deg,rgba(15,23,42,.98),rgba(88,28,135,.94),rgba(15,23,42,.92)) !important; }

.home-card-1, .home-card-2, .home-card-3, .home-card-4, .home-card-5, .home-card-6, .home-card-7 {
    transition: transform .20s ease, box-shadow .20s ease, border-color .20s ease;
}
.home-card-1:hover, .home-card-2:hover, .home-card-3:hover,
.home-card-4:hover, .home-card-5:hover, .home-card-6:hover, .home-card-7:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(30,41,59,.16);
    border-color: rgba(99,102,241,.35);
}


/* NEON MUSIC UI STYLES */

.neon-hero {
    padding: 30px;
    border-radius: 26px;
    background: linear-gradient(135deg, #090d16 0%, #1e1b4b 50%, #31104b 100%);
    border: 1px solid rgba(192, 132, 252, 0.4);
    box-shadow: 0 0 35px rgba(168, 85, 247, 0.25);
    margin-bottom: 22px;
}

.neon-hero h1 {
    margin: 0;
    font-size: clamp(30px, 4.5vw, 54px);
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #c084fc, #f472b6, #34d399);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
}

.neon-hero p {
    color: #cbd5e1 !important;
    font-size: 15px;
    margin-top: 10px;
}

.neon-panel {
    background: rgba(15, 23, 42, 0.90);
    border: 1px solid rgba(168, 85, 247, 0.35);
    border-radius: 20px;
    padding: 22px;
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
    color: #f8fafc;
    margin-bottom: 20px;
}


/* SOCIAL SHARE BUTTON COLORS */
.share-whatsapp a { background: linear-gradient(120deg,#16a34a,#22c55e,#84cc16) !important; }
.share-facebook a { background: linear-gradient(120deg,#1877f2,#2563eb,#60a5fa) !important; }
.share-x a { background: linear-gradient(120deg,#111827,#334155,#000000) !important; }
.share-linkedin a { background: linear-gradient(120deg,#0a66c2,#0284c7,#06b6d4) !important; }
.share-instagram a { background: linear-gradient(120deg,#7c3aed,#db2777,#f97316) !important; }

/* INPUTS */

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select {
    background: #ffffff !important;
    color: #111827 !important;
    caret-color: #111827 !important;
    border: 2px solid #cbd5e1 !important;
    border-radius: 15px !important;
    font-size: 16px !important;
}

[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}


/* FILE UPLOADER */

[data-testid="stFileUploader"] section {
    background: #ffffff !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 17px !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #1f2937;
}

@media (max-width: 800px) {
    [data-testid="stSidebar"] {
        min-width: 280px;
    }
    .hero {
        padding: 21px;
        border-radius: 23px;
    }
    .hero h1 {
        font-size: 35px;
        letter-spacing: -1px;
    }
    .card {
        padding: 18px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SECRETS & CONFIG
# ============================================================

def safe_secret(name: str, default: str = "") -> str:
    candidates = [name, name.lower(), name.upper()]
    for key in candidates:
        try:
            value = st.secrets.get(key)
            if value:
                return str(value).strip()
        except Exception:
            pass
        value = os.getenv(key)
        if value:
            return value.strip()
    return default


def gemini_keys():
    """Return all configured Gemini keys in deterministic failover order."""
    values = []
    # Support both individually named keys and a comma/newline-separated pool.
    for name in (
        "GEMINI_API_KEY",
        "GEMINI_API_KEY_2",
        "GEMINI_API_KEY_3",
        "GEMINI_AI_KEY_1",
        "GEMINI_AI_KEY_2",
        "GEMINI_AI_KEY_3",
    ):
        value = safe_secret(name)
        if value and value not in values:
            values.append(value)
    pool = safe_secret("GEMINI_API_KEYS")
    if pool:
        for value in re.split(r"[\s,;]+", pool):
            value = value.strip()
            if value and value not in values:
                values.append(value)
    return values


def gemini_key():
    keys = gemini_keys()
    return keys[0] if keys else ""


def configured_models():
    primary = safe_secret("GEMINI_MODEL", "gemini-3.8-flash")
    # Only use currently documented stable Gemini API model IDs.
    # Keep the fallback set on current 3.x models. Do not silently fall back to older
    # model IDs when the user's credential is rejected; that obscures the real problem.
    models = [primary, "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash", "gemini-3.5-flash"]
    return list(dict.fromkeys(x.strip() for x in models if x.strip()))


# ============================================================
# GEMINI CLIENTS
# ============================================================

@st.cache_resource(show_spinner=False)
def get_gemini_client(api_key: str = ""):
    key = api_key or gemini_key()
    if not key:
        return None
    try:
        from google import genai
        return genai.Client(api_key=key)
    except Exception:
        return None


def clean_error(exc):
    text = str(exc)
    text = re.sub(r"[A-Za-z0-9_-]{30,}", "[redacted]", text)
    return text[:1600]


def _gemini_auth_headers(api_key: str, bearer: bool = False):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if bearer:
        headers["Authorization"] = f"Bearer {api_key}"
    else:
        headers["x-goog-api-key"] = api_key
    return headers


def _gemini_extract_interaction_text(body: dict) -> str:
    if not isinstance(body, dict):
        return ""
    if body.get("output_text"):
        return str(body["output_text"])
    output = body.get("output")
    if isinstance(output, list):
        parts = []
        for item in output:
            if isinstance(item, dict):
                if item.get("text"):
                    parts.append(str(item["text"]))
                for content in item.get("content", []) or []:
                    if isinstance(content, dict) and content.get("text"):
                        parts.append(str(content["text"]))
        if parts:
            return "".join(parts)
    for step in body.get("steps", []) or []:
        if isinstance(step, dict):
            for content in step.get("content", []) or []:
                if isinstance(content, dict) and content.get("text"):
                    return str(content["text"])
    return ""


def _gemini_is_auth_error(status: int, raw: str) -> bool:
    text = raw.upper()
    return status in (401, 403) or any(x in text for x in (
        "UNAUTHENTICATED", "ACCESS_TOKEN_TYPE_UNSUPPORTED", "INVALID AUTHENTICATION",
        "INVALID_API_KEY", "API KEY NOT VALID", "CREDENTIAL",
    ))


def gemini_generate(prompt: str, grounded: bool = False, retries: int = 1):
    """Generate Gemini text, supporting both current API-key header styles.

    Current Google documentation supports x-goog-api-key for Gemini API requests;
    auth keys are also usable with Authorization: Bearer. Trying the second header
    on an authentication rejection makes the app resilient to the newer auth-key
    transition without changing the user's prompt or silently using an unrelated model.
    """
    keys = gemini_keys()
    if not keys:
        return False, "Gemini is not connected. Add GEMINI_API_KEY and optionally GEMINI_API_KEY_2 to Streamlit Secrets."

    last_error = ""
    models = configured_models()
    for key_index, api_key in enumerate(keys, start=1):
        for model in models:
            auth_modes = [False, True]
            for bearer in auth_modes:
                for attempt in range(retries + 1):
                    try:
                        if grounded:
                            url = "https://generativelanguage.googleapis.com/v1beta/interactions"
                            payload = {
                                "model": model,
                                "input": prompt,
                                "tools": [{"type": "google_search"}],
                            }
                        else:
                            url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model, safe='')}:generateContent"
                            payload = {
                                "contents": [{"parts": [{"text": prompt}]}],
                                "generationConfig": {"temperature": 0.4},
                            }

                        response = requests.post(
                            url,
                            headers=_gemini_auth_headers(api_key, bearer=bearer),
                            json=payload,
                            timeout=90,
                        )
                        raw = response.text[:1800]
                        if not response.ok:
                            if _gemini_is_auth_error(response.status_code, raw):
                                last_error = f"Gemini key {key_index} / {model}: HTTP {response.status_code} ({'Bearer' if bearer else 'x-goog-api-key'}): {raw}"
                                # Try the other current authentication header before moving
                                # to the second configured key.
                                break
                            raise RuntimeError(f"HTTP {response.status_code}: {raw}")

                        data = response.json()
                        if grounded:
                            answer = _gemini_extract_interaction_text(data)
                        else:
                            parts = (((data.get("candidates") or [{}])[0]).get("content") or {}).get("parts") or []
                            answer = "".join(str(part.get("text", "")) for part in parts if isinstance(part, dict) and part.get("text"))

                        if answer and str(answer).strip():
                            return True, str(answer).strip()
                        last_error = f"Gemini key {key_index} / {model}: empty response"
                        break
                    except Exception as exc:
                        raw_exc = str(exc)
                        last_error = f"Gemini key {key_index} / {model}: {clean_error(exc)}"
                        if _gemini_is_auth_error(401, raw_exc):
                            break
                        transient = any(k in raw_exc.upper() for k in ["429", "500", "502", "503", "504", "TIMEOUT", "DEADLINE", "UNAVAILABLE", "RESOURCE_EXHAUSTED"])
                        if transient and attempt < retries:
                            time.sleep(1.5 * (2 ** attempt))
                            continue
                        break
                # On auth failure, try the other header for this same key/model.
                if "401" not in last_error and "403" not in last_error and "UNAUTHENTICATED" not in last_error.upper() and "ACCESS_TOKEN_TYPE_UNSUPPORTED" not in last_error.upper():
                    break

    if any(x in last_error.upper() for x in ["401", "403", "UNAUTHENTICATED", "ACCESS_TOKEN_TYPE_UNSUPPORTED", "INVALID_API_KEY", "API KEY NOT VALID"]):
        return False, (
            "Gemini authentication was rejected by Google. The app now tries both documented API-key header styles "
            "for each configured key. If both are rejected, create a fresh Gemini auth key in Google AI Studio, "
            "replace GEMINI_API_KEY / GEMINI_API_KEY_2, and redeploy. This is not a prompt failure. "
            f"Last check: {last_error}"
        )
    return False, f"Gemini temporarily unavailable. Detail: {last_error}"


def gemini_analyze_image(image_bytes: bytes, user_prompt: str = "") -> str:
    """Analyze an uploaded image with the same REST/API-key path as normal Gemini text."""
    keys = gemini_keys()
    if not keys:
        return ""
    for api_key in keys:
        for model in configured_models():
            try:
                prompt = (
                    "Analyze this uploaded image and describe only what is visibly present. "
                    f"Then explain how to apply this requested edit: {user_prompt}. "
                    "Preserve the person's identity, pose, objects and composition unless the user explicitly asks to change them."
                )
                payload = {
                    "contents": [{"parts": [
                        {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(image_bytes).decode("utf-8")}},
                        {"text": prompt},
                    ]}],
                }
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{urllib.parse.quote(model, safe='')}:generateContent"
                r = requests.post(url, headers={"x-goog-api-key": api_key, "Content-Type": "application/json"}, json=payload, timeout=90)
                if not r.ok:
                    if r.status_code in (401, 403):
                        break
                    continue
                data = r.json()
                parts = (((data.get("candidates") or [{}])[0]).get("content") or {}).get("parts") or []
                text = "".join(str(x.get("text", "")) for x in parts if isinstance(x, dict) and x.get("text"))
                if text.strip():
                    return text.strip()
            except Exception:
                continue
    return ""


def render_answer(answer):
    if answer is None:
        return
    st.markdown(answer)


# ============================================================
# FFMPEG & AUDIO / MP3 SYNTHESIZER
# ============================================================

def ffmpeg_bin():
    """Find FFmpeg from Streamlit/apt packages or the imageio Python bundle."""
    # Streamlit Community Cloud installs packages.txt with apt-get. Prefer that
    # real system binary when available. The previous version only checked
    # imageio_ffmpeg, so a perfectly valid packages.txt installation was missed.
    system_exe = shutil.which("ffmpeg")
    if system_exe:
        return system_exe
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and Path(exe).exists():
            return exe
    except Exception:
        pass
    return None


def generate_synthesized_music(duration_sec: int = 10, style: str = "Bollywood", requested_format: str = "mp3"):
    """
    Generates polyphonic audio (kick drums, bass line, chords, melody) matching selected style/duration.
    Converts output dynamically to MP3 using FFmpeg if available.
    """
    sample_rate = 22050
    num_samples = int(sample_rate * duration_sec)
    
    if "Bollywood" in style or "Folk" in style or "Devotional" in style:
        scale = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
    elif "Lo-Fi" in style or "Chill" in style:
        scale = [220.00, 261.63, 293.66, 329.63, 392.00]
    elif "EDM" in style or "Synthwave" in style:
        scale = [130.81, 146.83, 164.81, 174.61, 196.00, 220.00, 246.94]
    elif "Rap" in style or "Hip Hop" in style:
        scale = [110.00, 130.81, 146.83, 164.81, 196.00]
    else:
        scale = [261.63, 293.66, 329.63, 392.00, 440.00]

    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        
        note_dur = 0.22
        samples_per_note = int(sample_rate * note_dur)
        
        frames = []
        for i in range(num_samples):
            t = i / sample_rate
            note_idx = (i // samples_per_note) % len(scale)
            freq = scale[note_idx]
            
            # Sub-bass layer
            bass_freq = freq / 2.0
            bass = 0.35 * math.sin(2 * math.pi * bass_freq * t)
            
            # Polyphonic lead melody with envelope decay
            pos_in_note = (i % samples_per_note) / samples_per_note
            envelope = math.exp(-2.8 * pos_in_note)
            
            lead = 0.45 * math.sin(2 * math.pi * freq * t)
            lead += 0.22 * math.sin(2 * math.pi * (freq * 1.5) * t)
            lead += 0.12 * math.sin(2 * math.pi * (freq * 2.0) * t)
            
            # Percussion kick pulse every half second
            beat_cycle = (i % int(sample_rate * 0.5)) / (sample_rate * 0.5)
            kick = math.sin(2 * math.pi * 65 * (1 - beat_cycle) * t) * math.exp(-12 * beat_cycle) if beat_cycle < 0.25 else 0
            
            val = (lead * envelope) + bass + (kick * 0.4)
            sample = int(val * 14000)
            sample = max(-32768, min(32767, sample))
            frames.append(struct.pack('<h', sample))
            
        wav_file.writeframes(b''.join(frames))
        
    wav_bytes = buffer.getvalue()
    
    # Encode WAV to MP3 using FFmpeg executable
    exe = ffmpeg_bin()
    if requested_format == "mp3" and exe:
        try:
            with tempfile.TemporaryDirectory() as td:
                td = Path(td)
                in_file = td / "temp.wav"
                out_file = td / "song.mp3"
                in_file.write_bytes(wav_bytes)
                
                cmd = [
                    exe, "-y", "-i", str(in_file),
                    "-codec:a", "libmp3lame",
                    "-b:a", "192k",
                    str(out_file)
                ]
                res = subprocess.run(cmd, capture_output=True, timeout=60)
                if res.returncode == 0 and out_file.exists():
                    return out_file.read_bytes(), "audio/mp3", "mp3"
        except Exception:
            pass
            
    return wav_bytes, "audio/wav", "wav"


# ============================================================
# VIDEO TOOLS
# ============================================================

def video_to_audio(data: bytes, suffix=".mp4"):
    exe = ffmpeg_bin()
    if not exe:
        raise RuntimeError("FFmpeg runtime unavailable. Add FFmpeg to packages.txt or use a Streamlit image that includes it.")
    if not data:
        raise RuntimeError("The uploaded video is empty.")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        safe_suffix = suffix if suffix.lower() in {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"} else ".mp4"
        source = td / ("source" + safe_suffix)
        output = td / "audio.mp3"
        source.write_bytes(data)
        command = [
            exe, "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(source), "-map", "0:a:0?", "-vn", "-sn", "-dn",
            "-codec:a", "libmp3lame", "-q:a", "2", "-threads", "0", str(output),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        if result.returncode != 0 or not output.exists() or output.stat().st_size < 1024:
            detail = (result.stderr or result.stdout or "No audio stream found")[-1800:]
            raise RuntimeError(f"Audio extraction failed: {detail}")
        return output.read_bytes()


def _ffprobe_duration(path: Path) -> float:
    """Read media duration using the ffmpeg executable bundled by imageio_ffmpeg."""
    exe = ffmpeg_bin()
    if not exe:
        return 0.0
    try:
        result = subprocess.run(
            [exe, "-hide_banner", "-i", str(path)],
            capture_output=True, text=True, timeout=30,
        )
        text = result.stderr or result.stdout or ""
        match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", text)
        if not match:
            return 0.0
        h, m, sec = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(sec)
    except Exception:
        return 0.0


def make_reel(images, audio_bytes=None, fps=30):
    """Render every supplied image as a slide and fit the complete sequence to the audio when present."""
    exe = ffmpeg_bin()
    if not exe:
        raise RuntimeError("FFmpeg runtime unavailable.")
    if not images:
        raise RuntimeError("No images supplied.")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # Normalize every upload to a real PNG. This avoids extension/content mismatches
        # when users upload JPG/WEBP but the old code wrote them as .png.
        normalized = []
        for index, data in enumerate(images):
            src = td / f"upload_{index:03d}"
            src.write_bytes(data)
            png = td / f"image_{index:03d}.png"
            conv = subprocess.run(
                [exe, "-y", "-i", str(src), "-vf", "format=yuv420p", str(png)],
                capture_output=True, text=True, timeout=60,
            )
            if conv.returncode != 0 or not png.exists():
                raise RuntimeError(f"Could not decode reel image {index + 1}.")
            normalized.append(png)

        audio_path = None
        audio_duration = 0.0
        if audio_bytes:
            audio_path = td / "music_input"
            audio_path.write_bytes(audio_bytes)
            audio_duration = _ffprobe_duration(audio_path)

        # With audio, distribute the available song duration across ALL photos so
        # a short song cannot leave the user seeing only the first image.
        if audio_duration > 0:
            slide_duration = max(0.5, audio_duration / len(normalized))
        else:
            slide_duration = 3.0
        total_duration = slide_duration * len(normalized)

        concat_file = td / "list.txt"
        lines = []
        for image_path in normalized:
            # concat demuxer requires escaped absolute paths.
            safe = str(image_path).replace("'", "'\\''")
            lines.append(f"file '{safe}'")
            lines.append(f"duration {slide_duration:.6f}")
        lines.append(f"file '{str(normalized[-1]).replace(chr(39), chr(39)+chr(92)+chr(39)+chr(39))}'")
        concat_file.write_text("\n".join(lines), encoding="utf-8")

        output = td / "reel.mp4"
        command = [exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file)]
        if audio_path:
            command += ["-i", str(audio_path)]
        command += [
            "-t", f"{total_duration:.3f}",
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p",
            "-r", str(fps), "-c:v", "libx264", "-preset", "veryfast", "-movflags", "+faststart",
        ]
        if audio_path:
            command += ["-c:a", "aac", "-b:a", "192k", "-map", "0:v:0", "-map", "1:a:0"]
        else:
            command += ["-an"]
        command += [str(output)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        if result.returncode != 0 or not output.exists():
            detail = (result.stderr or result.stdout or "FFmpeg failed")[-1800:]
            raise RuntimeError(f"Reel rendering failed: {detail}")
        return output.read_bytes()


# ============================================================
# LIVE NEWS RSS
# ============================================================

LANGUAGES = {
    "English": "en", "తెలుగు": "te", "हिन्दी": "hi", "தமிழ்": "ta",
    "ಕನ್ನಡ": "kn", "മലയാളം": "ml", "বাংলা": "bn", "मराठी": "mr",
    "ગુજરાતી": "gu", "ਪੰਜਾਬੀ": "pa",
}

RSS_FEEDS = {
    "English": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
    "తెలుగు": "https://news.google.com/rss?hl=te&gl=IN&ceid=IN:te",
    "हिन्दी": "https://news.google.com/rss?hl=hi&gl=IN&ceid=IN:hi",
    "தமிழ்": "https://news.google.com/rss?hl=ta&gl=IN&ceid=IN:ta",
    "ಕನ್ನಡ": "https://news.google.com/rss?hl=kn&gl=IN&ceid=IN:kn",
    "മലയാളം": "https://news.google.com/rss?hl=ml&gl=IN&ceid=IN:ml",
    "বাংলা": "https://news.google.com/rss?hl=bn&gl=IN&ceid=IN:bn",
    "मराठी": "https://news.google.com/rss?hl=mr&gl=IN&ceid=IN:mr",
    "ગુજરાતી": "https://news.google.com/rss?hl=gu&gl=IN&ceid=IN:gu",
    "ਪੰਜਾਬੀ": "https://news.google.com/rss?hl=pa&gl=IN&ceid=IN:pa",
}


def fetch_rss(url: str, limit: int = 10):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code != 200:
            return []
        root = ET.fromstring(r.content)
        items = []
        for item in root.findall(".//item")[:limit]:
            items.append({
                "title": html.unescape(item.findtext("title") or "No Title"),
                "link": item.findtext("link") or "#",
                "pubDate": item.findtext("pubDate") or "",
                "source": item.findtext("source") or "",
            })
        return items
    except Exception:
        return []


def social_links(text: str, url: str = CHANNEL_URL):
    encoded_text = urllib.parse.quote(text)
    encoded_url = urllib.parse.quote(url)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f'<div class="share-whatsapp"><a href="https://api.whatsapp.com/send?text={encoded_text}%20{encoded_url}" target="_blank" style="display:block;text-align:center;padding:10px;border-radius:12px;text-decoration:none;color:#fff;font-weight:bold;">WhatsApp</a></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="share-facebook"><a href="https://www.facebook.com/sharer/sharer.php?u={encoded_url}" target="_blank" style="display:block;text-align:center;padding:10px;border-radius:12px;text-decoration:none;color:#fff;font-weight:bold;">Facebook</a></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="share-x"><a href="https://twitter.com/intent/tweet?text={encoded_text}&url={encoded_url}" target="_blank" style="display:block;text-align:center;padding:10px;border-radius:12px;text-decoration:none;color:#fff;font-weight:bold;">X (Twitter)</a></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="share-linkedin"><a href="https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}" target="_blank" style="display:block;text-align:center;padding:10px;border-radius:12px;text-decoration:none;color:#fff;font-weight:bold;">LinkedIn</a></div>', unsafe_allow_html=True)
    with c5:
        st.markdown(f'<div class="share-instagram"><a href="{CHANNEL_URL}" target="_blank" style="display:block;text-align:center;padding:10px;border-radius:12px;text-decoration:none;color:#fff;font-weight:bold;">YouTube</a></div>', unsafe_allow_html=True)


def go(page: str):
    # IMPORTANT: do not mutate the state of an already-created widget.
    # Streamlit raises StreamlitWidgetAlreadyInstantiatedError when a widget
    # key is changed after that widget has been instantiated in the same run.
    # The sidebar radio below is intentionally keyless; it derives its value
    # from the application route before it is created.
    st.session_state["nav"] = page
    st.rerun()


# ============================================================
# PAGES
# ============================================================

def page_home():
    st.markdown('<div class="hero"><h1>NavaBharat AI</h1><p>Your all-in-one suite for AI problem solving, music generation, science, instant multi-language translation, live information, job search, and video creator tools. Powered by RacharlaGPT.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="card home-card-1"><h3>🧠 Solve Anything</h3><p>Ask complex questions, uploaded homework images, or real-world problems and get step-by-step reasoning.</p></div>', unsafe_allow_html=True)
        if st.button("🧠 Open Solve Anything", key="home_solve"): go("🧠 Solve Anything")
        
        st.markdown('<div class="card home-card-3"><h3>🔬 AI Science Solver</h3><p>Solve physics, chemistry, biology, math, and engineering problems with clear explanations.</p></div>', unsafe_allow_html=True)
        if st.button("🔬 Open Science Solver", key="home_sci"): go("🔬 AI Science Solver")
        
        st.markdown('<div class="card home-card-5"><h3>🎨 Free AI Image Generator</h3><p>Generate sharp, clear photorealistic photos, digital art, anime, and transform uploaded photos instantly.</p></div>', unsafe_allow_html=True)
        if st.button("🎨 Open AI Image Generator", key="home_image_gen"): go("🎨 Free AI Image Generator")

    with c2:
        st.markdown('<div class="card home-card-7"><h3 style="color:#c084fc;">🎼 Free AI Music Generator</h3><p style="color:#cbd5e1;">Compose custom songs, arrange lyrics, select genres, and generate 5s to 60s free MP3 audio tracks with a neon interface.</p></div>', unsafe_allow_html=True)
        if st.button("🎼 Open AI Music Generator", key="home_music_gen"): go("🎼 Free AI Music Generator")
        
        st.markdown('<div class="card home-card-2"><h3>🌐 Translator</h3><p>Translate between English, Telugu, Hindi, Tamil, Kannada, Malayalam, Bengali, Gujarati, Punjabi, and Marathi.</p></div>', unsafe_allow_html=True)
        if st.button("🌐 Open Translator", key="home_trans"): go("🌐 Translator")
        
        st.markdown('<div class="card home-card-4"><h3>📡 Live Information</h3><p>Get grounded search answers and latest live Google News RSS feeds across Indian languages.</p></div>', unsafe_allow_html=True)
        if st.button("📡 Open Live Info", key="home_live"): go("📡 Live Information")

        st.markdown('<div class="card home-card-6"><h3>🗞️ Daily Current Affairs</h3><p>Read today&apos;s latest headlines in Telugu, English, Hindi and other Indian languages, then generate a quiz.</p></div>', unsafe_allow_html=True)
        if st.button("🗞️ Open Daily Current Affairs", key="home_current_affairs"): go("🗞️ Daily Current Affairs")
        if st.link_button("▶️ Open RacharlaGPT YouTube", CHANNEL_URL, type="secondary"):
            pass


def page_solve():
    st.markdown('<div class="hero"><h1>🧠 Solve Anything</h1><p>Get comprehensive, step-by-step solutions for any topic or upload a photo of your problem.</p></div>', unsafe_allow_html=True)
    query = st.text_area("Enter your question or problem prompt", height=140, placeholder="Type any math, coding, logical, general knowledge, or creative problem...", key="solve_query")
    uploaded = st.file_uploader("Optional: Attach Image or Document", type=["png", "jpg", "jpeg", "webp", "pdf", "txt"], key="solve_file")

    if st.button("🚀 Solve Problem", key="solve_btn"):
        if not query.strip() and not uploaded:
            st.warning("Please enter a question or upload a file.")
        else:
            with st.spinner("Analyzing and solving..."):
                full_prompt = f"Please solve this problem step by step with full clarity:\n{query}"
                if uploaded: full_prompt += f"\n[User attached file: {uploaded.name}]"
                ok, answer = gemini_generate(full_prompt)
                if ok:
                    render_answer(answer)
                    st.markdown("---")
                    st.markdown("### 📤 Share Solution")
                    social_links(f"Check out this solution on NavaBharat AI: {query[:80]}", CHANNEL_URL)
                else:
                    st.error(answer)


def generate_gemini_image(prompt: str, image_bytes=None, mime_type: str = "image/png",
                          aspect_ratio: str = "1:1", image_size: str = "2K"):
    """Generate/edit with Gemini 3.1 Flash Image using the documented Interactions API."""
    keys = gemini_keys()
    if not keys:
        return None, None, "No Gemini API key is configured."
    last_error = ""
    model = safe_secret("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image")
    for key_index, api_key in enumerate(keys, start=1):
        for bearer in (False, True):
            try:
                inputs = []
                if image_bytes:
                    inputs.append({"type": "image", "mime_type": mime_type or "image/png", "data": base64.b64encode(image_bytes).decode("utf-8")})
                inputs.append({"type": "text", "text": prompt})
                payload = {
                    "model": model,
                    "input": inputs,
                    "response_format": {"type": "image", "mime_type": "image/png", "aspect_ratio": aspect_ratio, "image_size": image_size},
                }
                response = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/interactions",
                    headers=_gemini_auth_headers(api_key, bearer=bearer),
                    json=payload, timeout=180,
                )
                raw = response.text[:1600]
                if not response.ok:
                    last_error = f"Gemini image key {key_index} rejected (HTTP {response.status_code}, {'Bearer' if bearer else 'x-goog-api-key'}): {raw}"
                    if _gemini_is_auth_error(response.status_code, raw):
                        continue
                    continue
                body = response.json()
                out = body.get("output_image") or body.get("outputImage") or {}
                data = out.get("data") if isinstance(out, dict) else None
                if data:
                    return base64.b64decode(data), out.get("mime_type") or out.get("mimeType") or "image/png", ""
                for step in body.get("steps", []) or []:
                    if not isinstance(step, dict):
                        continue
                    for block in step.get("content", []) or []:
                        if isinstance(block, dict) and block.get("type") == "image" and block.get("data"):
                            return base64.b64decode(block["data"]), block.get("mime_type") or block.get("mimeType") or "image/png", ""
                last_error = f"Gemini image key {key_index}: successful request but no image block was returned."
            except Exception as exc:
                last_error = f"Gemini image key {key_index}: {clean_error(exc)}"
    if any(x in last_error.upper() for x in ["401", "403", "ACCESS_TOKEN_TYPE_UNSUPPORTED", "UNAUTHENTICATED", "INVALID_API_KEY"]):
        return None, None, (
            "Gemini image authentication was rejected. The app tried both current Gemini authentication header styles "
            "with both configured keys. If both fail, replace the Gemini keys in Streamlit Secrets with fresh AI Studio auth keys. "
            + last_error
        )
    return None, None, last_error or "No image was returned by Gemini."


def sharpen_image_bytes(data: bytes) -> bytes:
    """Light lossless-ish post-processing to reduce soft/blurred-looking output."""
    try:
        from PIL import Image, ImageFilter
        src = Image.open(io.BytesIO(data)).convert("RGB")
        # Upscale small outputs before sharpening; never enlarge aggressively.
        if min(src.size) < 900:
            scale = 900 / min(src.size)
            src = src.resize((int(src.width * scale), int(src.height * scale)), Image.Resampling.LANCZOS)
        src = src.filter(ImageFilter.UnsharpMask(radius=1.4, percent=145, threshold=3))
        out = io.BytesIO()
        src.save(out, format="PNG", optimize=True)
        return out.getvalue()
    except Exception:
        return data


def page_image_generator():
    st.markdown(
        '<div class="hero"><h1>🎨 Free AI Image Studio</h1>'
        '<p>Native Gemini image generation/editing with a sharpened fallback renderer.</p></div>',
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["✨ Text to AI Image", "🖼️ Upload Image & AI Re-imagine"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            prompt = st.text_area(
                "Image Description / Prompt",
                height=150,
                placeholder="Describe exactly what you want. Example: a sharp realistic portrait, natural skin texture, clear eyes, detailed hair, clean background, no blur...",
                key="img_prompt",
            )
        with col2:
            style = st.selectbox(
                "Art Style",
                ["Photorealistic", "Digital Art", "Anime / Manga", "Cinematic", "3D Render", "Fantasy Art", "Cyberpunk"],
                key="img_style",
            )
            aspect = st.selectbox(
                "Aspect Ratio",
                ["1:1 (Square)", "16:9 (Landscape)", "9:16 (Portrait / Reel)"],
                key="img_aspect",
            )
            size = st.selectbox("Image Quality", ["1K", "2K"], index=1, key="img_size")

        if st.button("🎨 Generate Sharp AI Image", key="gen_img_btn"):
            if not prompt.strip():
                st.warning("Please enter an image description.")
            else:
                aspect_ratio = {"1:1 (Square)": "1:1", "16:9 (Landscape)": "16:9", "9:16 (Portrait / Reel)": "9:16"}[aspect]
                width, height = {"1:1 (Square)": (1024, 1024), "16:9 (Landscape)": (1536, 864), "9:16 (Portrait / Reel)": (864, 1536)}[aspect]
                style_instruction = {
                    "Photorealistic": "photorealistic photography",
                    "Digital Art": "high-detail digital illustration",
                    "Anime / Manga": "anime / manga illustration",
                    "Cinematic": "cinematic live-action photography",
                    "3D Render": "high-end 3D render",
                    "Fantasy Art": "detailed fantasy concept art",
                    "Cyberpunk": "cinematic cyberpunk concept art",
                }[style]
                quality_prompt = (
                    f"Create exactly this requested image: {prompt.strip()}. "
                    f"Visual style: {style_instruction}. "
                    "The user's requested subjects and actions are the highest priority; do not replace them with unrelated people, countries, clothing, "
                    "K-pop/Korean styling, random portraits, or unrelated scenes. Keep every explicit object, action, location, ethnicity/nationality descriptor, "
                    "food/object identity, and composition instruction from the user. "
                    "Use sharp focus, crisp edges, realistic fine details, coherent anatomy, clear objects, professional lighting, and high resolution. "
                    "Avoid blur, haze, smeared details, duplicate objects, warped faces, distorted hands, low resolution, random text, logos, and watermarks."
                )
                with st.spinner("Generating high-quality image..."):
                    img_bytes, mime, image_error = generate_gemini_image(
                        quality_prompt,
                        aspect_ratio=aspect_ratio,
                        image_size=size,
                    )

                    if img_bytes:
                        img_bytes = sharpen_image_bytes(img_bytes)
                        st.image(img_bytes, caption=f"Generated {style} image", use_container_width=True)
                        st.download_button(
                            "⬇️ Download Image",
                            data=img_bytes,
                            file_name="navabharat_ai_image.png",
                            mime="image/png",
                            key="dl_gen_img",
                        )
                        st.markdown("### 📤 Share Creation")
                        social_links(f"AI image created on NavaBharat AI: {prompt[:80]}", CHANNEL_URL)
                    else:
                        st.error(f"Image generation failed: {image_error}")
                        st.info("No unrelated fallback image is shown. Fix the Gemini key/model and generate again.")

    with tab2:
        st.markdown("### 📤 Upload Your Image for AI Transformation")
        user_img = st.file_uploader(
            "Upload Image to Transform",
            type=["png", "jpg", "jpeg", "webp"],
            key="user_img_uploader",
        )
        user_mod_prompt = st.text_input(
            "How should AI transform your uploaded image?",
            placeholder="Example: keep the person and face recognizable, change the background to a beach at sunset, cinematic lighting...",
            key="user_mod_prompt",
        )

        if st.button("⚡ Transform Uploaded Image", key="transform_img_btn"):
            if not user_img:
                st.warning("Please upload an image file first.")
            elif not user_mod_prompt.strip():
                st.warning("Please describe the transformation.")
            else:
                with st.spinner("Editing your image with Gemini image generation..."):
                    image_bytes = user_img.getvalue()
                    mime_in = user_img.type or "image/png"
                    edit_prompt = (
                        f"Edit ONLY the supplied image according to this exact request: {user_mod_prompt.strip()}. "
                        "Treat the uploaded image as the source of truth for the existing subject. Do not substitute a different person, country, ethnicity, "
                        "style, or unrelated scene. Preserve identity, pose, anatomy, important objects, and composition unless the request explicitly changes them. "
                        "If the request says to add or replace an object, make that requested object clearly visible and physically integrated into the scene. "
                        "Create a sharp, high-resolution result with crisp edges, clear facial details, natural skin texture, accurate hands, coherent lighting, "
                        "and no blur, haze, smeared features or distorted anatomy."
                    )
                    transformed, out_mime, edit_error = generate_gemini_image(
                        edit_prompt,
                        image_bytes=image_bytes,
                        mime_type=mime_in,
                        aspect_ratio="1:1",
                        image_size="2K",
                    )
                    if transformed:
                        transformed = sharpen_image_bytes(transformed)
                        st.image(transformed, caption="AI-transformed image", use_container_width=True)
                        st.download_button(
                            "⬇️ Download Transformed Image",
                            data=transformed,
                            file_name="navabharat_transformed_ai.png",
                            mime="image/png",
                            key="dl_transformed_img",
                        )
                    else:
                        st.error(f"Gemini image editing failed: {edit_error}")


def acestep_key():
    # Support the names people commonly use for the ACE-Step cloud key.
    return (
        safe_secret("ACESTEP_API_KEY")
        or safe_secret("ACE_API_KEY")
        or safe_secret("ACE_APP_KEY")
    )


def _acestep_audio_bytes_from_response(body):
    """Extract ACE-Step inline audio from current completion-mode responses."""
    found = []

    def inspect(obj):
        if isinstance(obj, dict):
            # Standard completion response: audio_url.url = data:audio/mpeg;base64,...
            au = obj.get("audio_url")
            if isinstance(au, dict) and au.get("url"):
                found.append(au.get("url"))
            if isinstance(obj.get("url"), str) and (obj["url"].startswith("data:audio/") or "," in obj["url"]):
                found.append(obj["url"])
            if isinstance(obj.get("data"), str):
                val = obj["data"]
                if val.startswith("data:audio/") or (len(val) > 1000 and re.fullmatch(r"[A-Za-z0-9+/=\\s]+", val)):
                    found.append(val)
            for value in obj.values():
                inspect(value)
        elif isinstance(obj, list):
            for value in obj:
                inspect(value)

    inspect(body)
    for value in found:
        try:
            if value.startswith("data:"):
                header, encoded = value.split(",", 1)
                raw = base64.b64decode(encoded)
                if raw:
                    if "mpeg" in header or "mp3" in header:
                        return raw, "audio/mpeg", "mp3"
                    if "wav" in header:
                        return raw, "audio/wav", "wav"
                    return raw, header.split(";", 1)[0], "audio"
            else:
                raw = base64.b64decode(value)
                if raw:
                    return raw, "audio/mpeg", "mp3"
        except Exception:
            continue

    detail = body.get("error") or body.get("message") or body.get("choices") or body
    if isinstance(detail, (dict, list)):
        detail = json.dumps(detail, ensure_ascii=False)[:2500]
    raise RuntimeError(f"ACE-Step returned no usable audio: {detail}")


def generate_song_with_acestep(duration_sec: int, style: str, lyrics: str, vocal_type: str):
    """Generate a real song with vocals + instruments using ACE Music cloud API.

    ACE Music's current cloud API is OpenAI-compatible:
    POST /v1/chat/completions. It returns audio inline, so no task polling is needed.
    """
    key = acestep_key()
    if not key:
        return None, None, None, "ACESTEP_API_KEY/ACE_API_KEY/ACE_APP_KEY is not configured."

    base_url = safe_secret("ACESTEP_BASE_URL", "https://api.acemusic.ai").rstrip("/")
    model = safe_secret("ACESTEP_MODEL", "acemusic/acestep-v1.5-turbo")
    vocal_language = safe_secret("ACESTEP_VOCAL_LANGUAGE", "en")

    # Give ACE-Step enough musical context to produce a complete song rather than
    # an instrumental loop. Lyrics are kept verbatim and vocals are explicitly requested.
    prompt = (
        f"<prompt>Create a complete finished song in the style of {style}. "
        f"Use {vocal_type}. Include clear lead vocals, musical accompaniment, "
        f"drums, bass and harmony appropriate to the genre, a distinct verse and chorus, "
        f"and a polished beginning and ending. Do not make it instrumental. "
        f"Perform the supplied lyrics naturally and keep the lyrics language.</prompt>\n"
        f"<lyrics>{lyrics.strip()}</lyrics>"
    )

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "audio_config": {
            "format": "mp3",
            "vocal_language": vocal_language,
            "instrumental": False,
            "duration": float(duration_sec),
        },
        "use_cot_caption": False,
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        # ACE-Step integrations document a curl-like User-Agent for the cloud API.
        "User-Agent": "curl/8.4.0",
    }

    try:
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=75,
        )
        if not response.ok:
            detail = response.text[:3000]
            if response.status_code == 504:
                return None, None, None, (
                    "ACE-Step cloud is currently overloaded and Cloudflare timed out the generation (HTTP 504). "
                    "This is a remote-service failure, not a Streamlit code error. Please retry after a short wait, "
                    "or use a shorter 5–10 second generation while the cloud queue is busy."
                )
            return None, None, None, (
                f"ACE-Step API HTTP {response.status_code} at {base_url}/v1/chat/completions: {detail}"
            )

        body = response.json()
        audio_bytes, mime_type, fmt = _acestep_audio_bytes_from_response(body)

        # The API may return WAV data even when MP3 was requested. Convert when
        # ffmpeg is available; otherwise preserve the actual returned format.
        if fmt == "wav" and shutil.which("ffmpeg"):
            try:
                wav_path = os.path.join(tempfile.gettempdir(), f"ace_{uuid.uuid4().hex}.wav")
                mp3_path = os.path.join(tempfile.gettempdir(), f"ace_{uuid.uuid4().hex}.mp3")
                with open(wav_path, "wb") as fh:
                    fh.write(audio_bytes)
                subprocess.run(
                    ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path, "-codec:a", "libmp3lame", "-q:a", "2", mp3_path],
                    check=True,
                    timeout=120,
                )
                with open(mp3_path, "rb") as fh:
                    audio_bytes = fh.read()
                for path in (wav_path, mp3_path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass
                mime_type, fmt = "audio/mpeg", "mp3"
            except Exception:
                # Keep the valid WAV instead of failing a successful generation.
                mime_type, fmt = "audio/wav", "wav"

        return audio_bytes, mime_type, fmt, ""
    except requests.exceptions.Timeout:
        return None, None, None, "ACE-Step cloud request timed out. Try a shorter song or try again."
    except requests.exceptions.RequestException as exc:
        return None, None, None, clean_error(exc)
    except Exception as exc:
        return None, None, None, clean_error(exc)

def generate_song_track(duration_sec: int, style: str, lyrics: str, vocal_type: str):
    """
    Creates a complete procedural song-like track: stereo accompaniment,
    chords, bass, percussion and a vowel/formant melody derived from lyrics.
    This is intentionally offline and does not require a third-party music API.
    """
    sample_rate = 22050
    total = int(sample_rate * duration_sec)

    if "EDM" in style or "Synthwave" in style:
        scale = [110.0, 130.81, 146.83, 164.81, 196.0, 220.0, 246.94]
        bpm = 120
    elif "Hip Hop" in style or "Rap" in style:
        scale = [110.0, 130.81, 146.83, 164.81, 196.0]
        bpm = 92
    elif "Devotional" in style or "Classical" in style:
        scale = [261.63, 293.66, 329.63, 392.0, 440.0, 493.88, 523.25]
        bpm = 76
    elif "Folk" in style or "Bollywood" in style:
        scale = [261.63, 293.66, 329.63, 349.23, 392.0, 440.0, 493.88, 523.25]
        bpm = 102
    else:
        scale = [220.0, 261.63, 293.66, 329.63, 392.0]
        bpm = 84

    # Turn lyric words into syllable-ish vowel targets for a melodic vocal synth.
    words = re.findall(r"[A-Za-zÀ-ÿ\u0900-\u0dff]+", lyrics) or ["NavaBharat", "AI"]
    vowels = []
    for word in words:
        chars = [c for c in word.lower() if c in "aeiou"]
        vowels.extend(chars or ["a"])
    if not vowels:
        vowels = ["a", "e", "i", "o", "u"]

    def formant_vowel(t, freq, vowel, attack=0.03, release=0.12):
        # Simple vowel-like harmonic spectrum; intentionally musical, not speech.
        formants = {
            "a": (800, 1150),
            "e": (500, 1900),
            "i": (300, 2200),
            "o": (500, 1000),
            "u": (350, 850),
        }
        f1, f2 = formants.get(vowel, (600, 1200))
        base = math.sin(2 * math.pi * freq * t)
        h2 = 0.45 * math.sin(2 * math.pi * 2 * freq * t)
        h3 = 0.20 * math.sin(2 * math.pi * 3 * freq * t)
        formant1 = 0.08 * math.sin(2 * math.pi * f1 * t)
        formant2 = 0.05 * math.sin(2 * math.pi * f2 * t)
        return base + h2 + h3 + formant1 + formant2

    beat_sec = 60.0 / bpm
    note_sec = beat_sec / 2
    chord_len = int(beat_sec * 4 * sample_rate)
    note_len = max(1, int(note_sec * sample_rate))
    lyric_index = 0

    frames = bytearray()
    for i in range(total):
        t = i / sample_rate
        note_pos = i // note_len
        beat_pos = (i % int(beat_sec * sample_rate)) / sample_rate

        # I-V-vi-IV-like cycle, adapted to the chosen scale.
        root_idx = (note_pos // 8 * 2) % len(scale)
        root = scale[root_idx]
        third = scale[(root_idx + 2) % len(scale)]
        fifth = scale[(root_idx + 4) % len(scale)]
        chord = (
            0.12 * math.sin(2 * math.pi * root * t)
            + 0.08 * math.sin(2 * math.pi * third * t)
            + 0.07 * math.sin(2 * math.pi * fifth * t)
        )

        bass = 0.16 * math.sin(2 * math.pi * (root / 2) * t)

        # Lead melody.
        melody_freq = scale[(note_pos + 1) % len(scale)]
        local = (i % note_len) / note_len
        env = min(1.0, local / 0.08) * max(0.0, 1.0 - max(0.0, (local - 0.72) / 0.28))
        lead = 0.26 * math.sin(2 * math.pi * melody_freq * t) * env

        # Vowel/formant "vocal" layer follows lyric vowels.
        if note_pos % 2 == 0:
            lyric_index = (note_pos // 2) % len(vowels)
        vowel = vowels[lyric_index]
        vocal = 0.0
        if vocal_type != "High Tempo Instrumental Beats":
            vocal_freq = melody_freq * (1.0 if "Solo" in vocal_type else 1.0)
            vocal = 0.18 * formant_vowel(t, vocal_freq, vowel) * env

        # Kick/snare/hi-hat layers.
        kick = 0.0
        if beat_pos < 0.12:
            kick = 0.34 * math.exp(-28 * beat_pos) * math.sin(2 * math.pi * (95 - 45 * beat_pos) * t)
        snare = 0.0
        half = beat_sec / 2
        if half - 0.025 < beat_pos < half + 0.025:
            snare = 0.10 * math.sin(2 * math.pi * 180 * t) * math.exp(-45 * abs(beat_pos - half))
        hat = 0.025 * math.sin(2 * math.pi * 5000 * t) * math.exp(-35 * (beat_pos % (beat_sec / 4)))

        left = chord + bass + lead + vocal + kick + snare + hat
        right = chord * 0.92 + bass + lead * 0.96 + vocal * 1.02 + kick * 0.92 + snare + hat * 0.8

        # Gentle master envelope.
        master = min(1.0, t / 0.12) * min(1.0, (duration_sec - t) / 0.20)
        left = max(-0.92, min(0.92, left * master))
        right = max(-0.92, min(0.92, right * master))

        frames.extend(struct.pack("<hh", int(left * 15000), int(right * 15000)))

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(bytes(frames))
    wav_bytes = buffer.getvalue()

    exe = ffmpeg_bin()
    if exe:
        try:
            with tempfile.TemporaryDirectory() as td:
                td = Path(td)
                source = td / "song.wav"
                output = td / "song.mp3"
                source.write_bytes(wav_bytes)
                result = subprocess.run(
                    [exe, "-y", "-i", str(source), "-codec:a", "libmp3lame", "-b:a", "192k", str(output)],
                    capture_output=True,
                    timeout=120,
                )
                if result.returncode == 0 and output.exists():
                    return output.read_bytes(), "audio/mp3", "mp3"
        except Exception:
            pass

    return wav_bytes, "audio/wav", "wav"


def _extract_gemini_music_audio(body):
    """Extract Lyria audio robustly from convenience or interleaved response blocks."""
    audio_candidates = []
    text_parts = []

    def walk(obj):
        if isinstance(obj, dict):
            typ = str(obj.get("type", "")).lower()
            if typ == "audio" and obj.get("data"):
                audio_candidates.append((obj.get("data"), obj.get("mime_type") or obj.get("mimeType") or "audio/mpeg"))
            if typ in ("text", "output_text"):
                val = obj.get("text") or obj.get("data")
                if val:
                    text_parts.append(str(val))
            for key in ("steps", "content", "output", "model_output"):
                if key in obj:
                    walk(obj[key])
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    # Prefer documented convenience property, then scan the complete response.
    output_audio = body.get("output_audio") or body.get("outputAudio")
    if isinstance(output_audio, dict) and output_audio.get("data"):
        audio_candidates.append((output_audio.get("data"), output_audio.get("mime_type") or output_audio.get("mimeType") or "audio/mpeg"))
    output_text = body.get("output_text") or body.get("outputText")
    if output_text:
        text_parts.append(str(output_text))
    walk(body)

    # Deduplicate identical audio blocks while preserving order.
    seen = set()
    unique = []
    for item in audio_candidates:
        key = item[0]
        if key and key not in seen:
            seen.add(key)
            unique.append(item)
    if not unique:
        return None, None, "Gemini Lyria returned no audio data."

    # If multiple audio blocks are returned, the last block is the documented convenience output.
    audio_b64, audio_mime = unique[-1]
    try:
        raw = base64.b64decode(audio_b64)
    except Exception as exc:
        return None, None, f"Could not decode Gemini music audio: {clean_error(exc)}"
    if not raw:
        return None, None, "Gemini Lyria returned empty audio data."
    mime = str(audio_mime or "audio/mpeg").lower()
    if "wav" in mime:
        ext, mime = "wav", "audio/wav"
    elif "ogg" in mime:
        ext, mime = "ogg", "audio/ogg"
    else:
        ext, mime = "mp3", "audio/mpeg"
    return raw, (mime, ext), "\n\n".join(dict.fromkeys(text_parts)).strip()


def generate_song_with_gemini_lyria(duration_sec: int, style: str, lyrics: str, vocal_type: str):
    """Generate real music through Google's current Lyria 3.5 Gemini API."""
    keys = gemini_keys()
    if not keys:
        return None, None, None, "No Gemini API key is configured."

    model = safe_secret("GEMINI_MUSIC_MODEL", "lyria-3.5")
    if not lyrics.strip():
        lyrics = "Create original lyrics matching the requested theme."
    prompt = f"""
Create an original finished song, not a sound effect and not an instrumental loop.
Style/genre: {style}
Vocal arrangement: {vocal_type}
Target duration: approximately {duration_sec} seconds.
Use the same language as the supplied lyrics/topic.
Use clear human-like singing vocals, drums, bass, harmony, melody and a polished full arrangement.
Structure the song with an intro, verse/chorus movement where appropriate, and a musical ending.
Do not imitate or clone a named real artist's voice.
Do not use copyrighted lyrics unless they were supplied by the user.
User lyrics or song topic:
{lyrics.strip()}
""".strip()

    last_error = ""
    for key_index, api_key in enumerate(keys, start=1):
        for bearer in (False, True):
            try:
                response = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/interactions",
                    headers=_gemini_auth_headers(api_key, bearer=bearer),
                    json={"model": model, "input": prompt, "response_format": {"type": "audio"}},
                    timeout=240,
                )
                raw = response.text[:1200]
                if not response.ok:
                    last_error = f"Gemini music key {key_index}: HTTP {response.status_code} ({'Bearer' if bearer else 'x-goog-api-key'}): {raw}"
                    if _gemini_is_auth_error(response.status_code, raw):
                        continue
                    break
                body = response.json()
                audio_bytes, file_info, lyrics_text = _extract_gemini_music_audio(body)
                if audio_bytes:
                    mime, ext = file_info
                    return audio_bytes, mime, ext, lyrics_text
                last_error = f"Gemini music key {key_index}: {lyrics_text or 'no audio returned'}"
                break
            except requests.exceptions.Timeout:
                last_error = f"Gemini music key {key_index}: request timed out."
            except Exception as exc:
                last_error = f"Gemini music key {key_index}: {clean_error(exc)}"
    return None, None, None, last_error or "Gemini Lyria music generation failed."


def page_music_generator():
    st.markdown(
        '<div class="neon-hero"><h1>🎼 AI Music & Song Generator</h1>'
        '<p>Real AI-generated songs with vocals and instruments. Gemini Lyria 3.5 is primary; ACE-Step is the backup service.</p></div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns([2, 1])
    with c1:
        lyrics_input = st.text_area(
            "📝 Lyrics or Song Topic",
            height=180,
            placeholder="Write original lyrics or describe a song. Example: Telugu motivational song about success...",
            key="mgen_lyrics",
        )
    with c2:
        genre_style = st.selectbox(
            "🎸 Music Style",
            ["Bollywood Romantic / Melodic", "Tollywood Mass Folk / High Beat",
             "Lo-Fi Chill & Acoustic", "EDM / Cyberpunk Synthwave",
             "Cinematic Orchestral Epic", "Hip Hop / Indian Rap",
             "Devotional / Bhakti Fusion", "Classical Fusion & Sitar"],
            key="mgen_genre",
        )
        duration_sec = st.selectbox(
            "⏱️ Target Duration",
            [30, 60, 90, 120],
            index=1,
            format_func=lambda x: f"{x} seconds",
            key="mgen_duration",
        )
        vocal_type = st.selectbox(
            "🎤 Vocal Arrangement",
            ["Solo Male Vocalist", "Solo Female Vocalist", "Male & Female Chorus Duet", "Instrumental"],
            key="mgen_vocal",
        )

    st.caption("Primary: Google Gemini Lyria 3.5 • Backup: ACE-Step cloud. Your second Gemini key is used automatically if the first key fails.")

    if st.button("🎼 Generate Real AI Song", key="mgen_btn"):
        if not lyrics_input.strip():
            st.warning("Please enter original lyrics or a song topic.")
            return

        with st.spinner(f"Generating a real {duration_sec}-second AI song with vocals and instruments..."):
            audio_data = None
            mime_type = None
            fmt = None
            song_text = ""
            primary_error = ""

            # PRIMARY: Gemini Lyria 3.5. This path does not depend on ACE-Step.
            try:
                audio_data, mime_type, fmt, song_text = generate_song_with_gemini_lyria(
                    duration_sec, genre_style, lyrics_input, vocal_type
                )
                if audio_data:
                    st.success("✅ Song generated with Gemini Lyria 3.5.")
            except Exception as exc:
                primary_error = clean_error(exc)

            # SECONDARY: ACE-Step only if Gemini music generation fails.
            if not audio_data:
                st.warning("Gemini Lyria did not return audio. Trying ACE-Step backup...")
                try:
                    audio_data, mime_type, fmt, ace_error = generate_song_with_acestep(
                        duration_sec, genre_style, lyrics_input, vocal_type
                    )
                    if audio_data:
                        st.success("✅ Song generated with ACE-Step backup.")
                    else:
                        primary_error = f"Gemini: {primary_error or 'no audio returned'} | ACE-Step: {ace_error}"
                except Exception as exc:
                    primary_error = f"Gemini: {primary_error or 'no audio returned'} | ACE-Step: {clean_error(exc)}"

            if not audio_data:
                st.error(f"Real AI music generation failed: {primary_error}")
                st.info("No fake/synthetic music is played. Check both Gemini API keys and, if needed, the ACE-Step key.")
                return

            st.audio(audio_data, format=mime_type)
            st.download_button(
                f"⬇️ Download AI Song (.{fmt})",
                data=audio_data,
                file_name=f"navabharat_ai_song_{duration_sec}s.{fmt}",
                mime=mime_type,
                key="dl_generated_song_file",
            )
            if song_text:
                st.markdown("### 🎤 Generated Lyrics / Music Notes")
                render_answer(song_text)

def page_science():
    st.markdown('<div class="hero"><h1>🔬 AI Science Solver</h1><p>Specialized solver for Physics, Chemistry, Biology, Mathematics, and Engineering topics.</p></div>', unsafe_allow_html=True)
    subject = st.selectbox("Select Subject Discipline", ["Physics", "Chemistry", "Biology", "Mathematics", "Engineering & Tech"], key="sci_subj")
    query = st.text_area(f"Enter your {subject} problem or formula prompt", height=140, key="sci_query")

    if st.button("🔬 Resolve Science Problem", key="sci_btn"):
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Generating scientific solution..."):
                prompt = f"You are an expert scientific tutor in {subject}.\nSolve and explain clearly:\n{query}"
                ok, answer = gemini_generate(prompt)
                if ok:
                    render_answer(answer)
                    st.markdown("---")
                    st.markdown("### 📤 Share Science Solution")
                    social_links(f"Check out this {subject} solution on NavaBharat AI: {query[:80]}", CHANNEL_URL)
                else:
                    st.error(answer)


def page_translator():
    st.markdown('<div class="hero"><h1>🌐 Multi-Language Translator</h1><p>Instant translation across major Indian and global languages powered by RacharlaGPT.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: source_lang = st.selectbox("Source Language", list(LANGUAGES.keys()), index=0, key="trans_src")
    with c2: target_lang = st.selectbox("Target Language", list(LANGUAGES.keys()), index=1, key="trans_tgt")

    text = st.text_area("Text to Translate", height=140, placeholder="Type text here...", key="trans_text")

    if st.button("🌐 Translate Now", key="trans_btn"):
        if not text.strip():
            st.warning("Please enter text to translate.")
        else:
            with st.spinner("Translating..."):
                prompt = f"Translate the following text from {source_lang} to {target_lang}.\nProvide direct translation followed by transliteration if applicable.\n\nText:\n{text}"
                ok, answer = gemini_generate(prompt)
                if ok:
                    render_answer(answer)
                    st.markdown("---")
                    st.markdown("### 📤 Share Translation")
                    social_links(f"Translation from {source_lang} to {target_lang}: {text[:60]}", CHANNEL_URL)
                else:
                    st.error(answer)


def page_live():
    st.markdown('<div class="hero"><h1>📡 Live Information & Google News RSS</h1><p>Real-time search answers and live feeds across official news channels.</p></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔍 Live Grounded Search", "📰 RSS News Feeds"])

    with tab1:
        query = st.text_input("Ask for latest live real-world news or updates", placeholder="e.g. Latest Tech updates or Cricket news", key="live_search_q")
        if st.button("🔍 Search Live Web", key="live_search_btn"):
            if not query.strip():
                st.warning("Enter a search topic.")
            else:
                with st.spinner("Searching live web..."):
                    ok, answer = gemini_generate(query, grounded=True)
                    if ok:
                        render_answer(answer)
                    else:
                        # Keep Live Information useful even when Gemini authentication is
                        # temporarily unavailable: Google News RSS is a real live feed and
                        # does not depend on the Gemini key.
                        st.warning("Live AI search is temporarily unavailable, so the app is showing live RSS results for your query instead.")
                        rss_url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&hl=en-IN&gl=IN&ceid=IN:en"
                        items = fetch_rss(rss_url, limit=12)
                        if items:
                            for item in items:
                                st.markdown(
                                    f'<div class="card"><h4><a href="{html.escape(item["link"], quote=True)}" target="_blank">{html.escape(item["title"])}</a></h4>'
                                    f'<p style="font-size:12px;color:#64748b;">{html.escape(item["source"])} · {html.escape(item["pubDate"])}</p></div>',
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.caption(answer)

    with tab2:
        lang = st.selectbox("Select News Language Feed", list(RSS_FEEDS.keys()), key="rss_lang")
        if st.button("🔄 Fetch Latest RSS News", key="rss_btn"):
            with st.spinner("Fetching news RSS..."):
                items = fetch_rss(RSS_FEEDS[lang], limit=12)
                if items:
                    for item in items:
                        st.markdown(f'<div class="card"><h4><a href="{item["link"]}" target="_blank" style="text-decoration:none; color:#2563eb;">{item["title"]}</a></h4><p style="font-size:12px; color:#64748b;">Source: {item["source"]} | Date: {item["pubDate"]}</p></div>', unsafe_allow_html=True)
                else:
                    st.info("Unable to load RSS news feed currently.")


def page_current_affairs():
    st.markdown(
        '<div class="hero"><h1>🗞️ Daily Current Affairs</h1>'
        '<p>Fresh daily headlines and optional AI summaries in Telugu, English, Hindi and other Indian languages.</p></div>',
        unsafe_allow_html=True,
    )

    lang = st.selectbox("Language", list(RSS_FEEDS.keys()), key="ca_lang")
    category = st.selectbox(
        "Category",
        ["All", "India", "World", "Business", "Technology", "Science", "Sports", "Education"],
        key="ca_category",
    )
    count = st.slider("Number of headlines", 5, 20, 12, key="ca_count")

    if st.button("📰 Load Today's Current Affairs", key="ca_load"):
        with st.spinner("Fetching today's latest headlines..."):
            items = fetch_rss(RSS_FEEDS[lang], limit=count * 2)
            if category != "All":
                terms = {
                    "India": ["india", "indian"],
                    "World": ["world", "international", "global"],
                    "Business": ["business", "economy", "market", "finance"],
                    "Technology": ["technology", "tech", "ai", "software"],
                    "Science": ["science", "space", "research"],
                    "Sports": ["sport", "cricket", "football", "tennis"],
                    "Education": ["education", "school", "university", "exam"],
                }[category]
                items = [x for x in items if any(t in x["title"].lower() for t in terms)]
            items = items[:count]

            if not items:
                st.info("No current-affairs items were returned. Try All categories.")
                return

            st.session_state["current_affairs_items"] = items
            st.session_state["current_affairs_lang"] = lang

    items = st.session_state.get("current_affairs_items", [])
    if items:
        st.markdown(f"### 📅 Today's Feed — {st.session_state.get('current_affairs_lang', lang)}")
        for n, item in enumerate(items, 1):
            safe_title = html.escape(item["title"])
            safe_link = html.escape(item["link"], quote=True)
            st.markdown(
                f'<div class="card"><h4>{n}. <a href="{safe_link}" target="_blank" '
                f'style="text-decoration:none;color:#2563eb;">{safe_title}</a></h4>'
                f'<p style="font-size:12px;color:#64748b;">{html.escape(item["source"])} · {html.escape(item["pubDate"])}</p></div>',
                unsafe_allow_html=True,
            )

        if st.button("🤖 Create Daily Current-Affairs Quiz", key="ca_quiz"):
            headline_text = "\n".join(f"- {x['title']}" for x in items)
            with st.spinner("Creating a quiz from today's feed..."):
                ok, quiz = gemini_generate(
                    f"Create 10 current-affairs MCQs from these latest headlines. "
                    f"Answer in {lang}. Do not invent facts not present in the headlines. "
                    f"Give 4 options and mark the correct answer.\n{headline_text}"
                )
                if ok:
                    render_answer(quiz)
                else:
                    st.error(quiz)


def page_jobs_exams():
    st.markdown('<div class="hero"><h1>💼 Jobs & Competitive Exam Alerts</h1><p>Stay updated on latest central & state government jobs, recruitment notifications, and exam updates.</p></div>', unsafe_allow_html=True)
    category = st.selectbox("Select Category", ["All Government Jobs", "Banking & Finance", "SSC & Railways", "UPSC & Civil Services", "State Public Service Commissions"], key="jobs_cat")

    if st.button("🔍 Search Job & Exam Updates", key="jobs_btn"):
        with st.spinner("Fetching latest updates..."):
            prompt = f"Provide latest notifications, exam dates, eligibility, and application details for: {category} in India. Include official portal references where relevant."
            ok, answer = gemini_generate(prompt, grounded=True)
            if ok:
                render_answer(answer)
            else:
                # Key-independent fallback: show current Google News job/exam alerts
                # instead of leaving the feature unusable when Gemini grounding is down.
                st.warning("Gemini live grounding is unavailable, so current job/exam RSS alerts are shown instead.")
                rss_query = f"India {category} government jobs recruitment exam notification"
                rss_url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(rss_query) + "&hl=en-IN&gl=IN&ceid=IN:en"
                items = fetch_rss(rss_url, limit=15)
                if items:
                    for item in items:
                        st.markdown(
                            f'<div class="card"><h4><a href="{html.escape(item["link"], quote=True)}" target="_blank">{html.escape(item["title"])}</a></h4>'
                            f'<p style="font-size:12px;color:#64748b;">{html.escape(item["source"])} · {html.escape(item["pubDate"])}</p></div>',
                            unsafe_allow_html=True,
                        )
                else:
                    st.error(answer)


def page_music():
    st.markdown('<div class="hero"><h1>🎧 RacharlaGPT Music Library</h1><p>Listen to audio tracks and background scores stored in your local music library.</p></div>', unsafe_allow_html=True)
    files = list(MUSIC_DIR.glob("*.*"))
    valid_files = [f for f in files if f.suffix.lower() in [".mp3", ".wav", ".ogg", ".m4a"]]

    if not valid_files:
        st.info("No audio tracks uploaded yet in the music library.")
    else:
        for track in valid_files:
            st.markdown(f"#### 🎧 {track.name}")
            st.audio(str(track))
            st.markdown("---")


def admin_password():
    return (
        safe_secret("ADMIN_PASSWORD")
        or safe_secret("ADMIN_MUSIC_PASSWORD")
        or safe_secret("MUSIC_ADMIN_PASSWORD")
        or safe_secret("NAVA_BHARAT_ADMIN_PASSWORD")
    )


def require_admin_music_access():
    """Require an explicit password from Streamlit Secrets before exposing library controls."""
    configured = admin_password()
    if not configured:
        st.error("Admin Music Library is locked because no admin password secret is configured.")
        st.caption("Add ADMIN_PASSWORD to Streamlit Secrets, then reload the app.")
        return False
    if st.session_state.get("admin_music_authenticated"):
        c1, c2 = st.columns([5, 1])
        with c2:
            if st.button("Logout", key="admin_music_logout"):
                st.session_state["admin_music_authenticated"] = False
                st.rerun()
        return True

    st.warning("🔐 Admin authentication required. The music library is not public.")
    password = st.text_input("Admin Password", type="password", key="admin_music_password_input")
    if st.button("🔓 Login", key="admin_music_login"):
        if password and hmac.compare_digest(password, configured):
            st.session_state["admin_music_authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect admin password.")
    return False


def page_admin_music():
    st.markdown('<div class="hero"><h1>🔐 Admin Music Library Manager</h1><p>Private administrator area for uploading and deleting library tracks.</p></div>', unsafe_allow_html=True)
    if not require_admin_music_access():
        return
    uploaded_files = st.file_uploader("Upload Audio Files (.mp3, .wav, .m4a, .ogg)", type=["mp3", "wav", "m4a", "ogg"], accept_multiple_files=True, key="admin_music_uploader")
    if st.button("💾 Save to Library", key="save_music_btn"):
        if not uploaded_files:
            st.warning("Please select files to upload.")
        else:
            count = 0
            for uf in uploaded_files:
                safe_name = Path(uf.name).name
                dest = MUSIC_DIR / safe_name
                dest.write_bytes(uf.getvalue())
                count += 1
            st.success(f"Saved {count} track(s) to music library.")
            st.rerun()

    st.markdown("### Existing Library Tracks")
    files = list(MUSIC_DIR.glob("*.*"))
    if not files:
        st.caption("Music directory is currently empty.")
    else:
        for f in files:
            c1, c2 = st.columns([4, 1])
            with c1: st.write(f"📄 {f.name}")
            with c2:
                if st.button("🗑️ Delete", key=f"del_{f.name}"):
                    f.unlink(missing_ok=True)
                    st.rerun()


def page_video():
    st.markdown('<div class="hero"><h1>🎬 Video Studio & Audio Extractor</h1><p>Extract MP3 audio from videos or create vertical social reels from images and audio.</p></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🎵 Extract Audio from Video", "🎞️ Build Reel Video"])

    with tab1:
        vid_file = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi", "mkv", "webm"], key="ext_vid_file")
        if st.button("⚡ Extract MP3 Audio", key="ext_audio_btn"):
            if not vid_file:
                st.warning("Upload a video first.")
            else:
                with st.spinner("Extracting MP3 audio..."):
                    try:
                        audio_bytes = video_to_audio(vid_file.getvalue(), suffix=Path(vid_file.name).suffix)
                        st.success("Audio extracted successfully!")
                        st.audio(audio_bytes, format="audio/mp3")
                        st.download_button("⬇️ Download MP3", data=audio_bytes, file_name=f"{Path(vid_file.name).stem}_audio.mp3", mime="audio/mp3", key="dl_audio_extracted")
                    except Exception as exc:
                        st.error(f"Extraction error: {clean_error(exc)}")

    with tab2:
        img_files = st.file_uploader("Upload Reel Slide Images (PNG/JPG)", type=["png", "jpg", "jpeg", "webp"], accept_multiple_files=True, key="reel_imgs")
        bg_music = st.file_uploader("Optional: Upload Background Audio Track", type=["mp3", "wav", "m4a"], key="reel_bgm")

        if st.button("🎞️ Render Vertical Reel (1080x1920)", key="make_reel_btn"):
            if not img_files:
                st.warning("Upload at least one image slide.")
            else:
                with st.spinner("Rendering reel video with FFmpeg..."):
                    try:
                        images_bytes = [f.getvalue() for f in img_files]
                        music_bytes = bg_music.getvalue() if bg_music else None
                        reel_bytes = make_reel(images_bytes, audio_bytes=music_bytes)
                        st.success("Reel generated successfully!")
                        st.video(reel_bytes)
                        st.download_button("⬇️ Download Reel MP4", data=reel_bytes, file_name="navabharat_reel.mp4", mime="video/mp4", key="dl_reel_video")
                    except Exception as exc:
                        st.error(f"Reel generation error: {clean_error(exc)}")


def page_creator():
    st.markdown('<div class="hero"><h1>✨ Creator Studio</h1><p>AI Content Generator for YouTube Titles, Descriptions, Hashtags, & Social Posts.</p></div>', unsafe_allow_html=True)
    topic = st.text_input("Content Topic / Idea", placeholder="e.g. AI tools in 2026 or Budget Smartphone Review", key="creator_topic")
    platform = st.selectbox("Target Platform", ["YouTube Video Script & Metadata", "Instagram Reel Caption & Hashtags", "LinkedIn Thought Leadership Post", "Twitter/X Thread"], key="creator_platform")

    if st.button("✨ Generate Viral Content", key="creator_gen_btn"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Generating content..."):
                prompt = f"You are a professional social media content strategist.\nCreate engaging content for: {platform}\nTopic: {topic}\nInclude catchy headlines, clear structure, call to action, and relevant trending hashtags."
                ok, answer = gemini_generate(prompt)
                if ok:
                    render_answer(answer)
                    st.markdown("---")
                    st.markdown("### 📤 Share Draft")
                    social_links(f"Check out this content draft on NavaBharat AI: {topic[:80]}", CHANNEL_URL)
                else:
                    st.error(answer)


def page_about():
    st.markdown('<div class="hero"><h1>ℹ️ About & System Diagnostics</h1><p>Application configuration, API status, and environment details.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📌 Application Info")
        st.write(f"**App Name:** {APP_NAME}")
        st.write(f"**Version:** {APP_VERSION}")
        st.write(f"**Developer:** {CREATOR}")
        st.write(f"**Brand Tagline:** {TAGLINE}")
        st.write(f"**Official Channel:** [{CHANNEL_URL}]({CHANNEL_URL})")

    with c2:
        st.markdown("### 🔧 API & Secret Status")
        if gemini_keys():
            st.success(f"✅ Gemini API keys configured: {len(gemini_keys())} (automatic failover enabled)")
        else:
            st.error("❌ Gemini API key is missing in secrets")
        if acestep_key():
            st.success("✅ ACE-Step music API key configured (real song generation enabled)")
        else:
            st.warning("⚠️ ACE-Step API key not configured (local synthetic fallback only)")

        ga_sec = safe_secret("GA_MEASUREMENT_ID")
        if ga_sec:
            st.info(f"📊 GA4 Measurement ID: `{ga_sec}`")
            st.caption("Use GA4 Realtime to confirm incoming page_view events after deployment.")

        mon_sec = safe_secret("MONETAG_ZONE_ID")
        if mon_sec:
            st.info(f"💰 Monetag Zone ID: `{mon_sec}`")
        if safe_secret("GOOGLE_SITE_VERIFICATION"):
            st.success("✅ Google site-verification token configured")
        else:
            st.warning("⚠️ GOOGLE_SITE_VERIFICATION secret not configured")
        if safe_secret("MONETAG_VERIFICATION_TAG") or safe_secret("MONETAG_VERIFICATION_META"):
            st.success("✅ Monetag verification code configured")
        else:
            st.warning("⚠️ MONETAG_VERIFICATION_TAG secret not configured")

        if ffmpeg_bin(): st.success("✅ FFmpeg MP3 Encoder active")
        else: st.warning("⚠️ FFmpeg binary not detected (WAV fallback active)")


# ============================================================
# NAVIGATION DICTIONARY
# ============================================================

NAVIGATION = {
    "🏠 Home": page_home,
    "🧠 Solve Anything": page_solve,
    "🎨 Free AI Image Generator": page_image_generator,
    "🎼 Free AI Music Generator": page_music_generator,
    "🔬 AI Science Solver": page_science,
    "🌐 Translator": page_translator,
    "📡 Live Information": page_live,
    "🗞️ Daily Current Affairs": page_current_affairs,
    "💼 Jobs & Exams": page_jobs_exams,
    "🎧 RacharlaGPT Music": page_music,
    "🎬 Video Studio": page_video,
    "✨ Creator Studio": page_creator,
    "🔐 Admin Music Library": page_admin_music,
    "ℹ️ About & Diagnostics": page_about,
}


# ============================================================
# MAIN ENTRYPOINT
# ============================================================

def render_runtime_tags():
    """Run client-side GA4 in the actual Streamlit document when supported."""
    ga_id = safe_secret("GA_MEASUREMENT_ID")
    if not ga_id:
        return
    tag_html = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={html.escape(ga_id)}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{html.escape(ga_id)}');
    </script>
    """
    try:
        if hasattr(st, "html"):
            st.html(tag_html, unsafe_allow_javascript=True)
        else:
            components.html(tag_html, height=0, width=0)
    except Exception:
        try:
            components.html(tag_html, height=0, width=0)
        except Exception:
            pass


def main():
    render_runtime_tags()
    st.sidebar.markdown(f'<div class="sidebar-brand"><div class="mark">🇮🇳</div><div class="name">{APP_NAME}</div><div class="tag">{TAGLINE}</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="nav-caption">Navigation Menu</div>', unsafe_allow_html=True)

    if "nav" not in st.session_state:
        st.session_state["nav"] = "🏠 Home"

    selected_page = st.sidebar.radio(
        "Navigate",
        list(NAVIGATION.keys()),
        index=list(NAVIGATION.keys()).index(st.session_state["nav"]) if st.session_state["nav"] in NAVIGATION else 0,
        label_visibility="collapsed",
    )

    if selected_page != st.session_state["nav"]:
        st.session_state["nav"] = selected_page

    render_fn = NAVIGATION.get(st.session_state["nav"], page_home)
    render_fn()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f'<div style="text-align:center; opacity:.8; font-size:12px; padding:10px 0;"><p style="margin:0; font-weight:bold;">Created by {CREATOR}</p><p style="margin:4px 0 0;"><a href="{CHANNEL_URL}" target="_blank" style="color:#a7f3d0; text-decoration:none;">Visit YouTube Channel ↗</a></p></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
