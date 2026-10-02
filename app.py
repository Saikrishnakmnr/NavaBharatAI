import io
import os
import re
import time
import html
import math
import wave
import struct
import tempfile
import subprocess
import urllib.parse
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
    Patches Streamlit's underlying static index.html file dynamically at startup.
    Reads GA Measurement ID and Monetag Zone ID from st.secrets with fallbacks.
    """
    try:
        ga_id = st.secrets.get("GA_MEASUREMENT_ID", "G-39MNX1V7XK")
        monetag_id = st.secrets.get("MONETAG_ZONE_ID", "11941649")
        
        streamlit_path = Path(st.__path__[0])
        index_path = streamlit_path / "static" / "index.html"
        
        if index_path.exists():
            html_text = index_path.read_text(encoding="utf-8")
            
            if ga_id not in html_text:
                head_injection = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());

      gtag('config', '{ga_id}');
    </script>

    <!-- Monetag Script (Zone ID: {monetag_id}) -->
    <script src="https://3nbf4.com/act/files/tag.min.js?z={monetag_id}" data-cfasync="false" async></script>
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
APP_VERSION = "6.5.0"
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


def gemini_key():
    return safe_secret("GEMINI_API_KEY") or safe_secret("GOOGLE_API_KEY")


def configured_models():
    primary = safe_secret("GEMINI_MODEL", "gemini-3.8-flash")
    models = [
        primary,
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash-lite",
        "gemini-2.5-flash-lite",
    ]
    return list(dict.fromkeys(x for x in models if x))


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
        return genai.Client(api_key=key)
    except Exception:
        return None


def clean_error(exc):
    text = str(exc)
    text = re.sub(r"[A-Za-z0-9_-]{30,}", "[redacted]", text)
    return text[:1600]


def gemini_generate(prompt: str, grounded: bool = False, retries: int = 2):
    client = get_gemini_client()
    if client is None:
        return False, "Gemini is not connected. Add GEMINI_API_KEY to Streamlit Secrets."

    try:
        from google.genai import types
    except Exception as exc:
        return False, f"Gemini SDK import failed: {clean_error(exc)}"

    last_error = ""
    for model in configured_models():
        for attempt in range(retries + 1):
            try:
                config = None
                if grounded:
                    config = types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())]
                    )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config,
                )
                answer = getattr(response, "text", None)
                if answer:
                    return True, answer

                last_error = f"{model}: empty response"
                break
            except Exception as exc:
                raw = str(exc)
                last_error = f"{model}: {clean_error(exc)}"
                transient = any(k in raw for k in ["503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "deadline", "timeout"])
                if transient and attempt < retries:
                    time.sleep(1.2 * (2 ** attempt))
                    continue
                break

    return False, f"Gemini temporarily unavailable. Detail: {last_error}"


def gemini_analyze_image(image_bytes: bytes, user_prompt: str = "") -> str:
    """Uses Gemini Vision to analyze an uploaded image and create a transformed AI image description."""
    client = get_gemini_client()
    if not client:
        return ""
    try:
        from google.genai import types
        part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        prompt = (
            "Analyze the scene, subject, gender, clothing, background, and features in this image in detail. "
            f"Modify the scene according to this user instruction: '{user_prompt}'. "
            "Return a clean, detailed text prompt suitable for an AI image generator to create a sharp high quality image."
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[part, prompt]
        )
        return getattr(response, "text", "").strip()
    except Exception:
        return ""


def render_answer(answer):
    if answer is None:
        return
    st.markdown(answer)


# ============================================================
# FFMPEG & AUDIO / MP3 SYNTHESIZER
# ============================================================

def ffmpeg_bin():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
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
        raise RuntimeError("FFmpeg runtime unavailable.")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        source = td / ("source" + suffix)
        output = td / "audio.mp3"
        source.write_bytes(data)

        command = [
            exe, "-y", "-i", str(source),
            "-vn", "-codec:a", "libmp3lame", "-q:a", "2",
            str(output)
        ]

        result = subprocess.run(command, capture_output=True, text=True, timeout=180)
        if result.returncode != 0 or not output.exists():
            raise RuntimeError("Audio extraction failed.")

        return output.read_bytes()


def make_reel(images, audio_bytes=None, fps=30):
    exe = ffmpeg_bin()
    if not exe:
        raise RuntimeError("FFmpeg runtime unavailable.")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        for index, data in enumerate(images):
            (td / f"image_{index:03d}.png").write_bytes(data)

        concat_file = td / "list.txt"
        lines = []
        duration = 3

        for index in range(len(images)):
            image_path = td / f"image_{index:03d}.png"
            lines.append(f"file '{image_path.as_posix()}'")
            lines.append(f"duration {duration}")

        last_image = td / f"image_{len(images)-1:03d}.png"
        lines.append(f"file '{last_image.as_posix()}'")
        concat_file.write_text("\n".join(lines), encoding="utf-8")

        audio_path = None
        if audio_bytes:
            audio_path = td / "music.mp3"
            audio_path.write_bytes(audio_bytes)

        output = td / "reel.mp4"
        command = [exe, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file)]

        if audio_path:
            command += ["-i", str(audio_path)]

        command += [
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-r", str(fps), "-pix_fmt", "yuv420p", "-c:v", "libx264"
        ]

        if audio_path:
            command += ["-c:a", "aac", "-b:a", "192k", "-shortest"]

        command += [str(output)]
        result = subprocess.run(command, capture_output=True, text=True, timeout=240)

        if result.returncode != 0 or not output.exists():
            raise RuntimeError("Reel rendering failed.")

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


def page_image_generator():
    st.markdown('<div class="hero"><h1>🎨 Free AI Image Studio</h1><p>Create sharp, realistic AI photos or transform uploaded user images with Flux AI power.</p></div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✨ Text to Sharp AI Image", "🖼️ Upload Image & AI Re-imagine"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        with col1:
            prompt = st.text_area("Image Description / Prompt", height=140, placeholder="e.g. A crisp detailed photo of a man eating food while watching TV in a living room, sharp focus, 8k resolution...", key="img_prompt")
        with col2:
            style = st.selectbox("Art Style", ["Photorealistic", "Digital Art", "Anime / Manga", "Cinematic", "3D Render", "Fantasy Art", "Cyberpunk"], key="img_style")
            aspect = st.selectbox("Aspect Ratio", ["1:1 (Square)", "16:9 (Landscape)", "9:16 (Portrait / Reel)"], key="img_aspect")

        if st.button("🎨 Generate Sharp AI Image", key="gen_img_btn"):
            if not prompt.strip():
                st.warning("Please enter an image description.")
            else:
                with st.spinner("Generating crisp AI Image with Flux model..."):
                    try:
                        dims = {"1:1 (Square)": (1024, 1024), "16:9 (Landscape)": (1280, 720), "9:16 (Portrait / Reel)": (720, 1280)}
                        width, height = dims.get(aspect, (1024, 1024))
                        
                        style_text = "sharp focus photorealistic photography, 8k resolution, crisp face and body features, clear subject detail" if style == "Photorealistic" else f"{style} style, crisp detail, sharp focus, high quality"
                        full_prompt = f"{prompt.strip()}, {style_text}"
                        encoded_prompt = urllib.parse.quote_plus(full_prompt)
                        seed = int(time.time() * 1000) % 1000000
                        
                        img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&seed={seed}&nologo=true&model=flux"
                        response = requests.get(img_url, timeout=35)
                        
                        if response.status_code == 200:
                            img_bytes = response.content
                            st.image(img_bytes, caption=f"Generated Image: {prompt[:80]}", use_container_width=True)
                            st.download_button("⬇️ Download Image (PNG)", data=img_bytes, file_name="navabharat_ai_image.png", mime="image/png", key="dl_gen_img")
                            st.markdown("### 📤 Share Creation")
                            social_links(f"Check out this AI image on NavaBharat AI: {prompt[:80]}", CHANNEL_URL)
                        else:
                            st.error("Image generation service busy. Please try again.")
                    except Exception as exc:
                        st.error(f"Image generation error: {clean_error(exc)}")

    with tab2:
        st.markdown("### 📤 Upload Your Image for AI Transformation")
        user_img = st.file_uploader("Upload Image to Transform", type=["png", "jpg", "jpeg", "webp"], key="user_img_uploader")
        user_mod_prompt = st.text_input("How should AI transform your uploaded image?", placeholder="e.g. Change into a futuristic superhero, or change background to a beach sunset...", key="user_mod_prompt")
        
        if st.button("⚡ Transform Uploaded Image into AI Image", key="transform_img_btn"):
            if not user_img:
                st.warning("Please upload an image file first.")
            else:
                with st.spinner("Analyzing uploaded image & generating AI transformation..."):
                    try:
                        image_bytes = user_img.getvalue()
                        ai_description = gemini_analyze_image(image_bytes, user_mod_prompt)
                        
                        if not ai_description:
                            ai_description = f"A photo transformation based on user request: {user_mod_prompt}, sharp focus, highly detailed, 8k resolution"
                        
                        encoded_prompt = urllib.parse.quote_plus(f"{ai_description}, sharp focus, high definition, clear features")
                        seed = int(time.time() * 1000) % 1000000
                        
                        img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true&model=flux"
                        response = requests.get(img_url, timeout=35)
                        
                        if response.status_code == 200:
                            transformed_bytes = response.content
                            st.image(transformed_bytes, caption="AI Transformed Image Creation", use_container_width=True)
                            st.download_button("⬇️ Download Transformed Image", data=transformed_bytes, file_name="navabharat_transformed_ai.png", mime="image/png", key="dl_transformed_img")
                        else:
                            st.error("Transformation service busy. Please try again.")
                    except Exception as exc:
                        st.error(f"Transformation failed: {clean_error(exc)}")


def page_music_generator():
    st.markdown('<div class="neon-hero"><h1>🎼 Free AI Music & Song Generator</h1><p>Compose original lyrics, music blue-prints & generate real MP3 track previews (5s, 10s, 30s, 60s limit) powered by Gemini AI.</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        lyrics_input = st.text_area("📝 Enter Your Lyrics or Song Topic", height=160, placeholder="Type your lyrics in Telugu, Hindi, English, etc. OR describe a topic (e.g. 'A high-energy party anthem about victory')...", key="mgen_lyrics")
    with c2:
        genre_style = st.selectbox("🎸 Music Style & Genre", ["Bollywood Romantic / Melodic", "Tollywood Mass Folk / High Beat", "Lo-Fi Chill & Acoustic", "EDM / Cyberpunk Synthwave", "Cinematic Orchestral Epic", "Hip Hop / Indian Rap", "Devotional / Bhakti Fusion", "Classical Fusion & Sitar"], key="mgen_genre")
        duration_sec = st.selectbox("⏱️ Song Duration (Free Limit: 60s)", ["5 Seconds (Jingle / Tag)", "10 Seconds (Reel Hook)", "30 Seconds (Half Verse)", "60 Seconds (Full Track - Max Free)"], index=3, key="mgen_duration")
        vocal_type = st.selectbox("🎤 Vocal & Melody Arrangement", ["Male & Female Chorus Duet", "Solo Male Vocalist", "Solo Female Vocalist", "High Tempo Instrumental Beats"], key="mgen_vocal")

    dur_seconds = 60
    if "5 Second" in duration_sec: dur_seconds = 5
    elif "10 Second" in duration_sec: dur_seconds = 10
    elif "30 Second" in duration_sec: dur_seconds = 30
    elif "60 Second" in duration_sec: dur_seconds = 60

    if st.button("🎼 Generate AI Song & MP3 Track", key="mgen_btn"):
        if not lyrics_input.strip():
            st.warning("Please enter your custom lyrics or song prompt.")
        else:
            with st.spinner(f"Composing {dur_seconds}s original song arrangement & generating MP3 audio track..."):
                prompt = (
                    f"You are a master music producer and songwriter powered by RacharlaGPT.\n"
                    f"Create a complete song blueprint and lyrics composition based on:\n"
                    f"- Lyrics/Topic: {lyrics_input}\n"
                    f"- Music Style: {genre_style}\n"
                    f"- Duration Target: {dur_seconds} seconds\n"
                    f"- Vocal Type: {vocal_type}\n\n"
                    f"Provide:\n"
                    f"1. 🎵 Song Title & Tempo (BPM)\n"
                    f"2. 🎼 Musical Arrangement & Instrument Stems\n"
                    f"3. 🎤 Timed Lyrics Breakdown matching {dur_seconds} Seconds\n"
                    f"4. 🎹 Chord Progression & Melody Scale Notes\n"
                )

                ok, composition = gemini_generate(prompt)

                if ok:
                    st.markdown(f'<div class="neon-panel"><h3 style="color:#a855f7; margin-top:0;">⚡ Generated Music Track Preview ({dur_seconds} Seconds - MP3)</h3><p style="color:#cbd5e1; font-size:13px;">Procedural instrumental track generated based on your selected style ({genre_style}) and duration limit.</p></div>', unsafe_allow_html=True)

                    try:
                        audio_data, mime_type, fmt = generate_synthesized_music(
                            duration_sec=dur_seconds,
                            style=genre_style,
                            requested_format="mp3"
                        )

                        st.audio(audio_data, format=mime_type)

                        st.download_button(
                            f"⬇️ Download AI Song Track (.{fmt.upper()})",
                            data=audio_data,
                            file_name=f"navabharat_ai_song_{dur_seconds}s.{fmt}",
                            mime=mime_type,
                            key="dl_generated_song_file"
                        )
                    except Exception:
                        st.caption("Audio player preview loading; full composition rendered below.")

                    st.markdown("---")
                    render_answer(composition)
                    st.markdown("---")
                    st.markdown("### 📤 Share Your AI Song Creation")
                    social_links(f"Listen to my new AI Song created on NavaBharat AI: {lyrics_input[:80]}", CHANNEL_URL)
                else:
                    st.error(composition)


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
                    if ok: render_answer(answer)
                    else: st.error(answer)

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


def page_jobs_exams():
    st.markdown('<div class="hero"><h1>💼 Jobs & Competitive Exam Alerts</h1><p>Stay updated on latest central & state government jobs, recruitment notifications, and exam updates.</p></div>', unsafe_allow_html=True)
    category = st.selectbox("Select Category", ["All Government Jobs", "Banking & Finance", "SSC & Railways", "UPSC & Civil Services", "State Public Service Commissions"], key="jobs_cat")

    if st.button("🔍 Search Job & Exam Updates", key="jobs_btn"):
        with st.spinner("Fetching latest updates..."):
            prompt = f"Provide latest notifications, exam dates, eligibility, and application details for: {category} in India. Include official portal references where relevant."
            ok, answer = gemini_generate(prompt, grounded=True)
            if ok: render_answer(answer)
            else: st.error(answer)


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


def page_admin_music():
    st.markdown('<div class="hero"><h1>🔐 Admin Music Library Manager</h1><p>Upload and manage track files in the local music directory.</p></div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload Audio Files (.mp3, .wav, .m4a, .ogg)", type=["mp3", "wav", "m4a", "ogg"], accept_multiple_files=True, key="admin_music_uploader")

    if st.button("💾 Save to Library", key="save_music_btn"):
        if not uploaded_files:
            st.warning("Please select files to upload.")
        else:
            count = 0
            for uf in uploaded_files:
                dest = MUSIC_DIR / uf.name
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
                    f.unlink()
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
        if gemini_key(): st.success("✅ GEMINI_API_KEY is configured")
        else: st.error("❌ GEMINI_API_KEY is missing in secrets")

        ga_sec = safe_secret("GA_MEASUREMENT_ID")
        if ga_sec: st.info(f"📊 GA4 ID: `{ga_sec}`")

        mon_sec = safe_secret("MONETAG_ZONE_ID")
        if mon_sec: st.info(f"💰 Monetag Zone ID: `{mon_sec}`")

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

def main():
    st.sidebar.markdown(f'<div class="sidebar-brand"><div class="mark">🇮🇳</div><div class="name">{APP_NAME}</div><div class="tag">{TAGLINE}</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="nav-caption">Navigation Menu</div>', unsafe_allow_html=True)

    if "nav" not in st.session_state:
        st.session_state["nav"] = "🏠 Home"

    selected_page = st.sidebar.radio(
        "Navigate",
        list(NAVIGATION.keys()),
        index=list(NAVIGATION.keys()).index(st.session_state["nav"]) if st.session_state["nav"] in NAVIGATION else 0,
        label_visibility="collapsed",
        key="nav_radio",
    )

    if selected_page != st.session_state["nav"]:
        st.session_state["nav"] = selected_page

    render_fn = NAVIGATION.get(st.session_state["nav"], page_home)
    render_fn()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f'<div style="text-align:center; opacity:.8; font-size:12px; padding:10px 0;"><p style="margin:0; font-weight:bold;">Created by {CREATOR}</p><p style="margin:4px 0 0;"><a href="{CHANNEL_URL}" target="_blank" style="color:#a7f3d0; text-decoration:none;">Visit YouTube Channel ↗</a></p></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
