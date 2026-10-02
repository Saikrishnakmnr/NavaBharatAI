```python
"""
NavaBharat AI v6.0.0
POWERED BY RACHARLAGPT

Creator & Developer:
Racharla Saikrishna

Features:
- Solve Anything
- Science Solver
- Student Hub
- Live Information
- Job Information
- Exam Information
- RacharlaGPT Music
- RacharlaGPT Video Studio
- Creator Studio
- Translator
- About
- Admin music upload/delete
- Social sharing buttons
- Responsive radiant/glass UI

No application database is required.
"""

from __future__ import annotations

import base64
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.parse
from pathlib import Path
from typing import Optional

import streamlit as st


# ============================================================
# APP CONSTANTS
# ============================================================

APP_NAME = "NavaBharat AI"
BRAND = "RacharlaGPT"
CREATOR = "Racharla Saikrishna"
APP_VERSION = "6.0.0"
TAGLINE = "POWERED BY RACHARLAGPT"

# FIX FOR:
# NameError: name 'CREATOR' is not defined
#
# These constants are intentionally defined BEFORE page_about()
# and before the navigation is executed.


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
# DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MUSIC_DIR = BASE_DIR / "racharlagptlibrary"
MUSIC_DIR.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# SECRETS / API
# ============================================================

GEMINI_API_KEY = ""

try:
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    pass

if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        pass

GEMINI_MODEL = "gemini-3.8-flash"

try:
    GEMINI_MODEL = st.secrets.get(
        "GEMINI_MODEL",
        "gemini-3.8-flash",
    )
except Exception:
    pass


# Optional admin password.
# Put this in Streamlit secrets if you want protected admin mode:
#
# ADMIN_PASSWORD = "your-password"
#
# If it is not configured, admin controls remain unavailable.

ADMIN_PASSWORD = ""

try:
    ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "")
except Exception:
    pass


# ============================================================
# SESSION STATE
# ============================================================

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Home"

if "navigation_open" not in st.session_state:
    st.session_state.navigation_open = True

if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "last_share_title" not in st.session_state:
    st.session_state.last_share_title = "NavaBharat AI"

if "last_share_text" not in st.session_state:
    st.session_state.last_share_text = ""


# ============================================================
# PREMIUM CSS
# ============================================================

st.markdown(
    """
<style>

:root {
    --text-main: #101828;
    --text-white: #ffffff;
    --glass: rgba(255,255,255,0.82);
    --glass-border: rgba(255,255,255,0.60);
}

/* ---------------------------------------------------------
   MAIN BACKGROUND
--------------------------------------------------------- */

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255,0,128,.16), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(0,170,255,.18), transparent 28%),
        radial-gradient(circle at 20% 90%, rgba(0,255,180,.14), transparent 30%),
        linear-gradient(135deg, #f7f9ff 0%, #eef4ff 45%, #f9f2ff 100%);
}

/* ---------------------------------------------------------
   HIDE STREAMLIT DEFAULT UI
--------------------------------------------------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* ---------------------------------------------------------
   GLOBAL TEXT
--------------------------------------------------------- */

html,
body,
.stApp,
p,
label,
span,
div {
    color: var(--text-main);
}

h1,
h2,
h3,
h4 {
    color: #111827 !important;
}

/* ---------------------------------------------------------
   MAIN TITLE
--------------------------------------------------------- */

.main-page-title {
    width: 100%;
    max-width: 100%;
    overflow: visible !important;
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
    font-size: clamp(1.8rem, 4vw, 3.6rem);
    line-height: 1.12;
    font-weight: 900;
    margin: 8px 0 10px 0;
    background: linear-gradient(
        90deg,
        #ff006e,
        #8338ec,
        #3a86ff,
        #00b894,
        #ff9f1c
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ---------------------------------------------------------
   BRAND
--------------------------------------------------------- */

.brand-strip {
    display: inline-block;
    padding: 7px 15px;
    border-radius: 999px;
    background:
        linear-gradient(
            120deg,
            #ff006e,
            #8338ec,
            #3a86ff,
            #00b894
        );
    color: white !important;
    font-weight: 900;
    font-size: .78rem;
    letter-spacing: .08em;
    box-shadow: 0 10px 25px rgba(71, 65, 255, .22);
}

/* ---------------------------------------------------------
   GLASS CARD
--------------------------------------------------------- */

.glass-card {
    padding: 22px;
    border-radius: 24px;
    background: var(--glass);
    border: 1px solid var(--glass-border);
    box-shadow:
        0 18px 50px rgba(31, 38, 135, .12),
        inset 0 1px 0 rgba(255,255,255,.85);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    margin-bottom: 18px;
}

/* ---------------------------------------------------------
   HOME CARDS
--------------------------------------------------------- */

.home-card {
    min-height: 190px;
    padding: 22px;
    border-radius: 26px;
    color: white !important;
    margin-bottom: 18px;
    box-shadow:
        0 18px 35px rgba(30, 30, 60, .18),
        inset 0 1px 0 rgba(255,255,255,.45);
    transition:
        transform .22s ease,
        box-shadow .22s ease;
}

.home-card:hover {
    transform: translateY(-7px) scale(1.015);
    box-shadow:
        0 25px 55px rgba(30, 30, 60, .27),
        inset 0 1px 0 rgba(255,255,255,.6);
}

.home-card h3,
.home-card p,
.home-card div,
.home-card span {
    color: white !important;
}

.card-pink {
    background: linear-gradient(135deg, #ff006e, #ff4d6d, #ff9f1c);
}

.card-blue {
    background: linear-gradient(135deg, #4361ee, #3a86ff, #00b4d8);
}

.card-green {
    background: linear-gradient(135deg, #00b894, #00cec9, #55efc4);
}

.card-purple {
    background: linear-gradient(135deg, #7209b7, #8338ec, #c77dff);
}

.card-orange {
    background: linear-gradient(135deg, #fb5607, #ff9f1c, #ffd166);
}

.card-teal {
    background: linear-gradient(135deg, #0077b6, #00b4d8, #90e0ef);
}

.card-red {
    background: linear-gradient(135deg, #d00000, #e85d04, #ff006e);
}

.card-indigo {
    background: linear-gradient(135deg, #3f37c9, #4895ef, #4361ee);
}

/* ---------------------------------------------------------
   SIDEBAR
--------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            160deg,
            rgba(255,255,255,.96),
            rgba(240,244,255,.96)
        );
    border-right: 1px solid rgba(100,100,150,.12);
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 48px;
    border: 0;
    border-radius: 15px;
    margin: 4px 0;
    color: white !important;
    font-weight: 850 !important;
    font-size: 14px !important;
    text-shadow: 0 1px 2px rgba(0,0,0,.25);
    box-shadow: 0 7px 18px rgba(40,40,80,.14);
    transition: all .2s ease;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateX(5px) scale(1.02);
    filter: brightness(1.07);
}

/* Different sidebar colors */

section[data-testid="stSidebar"] .stButton:nth-of-type(1) button {
    background: linear-gradient(135deg,#ff006e,#ff4d6d);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(2) button {
    background: linear-gradient(135deg,#4361ee,#3a86ff);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(3) button {
    background: linear-gradient(135deg,#7209b7,#8338ec);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(4) button {
    background: linear-gradient(135deg,#008f7a,#00b894);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(5) button {
    background: linear-gradient(135deg,#fb5607,#ff9f1c);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(6) button {
    background: linear-gradient(135deg,#0077b6,#00b4d8);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(7) button {
    background: linear-gradient(135deg,#d00000,#e85d04);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(8) button {
    background: linear-gradient(135deg,#8338ec,#c77dff);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(9) button {
    background: linear-gradient(135deg,#06d6a0,#118ab2);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(10) button {
    background: linear-gradient(135deg,#ef476f,#ff006e);
}

section[data-testid="stSidebar"] .stButton:nth-of-type(11) button {
    background: linear-gradient(135deg,#118ab2,#073b4c);
}

/* ---------------------------------------------------------
   NORMAL BUTTONS
--------------------------------------------------------- */

.stButton > button,
.stDownloadButton > button {
    border: 0 !important;
    border-radius: 14px !important;
    min-height: 44px !important;
    color: white !important;
    font-weight: 850 !important;
    text-shadow: 0 1px 2px rgba(0,0,0,.28);
    transition: all .2s ease !important;
    box-shadow: 0 8px 18px rgba(40,40,80,.15) !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px) scale(1.015);
    filter: brightness(1.08);
}

/* ---------------------------------------------------------
   SHARE BUTTONS
--------------------------------------------------------- */

.share-wa button {
    background: linear-gradient(135deg,#00b894,#00cec9) !important;
}

.share-instagram button {
    background: linear-gradient(
        135deg,
        #8338ec,
        #e1306c,
        #ff9f1c
    ) !important;
}

.share-facebook button {
    background: linear-gradient(135deg,#1877f2,#4267b2) !important;
}

.share-x button {
    background: linear-gradient(135deg,#111827,#374151) !important;
}

.share-linkedin button {
    background: linear-gradient(135deg,#0077b5,#00a0dc) !important;
}

.share-copy button {
    background: linear-gradient(135deg,#ff006e,#8338ec) !important;
}

/* ---------------------------------------------------------
   INPUTS
--------------------------------------------------------- */

textarea,
input,
.stTextInput input,
.stTextArea textarea {
    background: white !important;
    color: #111827 !important;
    border-radius: 14px !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

/* ---------------------------------------------------------
   MUSIC
--------------------------------------------------------- */

.music-card {
    padding: 20px;
    border-radius: 22px;
    background:
        linear-gradient(
            135deg,
            rgba(255,0,110,.12),
            rgba(131,56,236,.12),
            rgba(58,134,255,.12)
        );
    border: 1px solid rgba(100,80,200,.16);
    margin-bottom: 15px;
}

/* ---------------------------------------------------------
   NOTICE
--------------------------------------------------------- */

.security-notice {
    padding: 16px 18px;
    border-radius: 18px;
    background:
        linear-gradient(
            135deg,
            rgba(0,184,148,.12),
            rgba(58,134,255,.10)
        );
    border: 1px solid rgba(0,184,148,.25);
    margin: 15px 0;
}

/* ---------------------------------------------------------
   MOBILE
--------------------------------------------------------- */

@media (max-width: 768px) {

    .main-page-title {
        font-size: 2rem !important;
    }

    .home-card {
        min-height: 155px;
        padding: 18px;
    }

    .glass-card {
        padding: 16px;
        border-radius: 19px;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def safe_text(value: str) -> str:
    """Convert arbitrary content to safe display text."""
    return str(value or "").strip()


def show_page_title(title: str, subtitle: str = "") -> None:
    st.markdown(
        f'<div class="main-page-title">{html.escape(title)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<span class="brand-strip">{html.escape(TAGLINE)}</span>',
        unsafe_allow_html=True,
    )

    if subtitle:
        st.markdown(
            f'<div style="margin-top:12px;color:#475569;">'
            f'{html.escape(subtitle)}'
            f'</div>',
            unsafe_allow_html=True,
        )


def go_page(page: str) -> None:
    """
    Navigate to a page and automatically close navigation.

    This fixes the requested behavior:
    user clicks a sidebar item -> page opens -> navigation closes.
    """
    st.session_state.nav_page = page
    st.session_state.navigation_open = False
    st.rerun()


def go_home() -> None:
    st.session_state.nav_page = "Home"
    st.session_state.navigation_open = True
    st.rerun()


# ============================================================
# SHARING
# ============================================================

def make_share_text(title: str, text: str) -> str:
    return f"{title}\n\n{text}\n\nPowered by NavaBharat AI — {TAGLINE}"


def share_urls(title: str, text: str) -> dict[str, str]:
    """
    Browser-based sharing.

    No application database is used.
    """

    message = make_share_text(title, text)
    encoded = urllib.parse.quote(message)
    encoded_title = urllib.parse.quote(title)

    return {
        "whatsapp": f"https://wa.me/?text={encoded}",
        "facebook": (
            "https://www.facebook.com/sharer/sharer.php?"
            f"u={urllib.parse.quote('https://navabharatai.racharlagpt.in')}"
            f"&quote={encoded}"
        ),
        "x": (
            "https://twitter.com/intent/tweet?"
            f"text={encoded}"
        ),
        "linkedin": (
            "https://www.linkedin.com/sharing/share-offsite/?"
            f"url={urllib.parse.quote('https://navabharatai.racharlagpt.in')}"
        ),
        "instagram": (
            "https://www.instagram.com/"
            f"?text={encoded}"
        ),
        "copy": message,
        "title": encoded_title,
    }


def render_share_buttons(
    title: str,
    text: str,
    key_prefix: str,
) -> None:

    text = safe_text(text)

    if not text:
        return

    urls = share_urls(title, text)

    st.markdown("### 📤 Share this information")

    st.markdown(
        """
        <div class="security-notice">
        🔒 <strong>Your app does not need a database for these share buttons.</strong>
        Sharing opens the selected service in the user's browser/app.
        The app does not need to store the generated answer just to share it.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="share-wa">', unsafe_allow_html=True)
        st.link_button(
            "🟢 WhatsApp",
            urls["whatsapp"],
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="share-instagram">', unsafe_allow_html=True)
        st.link_button(
            "📸 Instagram",
            urls["instagram"],
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="share-facebook">', unsafe_allow_html=True)
        st.link_button(
            "🔵 Facebook",
            urls["facebook"],
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown('<div class="share-x">', unsafe_allow_html=True)
        st.link_button(
            "⚫ X",
            urls["x"],
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c5:
        st.markdown('<div class="share-linkedin">', unsafe_allow_html=True)
        st.link_button(
            "🔷 LinkedIn",
            urls["linkedin"],
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with c6:
        st.markdown('<div class="share-copy">', unsafe_allow_html=True)

        if st.button(
            "📋 Copy / Show Text",
            key=f"{key_prefix}_copy",
            use_container_width=True,
        ):
            st.code(text)

        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# GEMINI
# ============================================================

def get_gemini_client():
    """
    Supports the modern google-genai package.

    Install:
        pip install google-genai
    """

    if not GEMINI_API_KEY:
        return None

    try:
        from google import genai

        return genai.Client(api_key=GEMINI_API_KEY)

    except Exception:
        return None


def friendly_gemini_error(exc: Exception) -> str:

    message = str(exc)

    upper = message.upper()

    if "503" in upper or "UNAVAILABLE" in upper:
        return (
            "Gemini is temporarily busy or unavailable. "
            "Your API key was detected, but the selected model "
            "is currently not accepting this request. "
            "Please try again shortly."
        )

    if "429" in upper or "RESOURCE_EXHAUSTED" in upper:
        return (
            "Gemini usage is temporarily limited. "
            "Please wait and try again."
        )

    if "401" in upper or "UNAUTHENTICATED" in upper:
        return (
            "Gemini rejected the API credentials. "
            "Check GEMINI_API_KEY in Streamlit Secrets."
        )

    if "403" in upper or "PERMISSION_DENIED" in upper:
        return (
            "Gemini permission was denied. "
            "Check whether this model/API is enabled for your project."
        )

    if "404" in upper or "NOT_FOUND" in upper:
        return (
            f"The configured Gemini model '{GEMINI_MODEL}' "
            "was not found or is unavailable for this API account."
        )

    return f"Gemini request failed: {message}"


def ask_gemini(prompt: str) -> tuple[bool, str]:

    if not GEMINI_API_KEY:
        return (
            False,
            "Gemini API key is not configured. "
            "Add GEMINI_API_KEY to Streamlit Secrets.",
        )

    client = get_gemini_client()

    if client is None:
        return (
            False,
            "The Gemini Python package is not installed. "
            "Add google-genai to requirements.txt.",
        )

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        answer = getattr(response, "text", None)

        if not answer:
            return False, "Gemini returned an empty response."

        return True, str(answer)

    except Exception as exc:
        return False, friendly_gemini_error(exc)


def render_ai_result(
    title: str,
    answer: str,
    share_key: str,
) -> None:

    st.markdown(
        f"""
        <div class="glass-card">
            <h3>🤖 {html.escape(title)}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # IMPORTANT:
    # Do NOT do:
    #
    # st.write(st.markdown(answer))
    #
    # That produces DeltaGenerator(...) output.
    #
    # Correct:
    st.markdown(answer)

    render_share_buttons(
        title,
        answer,
        share_key,
    )


# ============================================================
# ADMIN AUTHENTICATION
# ============================================================

def render_admin_login() -> bool:

    if st.session_state.admin_authenticated:
        return True

    st.markdown(
        """
        <div class="glass-card">
        <h3>🔐 Admin Access</h3>
        <p>
        Admin access is optional and is controlled through
        <strong>ADMIN_PASSWORD</strong> in Streamlit Secrets.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not ADMIN_PASSWORD:
        st.warning(
            "ADMIN_PASSWORD is not configured. "
            "Add it to Streamlit Secrets to enable admin controls."
        )
        return False

    password = st.text_input(
        "Admin password",
        type="password",
        key="admin_password",
    )

    if st.button(
        "🔓 Unlock Admin",
        key="unlock_admin",
        use_container_width=True,
    ):
        if password == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.success("Admin access enabled.")
            st.rerun()
        else:
            st.error("Incorrect admin password.")

    return False


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


def library_songs() -> list[Path]:

    songs = []

    for path in MUSIC_DIR.iterdir():

        if not path.is_file():
            continue

        if path.suffix.lower() in AUDIO_EXTENSIONS:
            songs.append(path)

    return sorted(
        songs,
        key=lambda p: p.name.lower(),
    )


def safe_library_path(path: Path) -> bool:

    try:
        resolved = path.resolve()
        library_root = MUSIC_DIR.resolve()

        return (
            resolved.parent == library_root
            and resolved.is_file()
        )

    except Exception:
        return False


def delete_library_song(path: Path) -> tuple[bool, str]:

    if not safe_library_path(path):
        return False, "Invalid library file."

    try:
        path.unlink()
        return True, f"Deleted {path.name}"

    except Exception as exc:
        return False, f"Could not delete song: {exc}"


def render_public_music_library():

    songs = library_songs()

    if not songs:
        st.info(
            "No songs have been published to the "
            "RacharlaGPT Library yet."
        )
        return

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
            with open(song, "rb") as audio_file:
                st.audio(
                    audio_file.read(),
                    format=song.suffix.lower(),
                )
        except Exception as exc:
            st.error(
                f"Unable to play {song.name}: {exc}"
            )


def render_admin_music_library():

    st.markdown("### 🛠️ Admin Music Management")

    songs = library_songs()

    if not songs:
        st.info("Library is empty.")
        return

    for index, song in enumerate(songs):

        col1, col2 = st.columns(
            [4, 1],
            vertical_alignment="center",
        )

        with col1:
            st.write(f"🎵 **{song.name}**")

        with col2:

            if st.button(
                "🗑️ Delete",
                key=f"delete_song_{index}_{song.name}",
                use_container_width=True,
            ):

                ok, message = delete_library_song(song)

                if ok:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)


# ============================================================
# VIDEO / AUDIO
# ============================================================

def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def extract_audio_from_video(
    video_path: Path,
    output_path: Path,
) -> tuple[bool, str]:

    if not ffmpeg_available():
        return (
            False,
            "FFmpeg is not installed on this server. "
            "Video-to-audio extraction is unavailable.",
        )

    try:

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-vn",
            "-acodec",
            "mp3",
            str(output_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
        )

        if result.returncode != 0:
            return (
                False,
                result.stderr[-1500:],
            )

        return True, str(output_path)

    except subprocess.TimeoutExpired:
        return (
            False,
            "FFmpeg timed out while processing the video.",
        )

    except Exception as exc:
        return False, str(exc)


# ============================================================
# HOME
# ============================================================

HOME_CARDS = [
    (
        "🧠",
        "Solve Anything",
        "Ask questions and get AI-powered explanations.",
        "card-pink",
        "Solve Anything",
    ),
    (
        "🔬",
        "AI Science Solver",
        "Physics, Mathematics, Chemistry and Science.",
        "card-blue",
        "AI Science Solver",
    ),
    (
        "🎓",
        "Student Hub",
        "Study help, notes, concepts and preparation.",
        "card-purple",
        "Student Hub",
    ),
    (
        "🌐",
        "Live Information",
        "Ask for current information and research topics.",
        "card-green",
        "Live Information",
    ),
    (
        "💼",
        "Job Notifications",
        "Explore government, banking, railway and other jobs.",
        "card-orange",
        "Job Notifications",
    ),
    (
        "📝",
        "Exam Notifications",
        "Exam categories, preparation and official links.",
        "card-teal",
        "Exam Notifications",
    ),
    (
        "🎵",
        "RacharlaGPT Music",
        "Listen to songs published in the public library.",
        "card-red",
        "RacharlaGPT Music",
    ),
    (
        "🎬",
        "Video Studio",
        "Create simple image/text/video projects.",
        "card-indigo",
        "RacharlaGPT Video Studio",
    ),
    (
        "✍️",
        "Creator Studio",
        "Create scripts, captions and content.",
        "card-pink",
        "Creator Studio",
    ),
    (
        "🌍",
        "Translator",
        "Translate text between languages.",
        "card-blue",
        "Translator",
    ),
]


def page_home():

    show_page_title(
        "🇮🇳 NavaBharat AI",
        "A multilingual AI workspace powered by RacharlaGPT.",
    )

    st.markdown(
        """
        <div class="security-notice">
        🔒 <strong>Privacy note:</strong>
        NavaBharat AI does not require an application database
        for these features. Sharing uses the user's browser/app.
        AI requests may still be processed by the configured AI
        provider when you use AI features.
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(2)

    for index, (
        icon,
        title,
        description,
        css_class,
        target,
    ) in enumerate(HOME_CARDS):

        with cols[index % 2]:

            st.markdown(
                f"""
                <div class="home-card {css_class}">
                    <div style="font-size:42px">{icon}</div>
                    <h3>{html.escape(title)}</h3>
                    <p>{html.escape(description)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Different gradient button classes are supplied by
            # Streamlit's CSS/button order and card colors.

            if st.button(
                f"Open {icon} {title}",
                key=f"home_card_{index}",
                use_container_width=True,
            ):
                go_page(target)


# ============================================================
# SOLVE ANYTHING
# ============================================================

def page_solve():

    show_page_title(
        "🧠 Solve Anything",
        "Ask questions across education, writing, science and general topics.",
    )

    question = st.text_area(
        "Your question",
        placeholder=(
            "Ask anything...\n\n"
            "Example: Explain quantum physics in simple language."
        ),
        height=180,
        key="solve_question",
    )

    if st.button(
        "🚀 Solve My Question",
        key="solve_button",
        use_container_width=True,
    ):

        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("Thinking..."):

            ok, answer = ask_gemini(
                f"""
You are NavaBharat AI.

Answer the following user question clearly and accurately.

Question:
{question}

Use headings, bullets, equations and examples when useful.
Do not invent current facts.
"""
            )

        if ok:
            st.session_state.last_answer = answer
            render_ai_result(
                "AI Answer",
                answer,
                "solve",
            )
        else:
            st.error(answer)


# ============================================================
# SCIENCE
# ============================================================

def page_science():

    show_page_title(
        "🔬 AI Science Solver",
        "Physics • Mathematics • Chemistry • Biology • General Science",
    )

    subject = st.selectbox(
        "Choose subject",
        [
            "Physics",
            "Mathematics",
            "Chemistry",
            "Biology",
            "General Science",
        ],
    )

    question = st.text_area(
        "Problem / Question",
        placeholder=(
            "Enter your question or problem here..."
        ),
        height=180,
        key="science_question",
    )

    if st.button(
        f"🧪 Solve {subject}",
        key="science_solve",
        use_container_width=True,
    ):

        if not question.strip():
            st.warning("Enter a problem first.")
            return

        with st.spinner("Solving..."):

            ok, answer = ask_gemini(
                f"""
You are an expert {subject} tutor.

Solve this problem:

{question}

Give:
1. Concept
2. Given information
3. Formula if applicable
4. Step-by-step solution
5. Final answer
6. Short explanation

For numerical questions, show calculations clearly.
"""
            )

        if ok:
            render_ai_result(
                f"{subject} Answer",
                answer,
                f"science_{subject.lower()}",
            )
        else:
            st.error(answer)


# ============================================================
# STUDENT HUB
# ============================================================

def page_student():

    show_page_title(
        "🎓 Student Hub",
        "Study support, notes, revision and preparation.",
    )

    topic = st.text_input(
        "Topic",
        placeholder="Example: Newton's Laws",
        key="student_topic",
    )

    mode = st.selectbox(
        "What do you need?",
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
        key="student_generate",
        use_container_width=True,
    ):

        if not topic.strip():
            st.warning("Enter a topic.")
            return

        ok, answer = ask_gemini(
            f"""
Create student learning material.

Topic: {topic}
Requested format: {mode}

Make it clear and useful for students.
"""
        )

        if ok:
            render_ai_result(
                f"Student Hub — {mode}",
                answer,
                "student",
            )
        else:
            st.error(answer)


# ============================================================
# LIVE INFORMATION
# ============================================================

def page_live():

    show_page_title(
        "🌐 Live Information",
        "Use this area for current-information questions.",
    )

    st.markdown(
        """
        <div class="glass-card">
        <h3>🔎 Current Information</h3>
        <p>
        Ask a question that needs up-to-date information.
        </p>
        <p>
        Examples: current technology news, current government
        information, latest announcements, recent events, etc.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    query = st.text_area(
        "Current-information question",
        placeholder=(
            "Example: What are the latest official announcements "
            "for students?"
        ),
        height=160,
        key="live_query",
    )

    if st.button(
        "🌐 Ask About Current Information",
        key="live_button",
        use_container_width=True,
    ):

        if not query.strip():
            st.warning("Enter a question.")
            return

        ok, answer = ask_gemini(
            f"""
The user wants information that may be current.

Question:
{query}

Be explicit when you cannot verify current information.
Do not fabricate dates, announcements, jobs, exam notices,
prices or live events.

If current sources are unavailable, clearly say that the user
should verify with the relevant official source.
"""
        )

        if ok:
            render_ai_result(
                "Live Information",
                answer,
                "live",
            )
        else:
            st.error(answer)


# ============================================================
# JOBS
# ============================================================

JOB_CATEGORIES = [
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
    "Other Jobs",
]


def page_jobs():

    show_page_title(
        "💼 Job Notifications",
        "Job categories and AI assistance for finding relevant information.",
    )

    category = st.selectbox(
        "Job category",
        JOB_CATEGORIES,
    )

    query = st.text_area(
        "What job information do you need?",
        placeholder=(
            "Example: Explain what qualifications are commonly "
            "required for SSC jobs."
        ),
        height=150,
        key="job_query",
    )

    if st.button(
        "💼 Generate Job Information",
        key="job_button",
        use_container_width=True,
    ):

        if not query.strip():
            st.warning("Enter a question.")
            return

        ok, answer = ask_gemini(
            f"""
Job information category:
{category}

User question:
{query}

Do not invent a currently open vacancy.
Clearly distinguish general information from current vacancies.
Tell the user to verify current vacancies on the official
recruitment website.
"""
        )

        if ok:
            render_ai_result(
                f"Job Information — {category}",
                answer,
                "jobs",
            )
        else:
            st.error(answer)

    st.markdown("### 🔗 Useful official-source categories")

    links = {
        "🇮🇳 UPSC": "https://upsc.gov.in/",
        "🧾 SSC": "https://ssc.gov.in/",
        "🚆 Indian Railways": "https://www.rrbapply.gov.in/",
        "🏦 IBPS": "https://www.ibps.in/",
    }

    for label, url in links.items():
        st.link_button(
            label,
            url,
            use_container_width=True,
        )


# ============================================================
# EXAMS
# ============================================================

EXAM_CATEGORIES = [
    "NEET",
    "JEE Main",
    "JEE Advanced",
    "TS EAPCET",
    "AP EAPCET",
    "CUET",
    "SSC Exams",
    "UPSC Exams",
    "GATE",
    "CAT",
    "State Exams",
    "University Exams",
    "Other Exams",
]


def page_exams():

    show_page_title(
        "📝 Exam Notifications",
        "Exam categories, preparation and official-source guidance.",
    )

    category = st.selectbox(
        "Exam",
        EXAM_CATEGORIES,
    )

    query = st.text_area(
        "Exam question",
        placeholder=(
            "Example: Explain the preparation strategy for this exam."
        ),
        height=150,
        key="exam_query",
    )

    if st.button(
        "📝 Generate Exam Information",
        key="exam_button",
        use_container_width=True,
    ):

        if not query.strip():
            st.warning("Enter a question.")
            return

        ok, answer = ask_gemini(
            f"""
Exam:
{category}

User request:
{query}

Do not invent exam dates or notifications.
For current dates, advise checking the official examination
authority.
"""
        )

        if ok:
            render_ai_result(
                f"Exam Information — {category}",
                answer,
                "exams",
            )
        else:
            st.error(answer)

    st.markdown("### 🔗 Official examination sources")

    exam_links = {
        "🎯 NTA": "https://www.nta.ac.in/",
        "🏛️ UPSC": "https://upsc.gov.in/",
        "📚 SSC": "https://ssc.gov.in/",
        "🎓 GATE": "https://gate2026.iitg.ac.in/",
    }

    for label, url in exam_links.items():
        st.link_button(
            label,
            url,
            use_container_width=True,
        )


# ============================================================
# MUSIC
# ============================================================

def page_music():

    show_page_title(
        "🎵 RacharlaGPT Music",
        "Public listening library published by the administrator.",
    )

    st.markdown(
        """
        <div class="security-notice">
        🎧 Public users can listen to published songs.
        Public users do not get upload or delete controls.
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_public_music_library()

    st.divider()

    st.markdown("### 🔐 Administrator")

    if render_admin_login():

        uploaded = st.file_uploader(
            "Publish a song",
            type=[
                "mp3",
                "wav",
                "m4a",
                "aac",
                "ogg",
                "flac",
                "opus",
            ],
            key="admin_music_upload",
        )

        if uploaded is not None:

            if st.button(
                "🎵 Publish Song",
                key="publish_song",
                use_container_width=True,
            ):

                filename = Path(uploaded.name).name

                # Remove unsafe characters.
                filename = re.sub(
                    r"[^A-Za-z0-9._ -]",
                    "_",
                    filename,
                )

                destination = MUSIC_DIR / filename

                try:

                    with open(destination, "wb") as file:
                        file.write(uploaded.getbuffer())

                    st.success(
                        f"Published: {filename}"
                    )

                    st.rerun()

                except Exception as exc:
                    st.error(
                        f"Could not publish song: {exc}"
                    )

        render_admin_music_library()


# ============================================================
# VIDEO STUDIO
# ============================================================

def page_video():

    show_page_title(
        "🎬 RacharlaGPT Video Studio",
        "Simple media tools for your own content.",
    )

    st.markdown(
        """
        <div class="glass-card">
        <h3>🎞️ Video → Audio</h3>
        <p>
        Upload a video you own or have permission to process.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_video = st.file_uploader(
        "Upload video",
        type=[
            "mp4",
            "mov",
            "mkv",
            "webm",
            "avi",
        ],
        key="video_upload",
    )

    if uploaded_video is not None:

        if not ffmpeg_available():
            st.warning(
                "FFmpeg is not available on this server. "
                "Video-to-audio extraction cannot run until "
                "FFmpeg is installed."
            )

        if st.button(
            "🎧 Extract Audio",
            key="extract_audio",
            use_container_width=True,
        ):

            if not ffmpeg_available():
                st.error(
                    "FFmpeg is unavailable. "
                    "No fake conversion will be reported."
                )
                return

            suffix = Path(uploaded_video.name).suffix

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix,
                dir=UPLOAD_DIR,
            ) as temp_video:

                temp_video.write(
                    uploaded_video.getbuffer()
                )
                temp_video_path = Path(
                    temp_video.name
                )

            output_name = (
                Path(uploaded_video.name).stem
                + "_audio.mp3"
            )

            output_path = OUTPUT_DIR / output_name

            ok, message = extract_audio_from_video(
                temp_video_path,
                output_path,
            )

            try:
                temp_video_path.unlink(
                    missing_ok=True
                )
            except Exception:
                pass

            if ok:

                st.success(
                    "Audio extraction completed."
                )

                with open(
                    output_path,
                    "rb",
                ) as audio:

                    st.audio(
                        audio.read(),
                        format="audio/mp3",
                    )

                st.download_button(
                    "⬇️ Download Audio",
                    data=output_path.read_bytes(),
                    file_name=output_path.name,
                    mime="audio/mpeg",
                    use_container_width=True,
                )

            else:
                st.error(message)


# ============================================================
# CREATOR STUDIO
# ============================================================

def page_creator():

    show_page_title(
        "✍️ Creator Studio",
        "Generate scripts, captions, posts and creative ideas.",
    )

    content_type = st.selectbox(
        "Content type",
        [
            "YouTube Script",
            "Instagram Caption",
            "Facebook Post",
            "LinkedIn Post",
            "Short Video Script",
            "Blog Outline",
            "Creative Idea",
        ],
    )

    topic = st.text_area(
        "Topic",
        placeholder="Enter your topic...",
        height=150,
        key="creator_topic",
    )

    if st.button(
        "✍️ Create Content",
        key="creator_button",
        use_container_width=True,
    ):

        if not topic.strip():
            st.warning("Enter a topic.")
            return

        ok, answer = ask_gemini(
            f"""
Create a {content_type}.

Topic:
{topic}

Make the content original, clear and useful.
"""
        )

        if ok:
            render_ai_result(
                f"Creator Studio — {content_type}",
                answer,
                "creator",
            )
        else:
            st.error(answer)


# ============================================================
# TRANSLATOR
# ============================================================

def page_translator():

    show_page_title(
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
        key="translator_source",
    )

    target = st.selectbox(
        "To",
        languages,
        index=1,
        key="translator_target",
    )

    text_input = st.text_area(
        "Text to translate",
        placeholder="Paste or type text here...",
        height=200,
        key="translator_text",
    )

    if st.button(
        "🌍 Translate",
        key="translate_button",
        use_container_width=True,
    ):

        if not text_input.strip():
            st.warning("Enter text first.")
            return

        ok, answer = ask_gemini(
            f"""
Translate the following text from {source} to {target}.

Preserve the meaning and formatting as much as possible.

TEXT:
{text_input}
"""
        )

        if ok:

            st.markdown(
                "### ✅ Translated Text"
            )

            # White/dark visible output area.
            st.markdown(
                f"""
                <div style="
                    background:#ffffff;
                    color:#111827;
                    padding:20px;
                    border-radius:18px;
                    border:1px solid #dbe3ef;
                    white-space:pre-wrap;
                    font-size:17px;
                    line-height:1.6;
                ">
                {html.escape(answer)}
                </div>
                """,
                unsafe_allow_html=True,
            )

            render_share_buttons(
                "NavaBharat AI Translation",
                answer,
                "translator",
            )

        else:
            st.error(answer)


# ============================================================
# ABOUT
# ============================================================

def page_about():

    # FIX:
    # CREATOR is defined globally before this function executes.

    show_page_title(
        "ℹ️ About",
        "Information about NavaBharat AI.",
    )

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
        <div class="security-notice">
        🔒 <strong>Data & sharing information</strong><br><br>

        NavaBharat AI does not need an application database for
        browser-based sharing. Generated information can be shared
        through the available sharing buttons without creating a
        permanent application record.

        <br><br>

        AI requests may be processed by the configured AI provider.
        Therefore, do not describe the service as guaranteeing
        that no data ever leaves the server/provider.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.link_button(
        "▶️ RacharlaGPT YouTube",
        "https://www.youtube.com/@racharlgpt",
        use_container_width=True,
    )

    st.markdown(
        """
        ### ✨ Main capabilities

        - 🧠 AI question solving
        - 🔬 Physics / Mathematics / Chemistry / Science
        - 🎓 Student assistance
        - 🌐 Current-information questions
        - 💼 Job information
        - 📝 Exam information
        - 🎵 RacharlaGPT Music
        - 🎬 Video Studio
        - ✍️ Creator Studio
        - 🌍 Translator
        - 📤 Social sharing
        """
    )


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


# ============================================================
# PAGE FUNCTION MAP
# ============================================================

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

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:8px 5px 18px 5px;
        ">
            <div style="
                font-size:42px;
                line-height:1;
            ">🇮🇳</div>

            <div style="
                font-size:20px;
                font-weight:900;
                margin-top:8px;
            ">
                NavaBharat AI
            </div>

            <div style="
                font-size:11px;
                font-weight:800;
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
            key=f"navigation_{label}",
            use_container_width=True,
        ):

            # Opens selected page and automatically closes
            # navigation according to requested behavior.
            go_page(label)

    st.divider()

    if st.session_state.admin_authenticated:

        if st.button(
            "🔒 Lock Admin",
            key="lock_admin",
            use_container_width=True,
        ):
            st.session_state.admin_authenticated = False
            st.rerun()


# ============================================================
# FINAL PAGE DISPATCH
# ============================================================

# Defensive fix:
# If a stale/invalid session value somehow exists,
# never crash with NAVIGATION[...] KeyError.

if st.session_state.nav_page not in NAVIGATION:
    st.session_state.nav_page = "Home"

current_page = NAVIGATION.get(
    st.session_state.nav_page,
    page_home,
)

# Execute exactly one page.
current_page()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div style="
        text-align:center;
        padding:35px 10px 20px;
        color:#64748b;
        font-size:13px;
    ">
        <strong>{html.escape(APP_NAME)}</strong>
        · v{html.escape(APP_VERSION)}
        · {html.escape(TAGLINE)}
        <br>
        Created & Developed by
        <strong>{html.escape(CREATOR)}</strong>
    </div>
    """,
    unsafe_allow_html=True,
)
```
