import html
import os
import re
import shutil
import subprocess
import tempfile
import urllib.parse
from pathlib import Path

import streamlit as st

# ============================================================

# NAVABHARAT AI v6.0.0

# POWERED BY RACHARLAGPT

# ============================================================

APP_NAME = "NavaBharat AI"
BRAND = "RacharlaGPT"
CREATOR = "Racharla Saikrishna"
APP_VERSION = "6.0.0"
TAGLINE = "POWERED BY RACHARLAGPT"

# FIXES:

# - CREATOR NameError

# - navigation KeyError protection

# - DeltaGenerator output

# - music delete

# - social sharing

# - different radiant buttons/cards

# - visible button text

# - responsive page titles

# - Gemini error handling

# - FFmpeg graceful handling

# ============================================================

# STREAMLIT CONFIG

# ============================================================

st.set_page_config(
page_title=f"{APP_NAME} | {BRAND}",
page_icon="🇮🇳",
layout="wide",
initial_sidebar_state="expanded",
)

# ============================================================

# PATHS

# ============================================================

BASE_DIR = Path(**file**).resolve().parent

MUSIC_DIR = BASE_DIR / "racharlagptlibrary"
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================

# SECRETS

# ============================================================

def read_secret(name, default=""):
try:
value = st.secrets.get(name, default)
if value is None:
return default
return str(value)
except Exception:
return default

GEMINI_API_KEY = read_secret("GEMINI_API_KEY")

if not GEMINI_API_KEY:
GEMINI_API_KEY = read_secret("GOOGLE_API_KEY")

GEMINI_MODEL = read_secret(
"GEMINI_MODEL",
"gemini-3.8-flash",
)

ADMIN_PASSWORD = read_secret(
"ADMIN_PASSWORD",
)

# ============================================================

# SESSION STATE

# ============================================================

if "nav_page" not in st.session_state:
st.session_state.nav_page = "Home"

if "admin_authenticated" not in st.session_state:
st.session_state.admin_authenticated = False

if "last_answer" not in st.session_state:
st.session_state.last_answer = ""

# ============================================================

# PREMIUM UI

# ============================================================

st.markdown(
"""

<style>

/* ========================================================
   BACKGROUND
======================================================== */

.stApp {
    background:
        radial-gradient(
            circle at 5% 5%,
            rgba(255, 0, 110, .13),
            transparent 28%
        ),
        radial-gradient(
            circle at 95% 5%,
            rgba(58, 134, 255, .15),
            transparent 28%
        ),
        radial-gradient(
            circle at 10% 95%,
            rgba(0, 184, 148, .13),
            transparent 28%
        ),
        linear-gradient(
            135deg,
            #f8fbff 0%,
            #eef4ff 48%,
            #fbf4ff 100%
        );
}

/* ========================================================
   STREAMLIT
======================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* ========================================================
   TEXT
======================================================== */

.stApp,
.stApp p,
.stApp label,
.stApp span,
.stApp div {
    color: #111827;
}

h1,
h2,
h3,
h4 {
    color: #111827 !important;
}

/* ========================================================
   PAGE TITLE
======================================================== */

.main-page-title {
    display: block;
    width: 100%;
    max-width: 100%;
    margin: 5px 0 10px 0;
    font-size: clamp(1.8rem, 4vw, 3.4rem);
    line-height: 1.12;
    font-weight: 950;
    white-space: normal !important;
    overflow: visible !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
    background:
        linear-gradient(
            90deg,
            #ff006e,
            #8338ec,
            #4361ee,
            #00a896,
            #fb8500
        );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ========================================================
   BRAND BADGE
======================================================== */

.brand-badge {
    display: inline-block;
    padding: 7px 16px;
    border-radius: 999px;
    color: #ffffff !important;
    font-weight: 900;
    font-size: 12px;
    letter-spacing: .07em;
    background:
        linear-gradient(
            120deg,
            #ff006e,
            #8338ec,
            #4361ee,
            #00b894
        );
    box-shadow:
        0 8px 25px rgba(80, 60, 200, .22);
}

/* ========================================================
   GLASS
======================================================== */

.glass-card {
    padding: 22px;
    border-radius: 25px;
    background: rgba(255, 255, 255, .82);
    border: 1px solid rgba(255, 255, 255, .75);
    box-shadow:
        0 18px 55px rgba(31, 38, 135, .13),
        inset 0 1px 0 rgba(255,255,255,.9);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    margin-bottom: 18px;
}

/* ========================================================
   HOME CARDS
======================================================== */

.home-card {
    min-height: 180px;
    padding: 22px;
    border-radius: 27px;
    margin-bottom: 8px;
    color: #ffffff !important;
    box-shadow:
        0 18px 38px rgba(30, 30, 60, .18),
        inset 0 1px 0 rgba(255,255,255,.45);
    transition:
        transform .22s ease,
        box-shadow .22s ease,
        filter .22s ease;
}

.home-card:hover {
    transform: translateY(-7px) scale(1.015);
    filter: brightness(1.06);
    box-shadow:
        0 28px 58px rgba(30, 30, 60, .27),
        inset 0 1px 0 rgba(255,255,255,.65);
}

.home-card h3,
.home-card p,
.home-card div {
    color: #ffffff !important;
}

.gradient-pink {
    background:
        linear-gradient(
            135deg,
            #ff006e,
            #ff4d6d,
            #ff9f1c
        );
}

.gradient-blue {
    background:
        linear-gradient(
            135deg,
            #4361ee,
            #3a86ff,
            #00b4d8
        );
}

.gradient-purple {
    background:
        linear-gradient(
            135deg,
            #7209b7,
            #8338ec,
            #c77dff
        );
}

.gradient-green {
    background:
        linear-gradient(
            135deg,
            #008f7a,
            #00b894,
            #55efc4
        );
}

.gradient-orange {
    background:
        linear-gradient(
            135deg,
            #fb5607,
            #ff9f1c,
            #ffd166
        );
}

.gradient-red {
    background:
        linear-gradient(
            135deg,
            #d00000,
            #e85d04,
            #ff006e
        );
}

.gradient-teal {
    background:
        linear-gradient(
            135deg,
            #0077b6,
            #00b4d8,
            #90e0ef
        );
}

.gradient-indigo {
    background:
        linear-gradient(
            135deg,
            #3f37c9,
            #4895ef,
            #4361ee
        );
}

/* ========================================================
   ALL BUTTONS
======================================================== */

.stButton > button,
.stLinkButton > a,
.stDownloadButton > button {
    min-height: 44px !important;
    border: 0 !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-weight: 900 !important;
    text-shadow:
        0 1px 2px rgba(0,0,0,.32);
    box-shadow:
        0 8px 20px rgba(30,40,80,.15) !important;
    transition:
        transform .2s ease,
        filter .2s ease,
        box-shadow .2s ease !important;
}

.stButton > button:hover,
.stLinkButton > a:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px) scale(1.015);
    filter: brightness(1.08);
    box-shadow:
        0 13px 27px rgba(30,40,80,.21) !important;
}

/* ========================================================
   DEFAULT BUTTON COLORS
======================================================== */

.stButton > button {
    background:
        linear-gradient(
            135deg,
            #4361ee,
            #8338ec
        ) !important;
}

/* ========================================================
   SIDEBAR
======================================================== */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            160deg,
            rgba(255,255,255,.97),
            rgba(239,244,255,.97)
        );
    border-right: 1px solid rgba(80,80,130,.12);
}

section[data-testid="stSidebar"] .stButton > button {
    color: #ffffff !important;
    font-weight: 900 !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(1) button {
    background: linear-gradient(135deg,#ff006e,#ff4d6d) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(2) button {
    background: linear-gradient(135deg,#4361ee,#3a86ff) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(3) button {
    background: linear-gradient(135deg,#7209b7,#8338ec) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(4) button {
    background: linear-gradient(135deg,#008f7a,#00b894) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(5) button {
    background: linear-gradient(135deg,#fb5607,#ff9f1c) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(6) button {
    background: linear-gradient(135deg,#0077b6,#00b4d8) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(7) button {
    background: linear-gradient(135deg,#d00000,#e85d04) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(8) button {
    background: linear-gradient(135deg,#8338ec,#c77dff) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(9) button {
    background: linear-gradient(135deg,#06d6a0,#118ab2) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(10) button {
    background: linear-gradient(135deg,#ef476f,#ff006e) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(11) button {
    background: linear-gradient(135deg,#118ab2,#073b4c) !important;
}

section[data-testid="stSidebar"] .stButton:nth-of-type(12) button {
    background: linear-gradient(135deg,#ff9f1c,#fb5607) !important;
}

/* ========================================================
   INPUTS
======================================================== */

.stTextInput input,
.stTextArea textarea,
textarea,
input {
    background: #ffffff !important;
    color: #111827 !important;
    border-radius: 14px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* ========================================================
   SHARING COLORS
======================================================== */

.share-whatsapp .stLinkButton > a {
    background:
        linear-gradient(
            135deg,
            #00b894,
            #00cec9
        ) !important;
}

.share-instagram .stLinkButton > a {
    background:
        linear-gradient(
            135deg,
            #8338ec,
            #e1306c,
            #ff9f1c
        ) !important;
}

.share-facebook .stLinkButton > a {
    background:
        linear-gradient(
            135deg,
            #1877f2,
            #4267b2
        ) !important;
}

.share-x .stLinkButton > a {
    background:
        linear-gradient(
            135deg,
            #111827,
            #374151
        ) !important;
}

.share-linkedin .stLinkButton > a {
    background:
        linear-gradient(
            135deg,
            #0077b5,
            #00a0dc
        ) !important;
}

/* ========================================================
   MUSIC
======================================================== */

.music-card {
    padding: 20px;
    border-radius: 22px;
    margin-bottom: 15px;
    background:
        linear-gradient(
            135deg,
            rgba(255,0,110,.12),
            rgba(131,56,236,.12),
            rgba(58,134,255,.12)
        );
    border: 1px solid rgba(100,80,200,.16);
}

/* ========================================================
   NOTICE
======================================================== */

.notice {
    padding: 17px;
    border-radius: 18px;
    margin: 15px 0;
    background:
        linear-gradient(
            135deg,
            rgba(0,184,148,.12),
            rgba(58,134,255,.10)
        );
    border: 1px solid rgba(0,184,148,.25);
}

/* ========================================================
   MOBILE
======================================================== */

@media (max-width: 768px) {

    .main-page-title {
        font-size: 2rem !important;
    }

    .home-card {
        min-height: 150px;
        padding: 17px;
    }

    .glass-card {
        padding: 16px;
        border-radius: 20px;
    }
}

</style>

""",
unsafe_allow_html=True,
)

# ============================================================

# HELPERS

# ============================================================

def page_title(title, subtitle=""):
st.markdown(
f'<div class="main-page-title">{html.escape(title)}</div>',
unsafe_allow_html=True,
)

```
st.markdown(
    f'<span class="brand-badge">{html.escape(TAGLINE)}</span>',
    unsafe_allow_html=True,
)

if subtitle:
    st.markdown(
        f'<p style="margin-top:12px;color:#475569;">'
        f'{html.escape(subtitle)}'
        f'</p>',
        unsafe_allow_html=True,
    )
```

def navigate(page):
st.session_state.nav_page = page
st.rerun()

# ============================================================

# GEMINI

# ============================================================

def gemini_client():
if not GEMINI_API_KEY:
return None

```
try:
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)
except Exception:
    return None
```

def gemini_error(exc):
text = str(exc)
upper = text.upper()

```
if "503" in upper or "UNAVAILABLE" in upper:
    return (
        "Gemini is temporarily unavailable or busy. "
        "Your API key was detected. Please try again shortly."
    )

if "429" in upper or "RESOURCE_EXHAUSTED" in upper:
    return (
        "Gemini usage is temporarily limited. "
        "Please wait and try again."
    )

if "401" in upper or "UNAUTHENTICATED" in upper:
    return (
        "Gemini authentication failed. "
        "Please check GEMINI_API_KEY in Streamlit Secrets."
    )

if "403" in upper or "PERMISSION_DENIED" in upper:
    return (
        "Gemini permission was denied. "
        "Check API/model permissions."
    )

if "404" in upper or "NOT_FOUND" in upper:
    return (
        f"Gemini model '{GEMINI_MODEL}' was not found "
        "or is unavailable for this API account."
    )

return f"Gemini request failed: {text}"
```

def ask_ai(prompt):
if not GEMINI_API_KEY:
return (
False,
"GEMINI_API_KEY is not configured in Streamlit Secrets.",
)

```
client = gemini_client()

if client is None:
    return (
        False,
        "google-genai is not installed. "
        "Add google-genai to requirements.txt.",
    )

try:
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    answer = getattr(response, "text", "")

    if not answer:
        return False, "Gemini returned an empty answer."

    return True, str(answer)

except Exception as exc:
    return False, gemini_error(exc)
```

# ============================================================

# SHARING

# ============================================================

def build_share_urls(title, text):
message = (
f"{title}\n\n"
f"{text}\n\n"
f"{TAGLINE}"
)

```
encoded = urllib.parse.quote(message)

app_url = (
    "https://navabharatai.racharlagpt.in"
)

return {
    "whatsapp": (
        "https://wa.me/?text="
        + encoded
    ),
    "facebook": (
        "https://www.facebook.com/sharer/sharer.php?"
        "u="
        + urllib.parse.quote(app_url)
        + "&quote="
        + encoded
    ),
    "x": (
        "https://twitter.com/intent/tweet?"
        "text="
        + encoded
    ),
    "linkedin": (
        "https://www.linkedin.com/sharing/share-offsite/?"
        "url="
        + urllib.parse.quote(app_url)
    ),
    "instagram": (
        "https://www.instagram.com/"
    ),
}
```

def share_buttons(title, text, prefix):

```
if not text:
    return

urls = build_share_urls(
    title,
    text,
)

st.markdown(
    "### 📤 Share this information"
)

st.markdown(
    """
    <div class="notice">
    🔒 <strong>Sharing:</strong>
    these buttons open the selected service through the
    user's browser/app. NavaBharat AI does not need to
    save a database record just to create these share links.
    AI requests may still be processed by the configured
    AI provider.
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        '<div class="share-whatsapp">',
        unsafe_allow_html=True,
    )

    st.link_button(
        "🟢 WhatsApp",
        urls["whatsapp"],
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        '<div class="share-instagram">',
        unsafe_allow_html=True,
    )

    st.link_button(
        "📸 Instagram",
        urls["instagram"],
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        '<div class="share-facebook">',
        unsafe_allow_html=True,
    )

    st.link_button(
        "🔵 Facebook",
        urls["facebook"],
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

c4, c5, c6 = st.columns(3)

with c4:
    st.markdown(
        '<div class="share-x">',
        unsafe_allow_html=True,
    )

    st.link_button(
        "⚫ X",
        urls["x"],
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

with c5:
    st.markdown(
        '<div class="share-linkedin">',
        unsafe_allow_html=True,
    )

    st.link_button(
        "🔷 LinkedIn",
        urls["linkedin"],
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

with c6:
    if st.button(
        "📋 Copy / Show",
        key=f"{prefix}_copy",
        use_container_width=True,
    ):
        st.code(text)
```

# ============================================================

# AI RESULT

# ============================================================

def display_answer(title, answer, prefix):

```
st.markdown(
    f"""
    <div class="glass-card">
        <h3>🤖 {html.escape(title)}</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# IMPORTANT:
# Never use:
#
# st.write(st.markdown(answer))
#
# That creates DeltaGenerator(...) output.
#
# Correct:
st.markdown(answer)

share_buttons(
    title,
    answer,
    prefix,
)
```

# ============================================================

# HOME

# ============================================================

HOME_CARDS = [
(
"🧠",
"Solve Anything",
"Ask questions and receive AI explanations.",
"gradient-pink",
"Solve Anything",
),
(
"🔬",
"AI Science Solver",
"Physics, Mathematics, Chemistry and Science.",
"gradient-blue",
"AI Science Solver",
),
(
"🎓",
"Student Hub",
"Notes, explanations, revision and study help.",
"gradient-purple",
"Student Hub",
),
(
"🌐",
"Live Information",
"Questions that require current information.",
"gradient-green",
"Live Information",
),
(
"💼",
"Job Notifications",
"Government, banking, railway and other jobs.",
"gradient-orange",
"Job Notifications",
),
(
"📝",
"Exam Notifications",
"NEET, JEE, EAPCET, CUET, SSC, UPSC and more.",
"gradient-teal",
"Exam Notifications",
),
(
"🎵",
"RacharlaGPT Music",
"Listen to songs published in the library.",
"gradient-red",
"RacharlaGPT Music",
),
(
"🎬",
"RacharlaGPT Video Studio",
"Video and audio tools.",
"gradient-indigo",
"RacharlaGPT Video Studio",
),
(
"✍️",
"Creator Studio",
"Scripts, captions and creative content.",
"gradient-pink",
"Creator Studio",
),
(
"🌍",
"Translator",
"Translate between multiple languages.",
"gradient-blue",
"Translator",
),
]

def page_home():

```
page_title(
    "🇮🇳 NavaBharat AI",
    "A free AI workspace powered by RacharlaGPT.",
)

st.markdown(
    """
    <div class="notice">
    🔒 <strong>Data notice:</strong>
    the application does not require a database for the
    browser-based sharing features. AI requests can be
    processed by the configured AI service.
    </div>
    """,
    unsafe_allow_html=True,
)

columns = st.columns(2)

for i, (
    icon,
    title,
    description,
    gradient,
    target,
) in enumerate(HOME_CARDS):

    with columns[i % 2]:

        st.markdown(
            f"""
            <div class="home-card {gradient}">
                <div style="font-size:43px;">{icon}</div>
                <h3>{html.escape(title)}</h3>
                <p>{html.escape(description)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            f"{icon} Open {title}",
            key=f"home_{i}",
            use_container_width=True,
        ):
            navigate(target)
```

# ============================================================

# SOLVE

# ============================================================

def page_solve():

```
page_title(
    "🧠 Solve Anything",
    "General AI question answering.",
)

question = st.text_area(
    "Your question",
    height=190,
    placeholder="Ask anything...",
)

if st.button(
    "🚀 Solve Question",
    use_container_width=True,
):

    if not question.strip():
        st.warning("Please enter a question.")
        return

    with st.spinner("Thinking..."):

        ok, answer = ask_ai(
            f"""
```

You are NavaBharat AI.

Answer this question accurately and clearly:

{question}

Use headings, bullets, examples and equations where useful.
Do not invent current information.
"""
)

```
    if ok:
        display_answer(
            "AI Answer",
            answer,
            "solve",
        )
    else:
        st.error(answer)
```

# ============================================================

# SCIENCE

# ============================================================

def page_science():

```
page_title(
    "🔬 AI Science Solver",
    "Physics • Mathematics • Chemistry • Biology • Science",
)

subject = st.selectbox(
    "Subject",
    [
        "Physics",
        "Mathematics",
        "Chemistry",
        "Biology",
        "General Science",
    ],
)

question = st.text_area(
    "Question / Problem",
    height=190,
    placeholder="Enter your problem...",
)

if st.button(
    f"🧪 Solve {subject}",
    use_container_width=True,
):

    if not question.strip():
        st.warning("Please enter a problem.")
        return

    with st.spinner("Solving..."):

        ok, answer = ask_ai(
            f"""
```

You are an expert {subject} teacher.

Solve:

{question}

Give:

* Concept
* Given information
* Formula
* Steps
* Calculations
* Final answer
* Short explanation

Be accurate and educational.
"""
)

```
    if ok:
        display_answer(
            f"{subject} Answer",
            answer,
            f"science_{subject.lower()}",
        )
    else:
        st.error(answer)
```

# ============================================================

# STUDENT HUB

# ============================================================

def page_student():

```
page_title(
    "🎓 Student Hub",
    "Study assistance and educational content.",
)

topic = st.text_input(
    "Topic",
    placeholder="Example: Newton's Laws",
)

task = st.selectbox(
    "Create",
    [
        "Simple Explanation",
        "Revision Notes",
        "Important Questions",
        "Quiz",
        "Study Plan",
    ],
)

if st.button(
    "🎓 Generate",
    use_container_width=True,
):

    if not topic.strip():
        st.warning("Enter a topic.")
        return

    ok, answer = ask_ai(
        f"""
```

Topic: {topic}

Student request:
{task}

Create useful, accurate educational material.
"""
)

```
    if ok:
        display_answer(
            f"Student Hub — {task}",
            answer,
            "student",
        )
    else:
        st.error(answer)
```

# ============================================================

# LIVE

# ============================================================

def page_live():

```
page_title(
    "🌐 Live Information",
    "Use this page for questions involving current information.",
)

question = st.text_area(
    "Current-information question",
    height=180,
    placeholder=(
        "Example: What is the latest official announcement "
        "about this topic?"
    ),
)

if st.button(
    "🌐 Get Information",
    use_container_width=True,
):

    if not question.strip():
        st.warning("Enter a question.")
        return

    ok, answer = ask_ai(
        f"""
```

The user wants potentially current information.

Question:
{question}

Do not fabricate current events, dates, jobs, exams,
announcements, prices or statistics.

If current verification is unavailable, clearly say so
and recommend checking the relevant official source.
"""
)

```
    if ok:
        display_answer(
            "Live Information",
            answer,
            "live",
        )
    else:
        st.error(answer)

st.markdown("### 🔗 Information sources")

links = [
    (
        "📰 General Search",
        "https://www.google.com/search?q=",
    ),
    (
        "🇮🇳 Government",
        "https://www.india.gov.in/",
    ),
]

for label, url in links:
    if url.endswith("="):
        st.link_button(
            label,
            "https://www.google.com/",
            use_container_width=True,
        )
    else:
        st.link_button(
            label,
            url,
            use_container_width=True,
        )
```

# ============================================================

# JOBS

# ============================================================

def page_jobs():

```
page_title(
    "💼 Job Notifications",
    "Job categories and job-related AI assistance.",
)

category = st.selectbox(
    "Category",
    [
        "Central Government",
        "State Government",
        "Telangana Government",
        "Andhra Pradesh Government",
        "Banking",
        "Railways",
        "SSC",
        "UPSC",
        "Defence",
        "Teaching",
        "Police",
        "Private Jobs",
        "IT Jobs",
    ],
)

question = st.text_area(
    "Job information",
    height=170,
    placeholder=(
        "Example: What qualifications are needed "
        "for this category?"
    ),
)

if st.button(
    "💼 Generate Job Information",
    use_container_width=True,
):

    if not question.strip():
        st.warning("Enter a question.")
        return

    ok, answer = ask_ai(
        f"""
```

Job category:
{category}

Question:
{question}

Clearly separate general career information from current
vacancy information. Never invent an open vacancy.
"""
)

```
    if ok:
        display_answer(
            f"Job Information — {category}",
            answer,
            "jobs",
        )
    else:
        st.error(answer)

st.markdown("### 🔗 Official job sources")

official_jobs = [
    (
        "🇮🇳 UPSC",
        "https://upsc.gov.in/",
    ),
    (
        "🧾 SSC",
        "https://ssc.gov.in/",
    ),
    (
        "🚆 Railway Recruitment",
        "https://www.rrbapply.gov.in/",
    ),
    (
        "🏦 IBPS",
        "https://www.ibps.in/",
    ),
]

for label, url in official_jobs:
    st.link_button(
        label,
        url,
        use_container_width=True,
    )
```

# ============================================================

# EXAMS

# ============================================================

def page_exams():

```
page_title(
    "📝 Exam Notifications",
    "Exam information and preparation assistance.",
)

exam = st.selectbox(
    "Exam",
    [
        "NEET",
        "JEE Main",
        "JEE Advanced",
        "TS EAPCET",
        "AP EAPCET",
        "CUET",
        "SSC",
        "UPSC",
        "GATE",
        "CAT",
        "State Exams",
        "University Exams",
    ],
)

question = st.text_area(
    "Exam information",
    height=170,
    placeholder="Ask about preparation or exam information...",
)

if st.button(
    "📝 Generate Exam Information",
    use_container_width=True,
):

    if not question.strip():
        st.warning("Enter a question.")
        return

    ok, answer = ask_ai(
        f"""
```

Exam:
{exam}

Question:
{question}

Do not invent current examination dates or notifications.
For current dates, advise verification with the official
examination authority.
"""
)

```
    if ok:
        display_answer(
            f"Exam Information — {exam}",
            answer,
            "exams",
        )
    else:
        st.error(answer)

st.markdown("### 🔗 Official examination sources")

exam_links = [
    (
        "🎯 NTA",
        "https://www.nta.ac.in/",
    ),
    (
        "🏛️ UPSC",
        "https://upsc.gov.in/",
    ),
    (
        "📚 SSC",
        "https://ssc.gov.in/",
    ),
]

for label, url in exam_links:
    st.link_button(
        label,
        url,
        use_container_width=True,
    )
```

# ============================================================

# MUSIC LIBRARY

# ============================================================

AUDIO_EXTENSIONS = {
".mp3",
".wav",
".m4a",
".aac",
".ogg",
".flac",
".opus",
}

def get_songs():
songs = []

```
if not MUSIC_DIR.exists():
    return songs

for path in MUSIC_DIR.iterdir():

    if (
        path.is_file()
        and path.suffix.lower()
        in AUDIO_EXTENSIONS
    ):
        songs.append(path)

return sorted(
    songs,
    key=lambda x: x.name.lower(),
)
```

def valid_library_file(path):
try:
return (
path.resolve().parent
== MUSIC_DIR.resolve()
and path.is_file()
)
except Exception:
return False

def delete_song(path):

```
if not valid_library_file(path):
    return False, "Invalid library file."

try:
    path.unlink()
    return True, f"Deleted {path.name}"
except Exception as exc:
    return False, str(exc)
```

def admin_login():

```
if st.session_state.admin_authenticated:
    return True

if not ADMIN_PASSWORD:
    st.info(
        "Admin controls are disabled because "
        "ADMIN_PASSWORD is not configured in Streamlit Secrets."
    )
    return False

password = st.text_input(
    "Admin password",
    type="password",
    key="admin_password",
)

if st.button(
    "🔐 Admin Login",
    use_container_width=True,
):

    if password == ADMIN_PASSWORD:
        st.session_state.admin_authenticated = True
        st.success("Admin access enabled.")
        st.rerun()
    else:
        st.error("Incorrect admin password.")

return False
```

def page_music():

```
page_title(
    "🎵 RacharlaGPT Music",
    "Public listening library.",
)

st.markdown(
    """
    <div class="notice">
    🎧 Users can listen to published songs.
    Upload and delete controls are available only to the
    authenticated administrator.
    </div>
    """,
    unsafe_allow_html=True,
)

songs = get_songs()

if not songs:

    st.info(
        "No songs have been published yet."
    )

else:

    for song in songs:

        st.markdown(
            f"""
            <div class="music-card">
                <h3>🎵 {html.escape(song.stem)}</h3>
                <p>RacharlaGPT Library</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:

            with open(
                song,
                "rb",
            ) as audio:

                st.audio(
                    audio.read(),
                    format=song.suffix.lower(),
                )

        except Exception as exc:
            st.error(
                f"Unable to play {song.name}: {exc}"
            )

st.divider()

st.markdown("### 🔐 Administrator")

if not admin_login():
    return

uploaded = st.file_uploader(
    "Publish song",
    type=[
        "mp3",
        "wav",
        "m4a",
        "aac",
        "ogg",
        "flac",
        "opus",
    ],
    key="music_upload",
)

if uploaded is not None:

    if st.button(
        "🎵 Publish Song",
        use_container_width=True,
    ):

        filename = Path(
            uploaded.name
        ).name

        filename = re.sub(
            r"[^A-Za-z0-9._ -]",
            "_",
            filename,
        )

        destination = (
            MUSIC_DIR / filename
        )

        try:

            with open(
                destination,
                "wb",
            ) as output:

                output.write(
                    uploaded.getbuffer()
                )

            st.success(
                f"Published: {filename}"
            )

            st.rerun()

        except Exception as exc:
            st.error(
                f"Could not publish song: {exc}"
            )

st.markdown(
    "### 🗑️ Delete songs"
)

songs = get_songs()

if not songs:
    st.info("No songs available.")
    return

for index, song in enumerate(songs):

    col1, col2 = st.columns(
        [5, 1]
    )

    with col1:
        st.write(
            f"🎵 **{song.name}**"
        )

    with col2:

        if st.button(
            "🗑️ Delete",
            key=f"delete_{index}_{song.name}",
            use_container_width=True,
        ):

            ok, message = delete_song(song)

            if ok:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
```

# ============================================================

# VIDEO STUDIO

# ============================================================

def ffmpeg_available():
return shutil.which("ffmpeg") is not None

def extract_audio(video_path, output_path):

```
if not ffmpeg_available():
    return (
        False,
        "FFmpeg is unavailable on this server.",
    )

command = [
    "ffmpeg",
    "-y",
    "-i",
    str(video_path),
    "-vn",
    "-codec:a",
    "libmp3lame",
    "-q:a",
    "2",
    str(output_path),
]

try:

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=180,
    )

    if result.returncode != 0:
        return (
            False,
            result.stderr[-2000:],
        )

    return True, "Audio extracted successfully."

except subprocess.TimeoutExpired:
    return (
        False,
        "FFmpeg timed out.",
    )

except Exception as exc:
    return False, str(exc)
```

def page_video():

```
page_title(
    "🎬 RacharlaGPT Video Studio",
    "Video and audio utilities.",
)

st.markdown(
    """
    <div class="glass-card">
    <h3>🎧 Video to Audio</h3>
    <p>
    Upload content that you own or have permission to process.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded = st.file_uploader(
    "Video file",
    type=[
        "mp4",
        "mov",
        "mkv",
        "webm",
        "avi",
    ],
)

if uploaded is None:
    return

if not ffmpeg_available():

    st.warning(
        "FFmpeg is not installed on this server. "
        "Video-to-audio extraction cannot currently run."
    )

    return

if st.button(
    "🎧 Extract Audio",
    use_container_width=True,
):

    suffix = Path(
        uploaded.name
    ).suffix

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
        dir=UPLOAD_DIR,
    ) as temp:

        temp.write(
            uploaded.getbuffer()
        )

        temp_path = Path(
            temp.name
        )

    output_path = (
        OUTPUT_DIR
        / (
            Path(uploaded.name).stem
            + "_audio.mp3"
        )
    )

    ok, message = extract_audio(
        temp_path,
        output_path,
    )

    try:
        temp_path.unlink(
            missing_ok=True
        )
    except Exception:
        pass

    if ok:

        st.success(message)

        audio_data = (
            output_path.read_bytes()
        )

        st.audio(
            audio_data,
            format="audio/mp3",
        )

        st.download_button(
            "⬇️ Download Audio",
            data=audio_data,
            file_name=output_path.name,
            mime="audio/mpeg",
            use_container_width=True,
        )

    else:
        st.error(message)
```

# ============================================================

# CREATOR STUDIO

# ============================================================

def page_creator():

```
page_title(
    "✍️ Creator Studio",
    "Create scripts, captions and content.",
)

content_type = st.selectbox(
    "Content type",
    [
        "YouTube Script",
        "Short Video Script",
        "Instagram Caption",
        "Facebook Post",
        "LinkedIn Post",
        "Blog Outline",
        "Creative Idea",
    ],
)

topic = st.text_area(
    "Topic",
    height=170,
    placeholder="Enter your topic...",
)

if st.button(
    "✍️ Create",
    use_container_width=True,
):

    if not topic.strip():
        st.warning("Enter a topic.")
        return

    ok, answer = ask_ai(
        f"""
```

Create a {content_type}.

Topic:
{topic}

Make it original and useful.
"""
)

```
    if ok:
        display_answer(
            f"Creator Studio — {content_type}",
            answer,
            "creator",
        )
    else:
        st.error(answer)
```

# ============================================================

# TRANSLATOR

# ============================================================

def page_translator():

```
page_title(
    "🌍 Translator",
    "Translate text between languages.",
)

languages = [
    "English",
    "Telugu",
    "Hindi",
    "Tamil",
    "Kannada",
    "Malayalam",
    "Marathi",
    "Bengali",
    "Gujarati",
    "Punjabi",
    "Urdu",
    "Odia",
    "French",
    "German",
    "Spanish",
    "Arabic",
    "Chinese",
    "Japanese",
]

source = st.selectbox(
    "From",
    languages,
)

target = st.selectbox(
    "To",
    languages,
    index=1,
)

source_text = st.text_area(
    "Text",
    height=200,
    placeholder="Paste or type text here...",
)

if st.button(
    "🌍 Translate",
    use_container_width=True,
):

    if not source_text.strip():
        st.warning("Enter text.")
        return

    ok, answer = ask_ai(
        f"""
```

Translate this text from {source} to {target}.

Preserve the meaning.

TEXT:
{source_text}
"""
)

```
    if ok:

        st.markdown(
            "### ✅ Translated Text"
        )

        # Explicit white background and dark text.
        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                color:#111827;
                padding:22px;
                border-radius:18px;
                border:1px solid #dbe3ef;
                white-space:pre-wrap;
                line-height:1.7;
                font-size:17px;
            ">
            {html.escape(answer)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        share_buttons(
            "NavaBharat AI Translation",
            answer,
            "translation",
        )

    else:
        st.error(answer)
```

# ============================================================

# ABOUT

# ============================================================

def page_about():

```
page_title(
    "ℹ️ About NavaBharat AI",
    "Application information.",
)

# CREATOR IS DEFINED AT THE TOP OF THIS FILE.
# This fixes the original:
#
# NameError: name 'CREATOR' is not defined

st.markdown(
    f"""
    <div class="glass-card">

    <h2>🇮🇳 {html.escape(APP_NAME)}</h2>

    <p>
    <strong>Version:</strong>
    {html.escape(APP_VERSION)}
    </p>

    <p>
    <strong>Creator & Developer:</strong>
    {html.escape(CREATOR)}
    </p>

    <p>
    <strong>Brand:</strong>
    {html.escape(BRAND)}
    </p>

    <p>
    <strong>Powered by:</strong>
    {html.escape(TAGLINE)}
    </p>

    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="notice">

    🔒 <strong>Data & sharing</strong>

    <br><br>

    The application does not require an application database
    for its browser-based sharing buttons.

    <br><br>

    Sharing opens the selected service in the user's browser
    or app. The application does not need to permanently save
    the generated answer simply to create a share link.

    <br><br>

    AI requests may be processed by the configured AI provider.
    Users should avoid submitting sensitive personal information.

    </div>
    """,
    unsafe_allow_html=True,
)

st.link_button(
    "▶️ RacharlaGPT YouTube",
    "https://www.youtube.com/@racharlgpt",
    use_container_width=True,
)
```

# ============================================================

# NAVIGATION

# ============================================================

NAV_ITEMS = [
("🏠", "Home"),
("🧠", "Solve Anything"),
("🔬", "AI Science Solver"),
("🎓", "Student Hub"),
("🌐", "Live Information"),
("💼", "Job Notifications"),
("📝", "Exam Notifications"),
("🎵", "RacharlaGPT Music"),
("🎬", "RacharlaGPT Video Studio"),
("✍️", "Creator Studio"),
("🌍", "Translator"),
("ℹ️", "About"),
]

NAVIGATION = {
"Home": page_home,
"Solve Anything": page_solve,
"AI Science Solver": page_science,
"Student Hub": page_student,
"Live Information": page_live,
"Job Notifications": page_jobs,
"Exam Notifications": page_exams,
"RacharlaGPT Music": page_music,
"RacharlaGPT Video Studio": page_video,
"Creator Studio": page_creator,
"Translator": page_translator,
"About": page_about,
}

# ============================================================

# SIDEBAR

# ============================================================

with st.sidebar:

```
st.markdown(
    """
    <div style="
        text-align:center;
        padding:10px 5px 18px;
    ">

        <div style="
            font-size:43px;
        ">🇮🇳</div>

        <div style="
            font-size:21px;
            font-weight:950;
            margin-top:7px;
        ">
            NavaBharat AI
        </div>

        <div style="
            font-size:10px;
            font-weight:900;
            letter-spacing:.08em;
            color:#64748b;
            margin-top:5px;
        ">
            POWERED BY RACHARLAGPT
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

for icon, label in NAV_ITEMS:

    if st.button(
        f"{icon}  {label}",
        key=f"nav_{label}",
        use_container_width=True,
    ):
        navigate(label)

st.divider()

if st.session_state.admin_authenticated:

    if st.button(
        "🔒 Lock Admin",
        key="lock_admin",
        use_container_width=True,
    ):

        st.session_state.admin_authenticated = False
        st.rerun()
```

# ============================================================

# SAFE PAGE DISPATCH

# ============================================================

# This prevents:

#

# NAVIGATION[st.session_state.nav_page]()

#

# from crashing if an invalid/stale page exists.

if st.session_state.nav_page not in NAVIGATION:
st.session_state.nav_page = "Home"

page_function = NAVIGATION.get(
st.session_state.nav_page,
page_home,
)

page_function()

# ============================================================

# FOOTER

# ============================================================

st.markdown(
f""" <div style="
     text-align:center;
     padding:35px 10px 20px;
     color:#64748b;
     font-size:13px;
 ">

```
    <strong>{html.escape(APP_NAME)}</strong>
    · v{html.escape(APP_VERSION)}
    · {html.escape(TAGLINE)}

    <br>

    Created & Developed by
    <strong>{html.escape(CREATOR)}</strong>

</div>
""",
unsafe_allow_html=True,
```

)

```

**Important:** this is a clean replacement, so it will not contain the `SyntaxError` from my previous answer. But if your goal is specifically **“keep every existing feature of my original 6.0.0 and only repair it”**, I need the actual existing `app.py`; otherwise there is no way to reconstruct code that isn't present in the conversation.
```
