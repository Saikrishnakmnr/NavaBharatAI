import io
import os
import re
import time
import html
import tempfile
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# AUTOMATIC HTML HEAD INJECTION (FOR GA & MONETAG VERIFICATION)
# ============================================================

def inject_tracking_scripts():
    """
    Patches Streamlit's underlying static index.html file dynamically at startup.
    This injects the Google Analytics and Monetag script tags into the real <head>
    element so that Google Tag verification and crawlers detect G-39MNX1V7XK.
    """
    try:
        streamlit_path = Path(st.__path__[0])
        index_path = streamlit_path / "static" / "index.html"
        
        if index_path.exists():
            html_text = index_path.read_text(encoding="utf-8")
            
            if "G-39MNX1V7XK" not in html_text:
                head_injection = """
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-39MNX1V7XK"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-39MNX1V7XK');
    </script>

    <!-- Monetag Script (Zone ID: 11941649) -->
    <script src="https://3nbf4.com/act/files/tag.min.js?z=11941649" data-cfasync="false" async></script>
    """
                updated_html = html_text.replace("<head>", f"<head>\n{head_injection}")
                index_path.write_text(updated_html, encoding="utf-8")
    except Exception:
        # Fallback if filesystem is read-only
        pass

inject_tracking_scripts()


# ============================================================
# NAVABHARAT AI
# POWERED BY RACHARLAGPT
# Created & Developed by Racharla Saikrishna
# ============================================================

APP_NAME = "NavaBharat AI"
APP_VERSION = "6.0.0"
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


/* BUTTONS — mixed radiant colors, strong contrast, visible text */

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

/* Different radiant colors for different buttons/tabs */
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

/* Make button labels visible on every theme */
.stButton > button p,
.stDownloadButton > button p,
.stLinkButton > a p,
.stFormSubmitButton > button p,
.stLinkButton > a div {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 900 !important;
}

/* Home cards — different radiant backgrounds */
.home-card-1 { background: linear-gradient(135deg,rgba(239,246,255,.98),rgba(219,234,254,.94),rgba(224,231,255,.92)) !important; }
.home-card-2 { background: linear-gradient(135deg,rgba(250,245,255,.98),rgba(243,232,255,.94),rgba(252,231,243,.92)) !important; }
.home-card-3 { background: linear-gradient(135deg,rgba(236,253,245,.98),rgba(209,250,229,.94),rgba(207,250,254,.92)) !important; }
.home-card-4 { background: linear-gradient(135deg,rgba(255,247,237,.98),rgba(254,215,170,.90),rgba(254,240,138,.84)) !important; }
.home-card-5 { background: linear-gradient(135deg,rgba(239,246,255,.98),rgba(224,242,254,.94),rgba(233,213,255,.92)) !important; }

.home-card-1, .home-card-2, .home-card-3, .home-card-4, .home-card-5 {
    transition: transform .20s ease, box-shadow .20s ease, border-color .20s ease;
}
.home-card-1:hover, .home-card-2:hover, .home-card-3:hover,
.home-card-4:hover, .home-card-5:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 50px rgba(30,41,59,.16);
    border-color: rgba(99,102,241,.35);
}


/* SOCIAL SHARE BUTTON COLORS */
.share-whatsapp a { background: linear-gradient(120deg,#16a34a,#22c55e,#84cc16) !important; }
.share-facebook a { background: linear-gradient(120deg,#1877f2,#2563eb,#60a5fa) !important; }
.share-x a { background: linear-gradient(120deg,#111827,#334155,#000000) !important; }
.share-linkedin a { background: linear-gradient(120deg,#0a66c2,#0284c7,#06b6d4) !important; }
.share-instagram a { background: linear-gradient(120deg,#7c3aed,#db2777,#f97316) !important; }

/* INPUTS */

[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {

    background:
        #ffffff !important;

    color:
        #111827 !important;

    caret-color:
        #111827 !important;

    border:
        2px solid #cbd5e1 !important;

    border-radius:
        15px !important;

    font-size:
        16px !important;
}

[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder {

    color:
        #64748b !important;

    opacity:
        1 !important;
}


/* FILE UPLOAD */

[data-testid="stFileUploader"] section {

    background:
        #ffffff !important;

    border:
        2px dashed #cbd5e1 !important;

    border-radius:
        17px !important;
}


/* GENERAL TEXT */

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {

    color:
        #1f2937;
}

.notice {
    padding: 14px 17px;

    border-radius: 16px;

    background: #eff6ff;

    border: 1px solid #bfdbfe;

    color: #1e3a8a;

    margin: 12px 0;
}

.warn {
    padding: 14px 17px;

    border-radius: 16px;

    background: #fff7ed;

    border: 1px solid #fed7aa;

    color: #9a3412;

    margin: 12px 0;
}

.success-box {
    padding: 14px 17px;

    border-radius: 16px;

    background: #ecfdf5;

    border: 1px solid #a7f3d0;

    color: #065f46;

    margin: 12px 0;
}


/* MOBILE */

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
# SECRETS
# ============================================================

def safe_secret(name: str, default: str = "") -> str:

    candidates = [
        name,
        name.lower(),
        name.upper(),
    ]

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


def gemini_key():

    return (
        safe_secret("GEMINI_API_KEY")
        or safe_secret("GOOGLE_API_KEY")
    )


def configured_models():

    primary = safe_secret(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    models = [
        primary,
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash-lite",
    ]

    return list(
        dict.fromkeys(
            x for x in models if x
        )
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

@st.cache_resource(show_spinner=False)
def get_gemini_client():

    key = gemini_key()

    if not key:
        return None

    try:

        from google import genai

        return genai.Client(
            api_key=key
        )

    except Exception:
        return None


def clean_error(exc):

    text = str(exc)

    # Never print possible keys/tokens.
    text = re.sub(
        r"[A-Za-z0-9_-]{30,}",
        "[redacted]",
        text
    )

    return text[:1600]


def gemini_generate(
    prompt: str,
    grounded: bool = False,
    retries: int = 2,
):

    client = get_gemini_client()

    if client is None:

        return (
            False,
            "Gemini is not connected. "
            "Add GEMINI_API_KEY to Streamlit Secrets."
        )

    try:

        from google.genai import types

    except Exception as exc:

        return (
            False,
            f"Gemini SDK import failed: {clean_error(exc)}"
        )

    last_error = ""

    for model in configured_models():

        for attempt in range(retries + 1):

            try:

                config = None

                if grounded:

                    config = types.GenerateContentConfig(
                        tools=[
                            types.Tool(
                                google_search=types.GoogleSearch()
                            )
                        ]
                    )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config,
                )

                answer = getattr(
                    response,
                    "text",
                    None
                )

                if answer:

                    return True, answer

                last_error = (
                    f"{model}: empty response"
                )

                break

            except Exception as exc:

                raw = str(exc)

                last_error = (
                    f"{model}: {clean_error(exc)}"
                )

                transient = (
                    "503" in raw
                    or "UNAVAILABLE" in raw
                    or "429" in raw
                    or "RESOURCE_EXHAUSTED" in raw
                    or "deadline" in raw.lower()
                    or "timeout" in raw.lower()
                )

                if transient and attempt < retries:

                    time.sleep(
                        1.2 * (2 ** attempt)
                    )

                    continue

                break

    return (
        False,
        "Gemini is temporarily unavailable. "
        "The app retried the configured model and "
        "supported fallback Flash models. "
        "Please try again shortly.\n\n"
        f"Provider detail: {last_error}"
    )


# ============================================================
# STREAMLIT OUTPUT FIX
# ============================================================

def render_answer(answer):
    if answer is None:
        return
    st.markdown(answer)


# ============================================================
# FILE HELPERS
# ============================================================

def file_bytes(uploaded):

    if uploaded is None:
        return None

    if uploaded.size > MAX_UPLOAD_MB * 1024 * 1024:

        st.error(
            f"File exceeds {MAX_UPLOAD_MB} MB."
        )

        return None

    return uploaded.getvalue()


def ffmpeg_bin():

    try:

        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()

    except Exception:

        return None


# ============================================================
# VIDEO -> AUDIO
# ============================================================

def video_to_audio(
    data: bytes,
    suffix=".mp4"
):

    exe = ffmpeg_bin()

    if not exe:

        raise RuntimeError(
            "FFmpeg runtime unavailable. "
            "Install imageio-ffmpeg."
        )

    with tempfile.TemporaryDirectory() as td:

        td = Path(td)

        source = td / (
            "source" + suffix
        )

        output = td / "audio.mp3"

        source.write_bytes(data)

        command = [
            exe,
            "-y",
            "-i",
            str(source),
            "-vn",
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(output),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=180,
        )

        if (
            result.returncode != 0
            or not output.exists()
        ):

            raise RuntimeError(
                result.stderr[-1800:]
                or "Audio extraction failed."
            )

        return output.read_bytes()


# ============================================================
# REEL MAKER
# ============================================================

def make_reel(
    images,
    audio_bytes=None,
    fps=30,
):

    exe = ffmpeg_bin()

    if not exe:

        raise RuntimeError(
            "FFmpeg runtime unavailable."
        )

    with tempfile.TemporaryDirectory() as td:

        td = Path(td)

        for index, data in enumerate(images):

            (
                td /
                f"image_{index:03d}.png"
            ).write_bytes(data)

        concat_file = td / "list.txt"

        lines = []

        duration = 3

        for index in range(len(images)):

            image_path = (
                td /
                f"image_{index:03d}.png"
            )

            lines.append(
                f"file '{image_path.as_posix()}'"
            )

            lines.append(
                f"duration {duration}"
            )

        last_image = (
            td /
            f"image_{len(images)-1:03d}.png"
        )

        lines.append(
            f"file '{last_image.as_posix()}'"
        )

        concat_file.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )

        audio_path = None

        if audio_bytes:

            audio_path = td / "music.mp3"

            audio_path.write_bytes(
                audio_bytes
            )

        output = td / "reel.mp4"

        command = [
            exe,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
        ]

        if audio_path:

            command += [
                "-i",
                str(audio_path),
            ]

        command += [
            "-vf",
            (
                "scale=1080:1920:"
                "force_original_aspect_ratio=decrease,"
                "pad=1080:1920:"
                "(ow-iw)/2:"
                "(oh-ih)/2"
            ),
            "-r",
            str(fps),
            "-pix_fmt",
            "yuv420p",
            "-c:v",
            "libx264",
        ]

        if audio_path:

            command += [
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-shortest",
            ]

        command += [
            str(output)
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=240,
        )

        if (
            result.returncode != 0
            or not output.exists()
        ):

            raise RuntimeError(
                result.stderr[-1800:]
                or "Reel rendering failed."
            )

        return output.read_bytes()


# ============================================================
# LIVE NEWS RSS
# ============================================================

LANGUAGES = {
    "English": "en",
    "తెలుగు": "te",
    "हिन्दी": "hi",
    "தமிழ்": "ta",
    "ಕನ್ನಡ": "kn",
    "മലയാളം": "ml",
    "বাংলা": "bn",
    "मराठी": "mr",
    "ગુજરાતી": "gu",
    "ਪੰਜਾਬੀ": "pa",
    "اردو": "ur",
}


def fetch_rss(
    query,
    language="en"
):

    params = {
        "q": query,
        "hl": language,
        "gl": "IN",
        "ceid": f"IN:{language}",
    }

    url = (
        "https://news.google.com/rss/search?"
        + urllib.parse.urlencode(params)
    )

    try:

        response = requests.get(
            url,
            timeout=15,
            headers={
                "User-Agent":
                "NavaBharatAI/6.0"
            },
        )

        response.raise_for_status()

        root = ET.fromstring(
            response.content
        )

        items = []

        for item in root.findall(
            "./channel/item"
        )[:20]:

            title = (
                item.findtext("title")
                or ""
            )

            link = (
                item.findtext("link")
                or ""
            )

            pub = (
                item.findtext("pubDate")
                or ""
            )

            source_node = item.find(
                "source"
            )

            source = (
                source_node.text
                if source_node is not None
                else "Google News"
            )

            items.append(
                (
                    title,
                    link,
                    pub,
                    source,
                )
            )

        return items

    except Exception as exc:

        return [
            (
                "Live feed unavailable",
                "",
                "",
                str(exc),
            )
        ]


# ============================================================
# SOCIAL SHARE
# ============================================================

def social_links(
    text,
    url=CHANNEL_URL
):
    encoded_text = urllib.parse.quote_plus(str(text))
    encoded_url = urllib.parse.quote_plus(str(url))

    columns = st.columns(5)

    share_items = [
        (
            "🟢 WhatsApp",
            "https://wa.me/?text="
            + encoded_text
            + "%20"
            + encoded_url,
            "share-whatsapp",
        ),
        (
            "🔵 Facebook",
            "https://www.facebook.com/sharer/sharer.php?u="
            + encoded_url,
            "share-facebook",
        ),
        (
            "⚫ X",
            "https://twitter.com/intent/tweet?text="
            + encoded_text
            + "&url="
            + encoded_url,
            "share-x",
        ),
        (
            "🔷 LinkedIn",
            "https://www.linkedin.com/sharing/share-offsite/?url="
            + encoded_url,
            "share-linkedin",
        ),
        (
            "📸 Instagram",
            "https://www.instagram.com/",
            "share-instagram",
        ),
    ]

    for column, (label, link, css_class) in zip(columns, share_items):
        with column:
            st.markdown(
                f'<div class="share-wrap {css_class}">',
                unsafe_allow_html=True,
            )
            st.link_button(label, link, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.caption(
        "Sharing opens the selected platform. NavaBharat AI does not save "
        "your generated answer in an app database."
    )


# ============================================================
# PAGE SWITCH
# ============================================================

def go(page_name):
    st.session_state.pending_nav = page_name
    st.session_state.nav_page = page_name
    st.rerun()


# ============================================================
# HOME
# ============================================================

def page_home():

    st.markdown(
        """
<div class="hero">

<h1>🇮🇳 NavaBharat AI</h1>

<p>
POWERED BY RACHARLAGPT • AI, study, creator tools,
music and live information in one place.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.caption(
        "No caste. No religion. No barriers."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
<div class="card home-card-1">

<h3>🧠 Solve Anything</h3>

<p>
Ask questions, upload text material,
solve homework and generate structured
answers.
</p>

</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            "🧠 Open Solve Anything",
            key="home_solve",
        ):

            go("🧠 Solve Anything")

    with col2:

        st.markdown(
            """
<div class="card home-card-2">

<h3>🎬 RacharlaGPT Video Studio</h3>

<p>
Create reels from images plus optional
music. Local rendering requires no AI key.
</p>

</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            "🎬 Open Video Studio",
            key="home_video",
        ):

            go("🎬 Video Studio")

    st.markdown(
        """
<div class="card home-card-3">

<h3>🎵 RacharlaGPT Music</h3>

<p>
Public listening library. Visitors do not
upload songs. The admin publishes songs.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(
        "🎵 Open RacharlaGPT Music",
        key="home_music",
    ):

        go("🎵 RacharlaGPT Music")

    st.markdown(
        """
<div class="card home-card-4">

<h3>🌐 Live Information</h3>

<p>
Live news, jobs and examination
notifications.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(
        "🌐 Open Live Information",
        key="home_live",
    ):

        go("📡 Live Information")

    st.markdown(
        "### ▶️ RacharlaGPT YouTube"
    )

    st.link_button(
        "Open @racharlagpt",
        CHANNEL_URL,
    )


# ============================================================
# SOLVE ANYTHING
# ============================================================

def page_solve():

    st.markdown(
        """
<div class="hero">

<h1>🧠 Solve Anything</h1>

<p>
Ask a question or add text material.
Gemini answers when available.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    uploaded = st.file_uploader(
        "📎 Add text material",
        type=[
            "txt",
            "md",
            "csv",
        ],
        key="solve_material",
    )

    question = st.text_area(
        "Your question",
        height=190,
        placeholder="Ask anything…",
        key="solve_question",
    )

    if uploaded:

        data = file_bytes(
            uploaded
        )

        if data:

            question += (
                "\n\nMATERIAL:\n"
                + data.decode(
                    "utf-8",
                    errors="replace"
                )[:120000]
            )

    if st.button(
        "✨ Ask NavaBharat AI",
        key="solve_button",
    ):

        if not question.strip():

            st.warning(
                "Enter a question or add text material."
            )

        else:

            with st.spinner(
                "Thinking…"
            ):

                ok, answer = gemini_generate(
                    question
                )

            if ok:

                render_answer(answer)

                st.markdown("### 📤 Share this Answer")
                social_links(
                    answer,
                    CHANNEL_URL,
                )

            else:

                st.error(answer)


# ============================================================
# SCIENCE
# ============================================================

def page_science():

    st.markdown(
        """
<div class="hero">

<h1>🔬 AI Science Solver</h1>

<p>
Mathematics, Physics, Chemistry and Science
with structured step-by-step explanations.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    subject = st.selectbox(
        "Subject",
        [
            "Mathematics",
            "Physics",
            "Chemistry",
            "Science",
        ],
    )

    question = st.text_area(
        "Problem",
        height=190,
        placeholder=(
            f"Enter your "
            f"{subject.lower()} problem…"
        ),
    )

    if st.button(
        "🧪 Solve Step-by-Step",
        key="science_button",
    ):

        if not question.strip():

            st.warning(
                "Enter a problem first."
            )

        else:

            prompt = f"""
You are an expert {subject} tutor.

Solve the problem carefully.

Show:
1. Given information
2. Relevant concept/formula
3. Substitution
4. Calculations
5. Final answer
6. Short explanation

Problem:

{question}
"""

            with st.spinner(
                "Solving…"
            ):

                ok, answer = gemini_generate(
                    prompt
                )

            if ok:

                render_answer(answer)

                st.markdown("### 📤 Share this Science Answer")
                social_links(
                    answer,
                    CHANNEL_URL,
                )

            else:

                st.error(answer)


# ============================================================
# TRANSLATOR
# ============================================================

def page_translator():

    st.markdown(
        """
<div class="hero">

<h1>🌐 Translator</h1>

<p>
Paste copied text here. The editor has a
white background and dark text for maximum
visibility.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    target = st.selectbox(
        "Translate to",
        list(LANGUAGES.keys()),
    )

    source = st.text_area(
        "Paste text here",
        height=250,
        placeholder="Paste copied text here…",
        key="translator_text",
    )

    if st.button(
        "🔄 Translate",
        key="translator_button",
    ):

        if not source.strip():

            st.warning(
                "Paste some text first."
            )

        else:

            prompt = f"""
Translate the following text to {target}.

Preserve:
- meaning
- formatting
- names
- numbers
- URLs

Return only the translation.

TEXT:

{source}
"""

            with st.spinner(
                "Translating…"
            ):

                ok, answer = gemini_generate(
                    prompt
                )

            if ok:

                render_answer(answer)

                st.markdown("### 📤 Share this Translation")
                social_links(
                    answer,
                    CHANNEL_URL,
                )

            else:

                st.error(answer)


# ============================================================
# LIVE INFORMATION
# ============================================================

def page_live():

    st.markdown(
        """
<div class="hero">

<h1>🌐 Live Information</h1>

<p>
Live news works even when Gemini is temporarily
unavailable. Gemini Search grounding is an
optional enhancement.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    language = st.selectbox(
        "Feed language",
        list(LANGUAGES.keys()),
        key="live_language",
    )

    language_code = LANGUAGES[
        language
    ]

    query = st.text_input(
        "Search live information",
        "technology India",
    )

    if st.button(
        "🔎 Refresh Live Search",
        key="live_search",
    ):

        results = fetch_rss(
            query,
            language_code,
        )

        for (
            title,
            link,
            pub,
            source,
        ) in results:

            if link:

                st.markdown(
                    f"""
**{html.escape(title)}**

`{html.escape(source)}` •
{html.escape(pub)}
"""
                )

                st.link_button(
                    "Open source",
                    link,
                )

            else:

                st.warning(
                    f"{title}: {source}"
                )

    st.markdown(
        "### 🏛️ Official information"
    )

    official = [
        (
            "NTA — NEET / JEE / CUET",
            "https://www.nta.ac.in/",
        ),
        (
            "UPSC — Exams & Recruitment",
            "https://www.upsc.gov.in/",
        ),
        (
            "SSC — Recruitment",
            "https://ssc.gov.in/",
        ),
    ]

    for name, url in official:

        st.link_button(
            name,
            url,
        )


# ============================================================
# JOBS & EXAMS
# ============================================================

def page_jobs_exams():

    st.markdown(
        """
<div class="hero">

<h1>💼 Jobs & Exams</h1>

<p>
Latest job notifications and examination
updates with multilingual live search.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    jobs_tab, exams_tab = st.tabs(
        [
            "💼 Job Notifications",
            "🎓 Exam Notifications",
        ]
    )

    language = st.selectbox(
        "Language",
        list(LANGUAGES.keys()),
        key="jobs_exam_language",
    )

    language_code = LANGUAGES[
        language
    ]

    # --------------------------------------------------------
    # JOBS
    # --------------------------------------------------------

    with jobs_tab:

        query = st.text_input(
            "Job search",
            (
                "government jobs India "
                "recruitment notification"
            ),
            key="job_query",
        )

        if st.button(
            "🔔 Get Latest Jobs",
            key="jobs_button",
        ):

            results = fetch_rss(
                query,
                language_code,
            )

            for (
                title,
                link,
                pub,
                source,
            ) in results:

                if link:

                    st.markdown(
                        f"""
**{title}**

`{source}` • {pub}
"""
                    )

                    st.link_button(
                        "Read notification",
                        link,
                    )

    # --------------------------------------------------------
    # EXAMS
    # --------------------------------------------------------

    with exams_tab:

        exams = [
            "NEET",
            "JEE Main",
            "JEE Advanced",
            "TG EAPCET / EAMCET",
            "CUET",
            "UPSC",
            "SSC",
            "GATE",
            "UGC NET",
        ]

        exam = st.selectbox(
            "Exam",
            exams,
            key="exam_name",
        )

        query = st.text_input(
            "Exam notification search",
            (
                f"{exam} latest notification "
                "dates admit card result"
            ),
            key="exam_query",
        )

        if st.button(
            "📅 Get Latest Exam Updates",
            key="exam_button",
        ):

            results = fetch_rss(
                query,
                language_code,
            )

            for (
                title,
                link,
                pub,
                source,
            ) in results:

                if link:

                    st.markdown(
                        f"""
**{title}**

`{source}` • {pub}
"""
                    )

                    st.link_button(
                        "Open update",
                        link,
                    )

        st.markdown(
            "### 🏛️ Official portals"
        )

        official = [
            (
                "NTA",
                "https://www.nta.ac.in/",
            ),
            (
                "UPSC",
                "https://www.upsc.gov.in/",
            ),
            (
                "SSC",
                "https://ssc.gov.in/",
            ),
            (
                "TG EAPCET",
                "https://eapcet.tgche.ac.in/",
            ),
        ]

        for name, url in official:

            st.link_button(
                name,
                url,
            )


# ============================================================
# MUSIC LIBRARY
# ============================================================

def music_files():

    supported = {
        ".mp3",
        ".wav",
        ".m4a",
        ".ogg",
        ".aac",
    }

    return sorted(
        [
            p
            for p in MUSIC_DIR.iterdir()
            if (
                p.is_file()
                and p.suffix.lower()
                in supported
            )
        ],
        key=lambda x: x.name.lower(),
    )


def page_music():

    st.markdown(
        """
<div class="hero">

<h1>🎵 RacharlaGPT Music</h1>

<p>
Free public listening library.
Visitors do not upload songs here.
The admin publishes the music library.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    songs = music_files()

    if not songs:

        st.info(
            "No songs have been published yet. "
            "The admin can publish songs from "
            "Admin Music Library."
        )

    for song in songs:

        st.markdown(
            f"### 🎧 {html.escape(song.stem)}"
        )

        audio = song.read_bytes()

        st.audio(
            audio
        )

        st.download_button(
            "⬇️ Download Song",
            audio,
            file_name=song.name,
            key=f"download_{song.name}",
        )

    st.markdown(
        "### 📤 Share RacharlaGPT Music"
    )

    social_links(
        "Listen to RacharlaGPT Music",
        CHANNEL_URL,
    )


# ============================================================
# ADMIN MUSIC
# ============================================================

def page_admin_music():

    st.markdown(
        """
<div class="hero">

<h1>🔐 Admin Music Library</h1>

<p>
Private publishing and deletion area.
Visitors can listen only. The admin can publish or delete songs.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    password = st.text_input(
        "Admin password",
        type="password",
        key="music_admin_password",
    )

    expected = safe_secret(
        "MUSIC_ADMIN_PASSWORD"
    )

    if not expected:
        st.warning(
            "Set MUSIC_ADMIN_PASSWORD in Streamlit Secrets first."
        )
        return

    if password != expected:
        st.info(
            "Enter the admin password to manage the public library."
        )
        return

    st.success("Admin access verified.")

    # ---------------- PUBLISH ----------------
    st.markdown("### 📚 Publish a Song")

    upload = st.file_uploader(
        "Upload a song",
        type=["mp3", "wav", "m4a", "ogg", "aac"],
        key="admin_music_upload",
    )

    title = st.text_input(
        "Song title",
        placeholder="My Song",
        key="admin_song_title",
    )

    if st.button(
        "📚 Publish Song",
        key="publish_song",
    ):
        if not upload:
            st.warning("Choose an audio file.")
        else:
            clean_title = re.sub(
                r"[^A-Za-z0-9._ -]",
                "",
                title.strip() or Path(upload.name).stem,
            ).strip()

            if not clean_title:
                clean_title = "Untitled Song"

            extension = Path(upload.name).suffix.lower()
            destination = MUSIC_DIR / f"{clean_title}{extension}"

            data = file_bytes(upload)
            if data is not None:
                destination.write_bytes(data)
                st.success(
                    f"'{clean_title}' published to RacharlaGPT Music."
                )
                st.rerun()

    # ---------------- DELETE ----------------
    st.markdown("### 🗑️ Delete Published Songs")
    st.caption(
        "Deletion is restricted to the authenticated admin. "
        "Visitors never see these controls."
    )

    songs = music_files()

    if not songs:
        st.info("The public music library is currently empty.")
        return

    for index, song in enumerate(songs):
        col1, col2 = st.columns([4, 1])

        with col1:
            st.markdown(f"**🎧 {html.escape(song.stem)}**")
            try:
                st.audio(song.read_bytes())
            except Exception:
                st.warning("Unable to preview this file.")

        with col2:
            st.write("")
            if st.button(
                "🗑️ Delete",
                key=f"delete_song_{index}_{song.name}",
                help=f"Delete {song.name} from the public library",
            ):
                try:
                    resolved_music = MUSIC_DIR.resolve()
                    resolved_song = song.resolve()

                    if resolved_song.parent != resolved_music:
                        st.error("Invalid library path.")
                    else:
                        resolved_song.unlink()
                        st.success(
                            f"Deleted '{song.stem}' from the library."
                        )
                        st.rerun()
                except FileNotFoundError:
                    st.warning("Song was already deleted.")
                except Exception as exc:
                    st.error(
                        "Could not delete the song: "
                        + clean_error(exc)
                    )


# ============================================================
# VIDEO STUDIO
# ============================================================

def page_video():

    st.markdown(
        """
<div class="hero">

<h1>🎬 RacharlaGPT Video Studio</h1>

<p>
Free local reel maker:
images + optional music → MP4.
No AI key is required for local rendering.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    images = st.file_uploader(
        "🖼️ Add images",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp",
        ],
        accept_multiple_files=True,
        key="video_images",
    )

    music = st.file_uploader(
        "🎵 Add music to this reel",
        type=[
            "mp3",
            "wav",
            "m4a",
            "ogg",
            "aac",
        ],
        key="video_music",
    )

    title = st.text_input(
        "Reel title / caption",
        placeholder="My NavaBharat AI Reel",
    )

    if st.button(
        "🎬 Create Reel MP4",
        key="create_reel",
    ):

        if not images:

            st.warning(
                "Add at least one image."
            )

        else:

            with st.spinner(
                "Rendering reel locally…"
            ):

                try:

                    image_data = [
                        file_bytes(image)
                        for image in images
                    ]

                    music_data = (
                        file_bytes(music)
                        if music
                        else None
                    )

                    video = make_reel(
                        image_data,
                        music_data,
                    )

                    st.success(
                        "Reel created successfully."
                    )

                    st.video(video)

                    st.download_button(
                        "⬇️ Download Reel MP4",
                        video,
                        file_name=(
                            "racharlagpt_reel.mp4"
                        ),
                        mime="video/mp4",
                    )

                    if title.strip():

                        st.caption(
                            f"Caption: {title}"
                        )

                except Exception as exc:

                    st.error(
                        "Reel creation failed: "
                        + clean_error(exc)
                    )

    st.divider()

    st.markdown(
        "### 🤖 Optional AI Video Hook"
    )

    st.caption(
        "AI video generation is provider-dependent "
        "and may have limits or paid billing. "
        "The local image + music reel maker remains "
        "the free path."
    )


# ============================================================
# CREATOR STUDIO
# ============================================================

def page_creator():

    st.markdown(
        """
<div class="hero">

<h1>✨ Creator Studio</h1>

<p>
Create captions, posts, study content and
shareable material without a user database.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    platform = st.selectbox(
        "Platform",
        [
            "Instagram",
            "WhatsApp",
            "Facebook",
            "X",
            "LinkedIn",
            "YouTube",
        ],
    )

    language = st.selectbox(
        "Language",
        list(LANGUAGES.keys()),
    )

    topic = st.text_area(
        "What should the content say?",
        height=180,
        placeholder=(
            "Product launch, study notes, "
            "song promotion, announcement…"
        ),
    )

    if st.button(
        "✨ Create Content",
        key="creator_generate",
    ):

        if not topic.strip():

            st.warning(
                "Enter a topic."
            )

        else:

            prompt = f"""
Create a polished {platform} post
in {language}.

Topic:

{topic}

Do not invent unsupported factual claims.
"""

            with st.spinner(
                "Creating content…"
            ):

                ok, answer = gemini_generate(
                    prompt
                )

            if ok:

                render_answer(answer)

                st.markdown(
                    "### 📤 Share"
                )

                social_links(
                    answer,
                    CHANNEL_URL,
                )

            else:

                st.error(answer)


# ============================================================
# ABOUT / DIAGNOSTICS
# ============================================================

def page_about():

    st.markdown(
        """
<div class="hero">

<h1>ℹ️ About NavaBharat AI</h1>

<p>
POWERED BY RACHARLAGPT
</p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
**Version:** {APP_VERSION}

**Creator & Developer:** {CREATOR}

**YouTube:** {CHANNEL_URL}

**Privacy:** No public user login or app database is required for the main tools. Generated share text is passed to the platform you choose only when you press its share button.
"""
    )

    st.markdown(
        "### 🔧 Gemini Connection Diagnostic"
    )

    key_exists = bool(
        gemini_key()
    )

    st.write(
        "Gemini API key detected:",
        "YES" if key_exists else "NO",
    )

    st.write(
        "Primary model:",
        configured_models()[0],
    )

    if st.button(
        "🧪 Test Gemini Connection",
        key="gemini_diagnostic",
    ):

        ok, answer = gemini_generate(
            "Reply with exactly: "
            "NavaBharat AI Gemini connection OK",
            retries=1,
        )

        if ok:

            st.success(answer)

        else:

            st.error(answer)

    st.info(
        "If the diagnostic says the key is detected "
        "but a generation returns 503 UNAVAILABLE, "
        "the key is not the problem. Gemini can return "
        "temporary capacity errors. This app retries "
        "and then tries supported fallback models."
    )

    st.markdown(
        "### 🔗 Creator channel"
    )

    st.link_button(
        "▶️ Open @racharlagpt",
        CHANNEL_URL,
    )

    st.markdown(
        "### 📌 SEO / Sitemap"
    )

    st.write(
        "Streamlit does not automatically create "
        "a complete SEO sitemap.xml for your app. "
        "A separate static sitemap/robots layer can "
        "be added later."
    )


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

NAVIGATION = {

    "🏠 Home":
        page_home,

    "🧠 Solve Anything":
        page_solve,

    "🔬 AI Science Solver":
        page_science,

    "🌐 Translator":
        page_translator,

    "📡 Live Information":
        page_live,

    "💼 Jobs & Exams":
        page_jobs_exams,

    "🎵 RacharlaGPT Music":
        page_music,

    "🎬 Video Studio":
        page_video,

    "✨ Creator Studio":
        page_creator,

    "🔐 Admin Music Library":
        page_admin_music,

    "ℹ️ About & Diagnostics":
        page_about,
}


if "nav_page" not in st.session_state:
    st.session_state.nav_page = "🏠 Home"

if "pending_nav" not in st.session_state:
    st.session_state.pending_nav = None

if st.session_state.pending_nav in NAVIGATION:
    st.session_state.nav_page = st.session_state.pending_nav
    st.session_state.main_navigation = st.session_state.pending_nav
    st.session_state.pending_nav = None


with st.sidebar:

    st.markdown(
        """
<div class="sidebar-brand">

<div class="mark">
🇮🇳 ✨
</div>

<div class="name">
NavaBharat AI
</div>

<div class="tag">
POWERED BY RACHARLAGPT
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    st.caption(
        "Free • Public • Worldwide"
    )

    st.markdown(
        '<div class="nav-caption">Explore</div>',
        unsafe_allow_html=True,
    )

    selected = st.radio(
        "Navigation",
        list(NAVIGATION.keys()),
        index=list(
            NAVIGATION.keys()
        ).index(
            st.session_state.nav_page
        ),
        label_visibility="collapsed",
        key="main_navigation",
    )

    if selected != st.session_state.nav_page:

        st.session_state.nav_page = selected
        st.rerun()

    st.divider()

    st.link_button(
        "▶️ @racharlagpt on YouTube",
        CHANNEL_URL,
    )

    st.caption(
        "No public user database is used "
        "by these tools."
    )


# ============================================================
# RUN CURRENT PAGE
# ============================================================

if st.session_state.nav_page not in NAVIGATION:
    st.session_state.nav_page = "🏠 Home"

NAVIGATION[
    st.session_state.nav_page
]()
