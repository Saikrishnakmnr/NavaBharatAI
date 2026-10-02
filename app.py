from __future__ import annotations

import html
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import requests
import streamlit as st

APP_VERSION = "5.0.0"
BRAND = "NavaBharat AI"
CREATOR = "Racharla Saikrishna"
DEFAULT_MODEL = "gemini-3.8-flash"
ROOT = Path(__file__).resolve().parent
MUSIC_DIR = ROOT / "music_library"
MUSIC_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title=f"{BRAND} • RacharlaGPT", page_icon="🇮🇳", layout="wide", initial_sidebar_state="expanded")


def inject_css() -> None:
    st.markdown(r"""
<style>
:root{--ink:#111827;--muted:#667085;--line:#e4e7ec}
html,body,[class*="css"]{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.stApp{background:radial-gradient(circle at 5% 0%,rgba(255,145,0,.16),transparent 25%),radial-gradient(circle at 95% 0%,rgba(99,102,241,.16),transparent 28%),radial-gradient(circle at 50% 100%,rgba(20,184,166,.10),transparent 32%),linear-gradient(180deg,#f8fbff,#f3f5fb);color:var(--ink)}
.block-container{max-width:1450px;padding:1.1rem 2rem 4rem}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#090d1c 0%,#101936 48%,#1b1030 100%);border-right:1px solid rgba(255,255,255,.10);min-width:310px!important;width:310px!important}
section[data-testid="stSidebar"]>div{width:310px!important}
section[data-testid="stSidebar"] *{color:#fff!important}
.brand-lockup{padding:10px 8px 20px;margin-bottom:12px;border-bottom:1px solid rgba(255,255,255,.12)}
.brand-symbol{font-size:50px;line-height:1;filter:drop-shadow(0 10px 24px rgba(255,255,255,.18));margin-bottom:8px}
.brand-name{font-size:24px;font-weight:950;letter-spacing:-.5px;background:linear-gradient(90deg,#ff8a00,#ffd166,#22d3ee,#7c3aed,#f43f5e);-webkit-background-clip:text;background-clip:text;color:transparent!important}
.brand-sub{font-size:10px;letter-spacing:1.25px;text-transform:uppercase;color:#cbd5e1!important;font-weight:800;margin-top:3px}
.nav-caption{font-size:10px;text-transform:uppercase;letter-spacing:1.6px;color:#94a3b8!important;font-weight:900;margin:14px 8px 7px}
section[data-testid="stSidebar"] .stPageLink a{display:flex!important;align-items:center!important;gap:9px!important;border-radius:15px!important;padding:12px 13px!important;margin:4px 0!important;background:linear-gradient(100deg,rgba(255,255,255,.07),rgba(255,255,255,.035))!important;border:1px solid rgba(255,255,255,.08)!important;font-weight:850!important;white-space:normal!important;min-height:48px!important;transition:.18s ease!important}
section[data-testid="stSidebar"] .stPageLink a:hover{transform:translateX(4px) scale(1.01);background:linear-gradient(90deg,rgba(255,138,0,.22),rgba(34,211,238,.16),rgba(124,58,237,.22))!important;border-color:rgba(255,255,255,.25)!important;box-shadow:0 10px 26px rgba(0,0,0,.22)!important}
section[data-testid="stSidebar"] .stPageLink a span:first-child{font-size:23px!important;min-width:28px}
.status-pill{display:inline-flex;align-items:center;gap:7px;padding:7px 10px;border-radius:999px;background:rgba(34,197,94,.13);border:1px solid rgba(134,239,172,.22);font-size:11px;font-weight:900}
.hero{border:1px solid rgba(255,255,255,.85);border-radius:32px;padding:34px;background:linear-gradient(135deg,rgba(255,255,255,.96),rgba(244,247,255,.84));box-shadow:0 28px 80px rgba(37,48,80,.14);overflow:hidden;position:relative}
.hero:after{content:"";position:absolute;width:330px;height:330px;border-radius:50%;right:-120px;top:-130px;background:linear-gradient(135deg,rgba(255,138,0,.34),rgba(99,102,241,.25),rgba(34,211,238,.20));filter:blur(5px)}
.hero h1{font-size:clamp(40px,6vw,72px);line-height:.95;margin:0 0 12px;font-weight:950;letter-spacing:-3px;background:linear-gradient(90deg,#f97316,#eab308,#06b6d4,#6366f1,#ec4899);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{font-size:17px;color:#475467;max-width:880px;line-height:1.65;margin:0}
.kicker{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border-radius:999px;background:#fff;border:1px solid #e5e7eb;font-size:11px;font-weight:900;letter-spacing:1px;text-transform:uppercase;color:#475467;margin-bottom:14px}
.page-title{font-size:clamp(30px,4vw,44px);font-weight:950;letter-spacing:-1.4px;color:#111827;margin-bottom:3px}.page-sub{font-size:15px;color:#667085;margin-bottom:22px}
.card{background:rgba(255,255,255,.94);border:1px solid #e5e7eb;border-radius:23px;padding:22px;box-shadow:0 16px 48px rgba(31,41,55,.09);height:100%;transition:.2s ease}.card:hover{transform:translateY(-4px);box-shadow:0 25px 65px rgba(31,41,55,.14)}
.icon-badge{width:58px;height:58px;border-radius:18px;display:flex;align-items:center;justify-content:center;font-size:30px;background:linear-gradient(135deg,#fff7ed,#ecfeff,#eef2ff);box-shadow:inset 0 0 0 1px #e5e7eb,0 10px 25px rgba(31,41,55,.08)}
.card h3{margin:10px 0 6px;color:#111827;font-size:20px}.card p{color:#667085;line-height:1.55}
.stButton>button,.stDownloadButton>button{border-radius:16px!important;min-height:50px!important;border:1px solid rgba(255,255,255,.72)!important;font-weight:900!important;color:#fff!important;text-shadow:0 1px 2px rgba(0,0,0,.28)!important;box-shadow:0 12px 28px rgba(31,41,55,.14)!important;transition:.18s ease!important;background:linear-gradient(100deg,#ff7a18,#ffb703,#14b8a6,#4f46e5,#db2777)!important}
.stButton>button:hover,.stDownloadButton>button:hover{transform:translateY(-2px) scale(1.01)!important;box-shadow:0 20px 38px rgba(31,41,55,.20)!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input{background:#fff!important;color:#111827!important;border:1.5px solid #cfd6e4!important;border-radius:14px!important;caret-color:#111827!important;font-size:16px!important;-webkit-text-fill-color:#111827!important}
.stTextArea textarea::placeholder,.stTextInput input::placeholder{color:#7b8494!important;opacity:1!important}
.stSelectbox div[data-baseweb="select"]>div{background:#fff!important;color:#111827!important;border:1.5px solid #cfd6e4!important;border-radius:14px!important}
.stSelectbox div[data-baseweb="select"] span{color:#111827!important}
.stTextArea label,.stTextInput label,.stSelectbox label,.stFileUploader label,.stRadio label,.stCheckbox label,.stSlider label{color:#1f2937!important;font-weight:850!important}
[data-testid="stFileUploaderDropzone"]{background:#fff!important;border:1.5px dashed #c6cfdd!important;border-radius:16px!important}
[data-testid="stFileUploaderDropzone"] *{color:#334155!important}
[data-testid="stAlert"]{border-radius:16px!important}
[data-testid="stMetric"]{background:#fff;border:1px solid #e5e7eb;border-radius:17px;padding:12px;box-shadow:0 9px 25px rgba(31,41,55,.07)}
[data-testid="stExpander"]{background:#fff!important;border:1px solid #e5e7eb!important;border-radius:16px!important}
.footer{margin-top:38px;padding:18px;border-top:1px solid #e5e7eb;color:#7a8498;font-size:12px;text-align:center}
.library-row{background:#fff;border:1px solid #e5e7eb;border-radius:18px;padding:14px 16px;margin:8px 0;box-shadow:0 8px 22px rgba(31,41,55,.06)}
.small-note{font-size:12px;color:#667085}
</style>
""", unsafe_allow_html=True)


def secret_value(*names: str, default: str = "") -> str:
    """Read Streamlit secrets robustly, including common nested forms and env vars."""
    candidates = []
    for name in names:
        candidates += [name, name.lower()]
    # Direct secrets
    try:
        for key in candidates:
            try:
                value = st.secrets.get(key)
            except Exception:
                value = None
            if value is not None and str(value).strip():
                return str(value).strip()
        # Common nested forms: [gemini] api_key / [google] api_key
        for section in ("gemini", "google", "api"):
            try:
                obj = st.secrets.get(section)
            except Exception:
                obj = None
            if isinstance(obj, dict):
                for k in ("api_key", "GEMINI_API_KEY", "GOOGLE_API_KEY", "key"):
                    if obj.get(k):
                        return str(obj[k]).strip()
    except Exception:
        pass
    for name in names:
        value = os.getenv(name, "")
        if value.strip():
            return value.strip()
    return default


def gemini_key() -> str:
    return secret_value("GEMINI_API_KEY", "GOOGLE_API_KEY")


def gemini_model() -> str:
    return secret_value("GEMINI_MODEL", default=DEFAULT_MODEL)


def gemini_request(prompt: str, *, use_search: bool = False) -> tuple[bool, str]:
    key = gemini_key()
    if not key:
        return False, "Gemini key was not found by the app. Check Streamlit Cloud → Settings → Secrets and use GEMINI_API_KEY = \"your_key\"."
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=key)
        config = None
        if use_search:
            config = types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
        response = client.models.generate_content(model=gemini_model(), contents=prompt, config=config)
        text = getattr(response, "text", None)
        if text and text.strip():
            return True, text.strip()
        return False, "Gemini returned no text. Try again or check model access/quota."
    except Exception as exc:
        msg = str(exc).replace(key, "[REDACTED]")
        return False, f"Gemini request failed: {msg}"


def ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return ""


def extract_audio_bytes(video_bytes: bytes, suffix: str) -> tuple[bool, bytes | str]:
    exe = ffmpeg_exe()
    if not exe:
        return False, "Bundled FFmpeg is unavailable. The app needs imageio-ffmpeg installed."
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        src = td / f"input{suffix or '.mp4'}"
        out = td / "audio.mp3"
        src.write_bytes(video_bytes)
        cmd = [exe, "-y", "-i", str(src), "-vn", "-codec:a", "libmp3lame", "-q:a", "2", str(out)]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired:
            return False, "Audio extraction timed out. Try a shorter/smaller video."
        if p.returncode != 0 or not out.exists():
            detail = (p.stderr or "Audio extraction failed").splitlines()[-1]
            return False, detail
        return True, out.read_bytes()


def make_reel_from_images(images: list[tuple[str, bytes]], title: str = "", caption: str = "", seconds: float = 3.0) -> tuple[bool, bytes | str]:
    if not images:
        return False, "Add at least one image."
    exe = ffmpeg_exe()
    if not exe:
        return False, "Bundled FFmpeg is unavailable."
    with tempfile.TemporaryDirectory() as td0:
        td = Path(td0)
        paths = []
        # Build a real text card so the "image + text" feature actually places
        # the user's title/caption into the rendered MP4 rather than merely
        # showing it in the UI.
        if title.strip() or caption.strip():
            try:
                from PIL import Image, ImageDraw, ImageFont
                card = Image.new("RGB", (1280, 720), (20, 24, 48))
                draw = ImageDraw.Draw(card)
                try:
                    font_big = ImageFont.truetype("DejaVuSans-Bold.ttf", 58)
                    font_small = ImageFont.truetype("DejaVuSans.ttf", 34)
                except Exception:
                    font_big = ImageFont.load_default(); font_small = ImageFont.load_default()
                draw.text((80, 150), title.strip()[:60], fill=(255, 255, 255), font=font_big)
                # Basic wrapped caption.
                words = caption.strip().split()
                lines=[]; line=""
                for word in words:
                    test=(line+" "+word).strip()
                    if len(test)>52:
                        if line: lines.append(line)
                        line=word
                    else: line=test
                if line: lines.append(line)
                for j,line in enumerate(lines[:6]):
                    draw.text((82, 255+j*48), line, fill=(205, 215, 235), font=font_small)
                card_path=td/"text_card.png"; card.save(card_path)
                paths.append(card_path)
            except Exception:
                pass
        for i, (_, data) in enumerate(images):
            p = td / f"img_{i:03d}.png"
            p.write_bytes(data)
            paths.append(p)
        concat = td / "concat.txt"
        lines = []
        for p in paths:
            safe = p.as_posix().replace("'", "'\\''")
            lines += [f"file '{safe}'", f"duration {seconds}"]
        lines.append(f"file '{paths[-1].as_posix()}'")
        concat.write_text("\n".join(lines), encoding="utf-8")
        out = td / "reel.mp4"
        cmd = [exe,"-y","-f","concat","-safe","0","-i",str(concat),"-vf","scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p","-r","30","-movflags","+faststart",str(out)]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
        except subprocess.TimeoutExpired:
            return False, "Video generation timed out. Try fewer images."
        if p.returncode != 0 or not out.exists():
            return False, (p.stderr or "Video creation failed").splitlines()[-1]
        return True, out.read_bytes()


def google_news(query: str) -> list[dict[str, str]]:
    q = requests.utils.quote(query.strip() or "India technology")
    url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
    try:
        r = requests.get(url, timeout=12, headers={"User-Agent":"NavaBharatAI/5.0"})
        r.raise_for_status()
        import xml.etree.ElementTree as ET
        root = ET.fromstring(r.content)
        out=[]
        for item in root.findall("./channel/item")[:10]:
            title=(item.findtext("title") or "").strip()
            link=(item.findtext("link") or "").strip()
            pub=(item.findtext("pubDate") or "").strip()
            if title and link: out.append({"title":title,"link":link,"date":pub})
        return out
    except Exception:
        return []


def page_header(title: str, subtitle: str, icon: str) -> None:
    st.markdown(f'<div class="page-title">{icon} {html.escape(title)}</div><div class="page-sub">{html.escape(subtitle)}</div>', unsafe_allow_html=True)


def render_nav() -> None:
    st.sidebar.markdown(f'<div class="brand-lockup"><div class="brand-symbol">🇮🇳✨🪷</div><div class="brand-name">NavaBharat AI</div><div class="brand-sub">POWERED BY RACHARLAGPT</div><div class="brand-sub">Created & Developed by {CREATOR}</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="nav-caption">Main Navigation</div>', unsafe_allow_html=True)
    for page, label, icon in NAV_ITEMS:
        st.sidebar.page_link(page, label=f"{icon}  {label}", use_container_width=True)
    state = "AI CONNECTED" if gemini_key() else "LOCAL MODE"
    st.sidebar.markdown(f'<div class="nav-caption">Status</div><span class="status-pill">● {state}</span>', unsafe_allow_html=True)
    st.sidebar.caption(f"v{APP_VERSION} • Free local tools • No login required")


def home_page() -> None:
    st.markdown('<div class="hero"><div class="kicker">🇮🇳 FREE • WORLDWIDE • PREMIUM</div><h1>NavaBharat AI</h1><p>Powered by RacharlaGPT — one polished workspace for solving, studying, translating, live information, music and video creation.</p></div>', unsafe_allow_html=True)
    st.write("")
    cols=st.columns(3)
    cards=[("🧠","Solve Anything","AI questions, homework, coding and reasoning.",SOLVE),("🎵","RacharlaGPT Music","Listen to admin-published songs and use your own permitted media for conversion.",MUSIC),("🎬","Video Studio","Create free local MP4 reels from images with text/title support.",VIDEO)]
    for c,(icon,title,desc,page) in zip(cols,cards):
        with c:
            st.markdown(f'<div class="card"><div class="icon-badge">{icon}</div><h3>{title}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
            st.page_link(page,label=f"Open {title}",use_container_width=True)
    st.write("")
    a,b,c,d=st.columns(4)
    for c,page,label in [(a,SCIENCE,"🔬 Science Solver"),(b,STUDENTS,"🎓 Student Hub"),(c,LIVE,"🌐 Live Information"),(d,TRANSLATOR,"🌐 Translator")]:
        with c: st.page_link(page,label=label,use_container_width=True)
    st.markdown('<div class="footer">No caste. No religion. No barriers. Built for everyone.</div>',unsafe_allow_html=True)


def solve_page() -> None:
    page_header("Solve Anything","Ask a question or add text material. Gemini answers when your key is connected.","🧠")
    q=st.text_area("Your question",height=190,placeholder="Explain this problem step by step…",key="solve_q")
    f=st.file_uploader("Optional text material",type=["txt","md","csv"],key="solve_file")
    if f: q += "\n\nMaterial:\n" + f.getvalue().decode("utf-8",errors="ignore")[:30000]
    if st.button("✨ Solve Step by Step",key="solve_btn",use_container_width=True):
        ok,ans=gemini_request(q or "Help me with this problem.")
        (st.markdown(ans) if ok else st.error(ans))


def science_page() -> None:
    page_header("AI Science Solver","Mathematics, Physics, Chemistry and Science explanations with structured reasoning.","🔬")
    subject=st.selectbox("Subject",["Mathematics","Physics","Chemistry","General Science","Coding & Logic"])
    problem=st.text_area("Problem",height=180,placeholder="Enter the equation, experiment, concept or code…",key="science_problem")
    if st.button("🧪 Solve Science Problem",key="science_btn",use_container_width=True):
        ok,ans=gemini_request(f"Act as a careful {subject} tutor. Solve step by step and verify calculations.\n\n{problem}")
        (st.markdown(ans) if ok else st.error(ans))


def students_page() -> None:
    page_header("Student Hub","Create notes, flashcards, quizzes and study plans.","🎓")
    material=st.text_area("Study material",height=220,placeholder="Paste a chapter or class notes…",key="student_material")
    mode=st.selectbox("Create",["Smart Notes","Flashcards","Quiz","Study Plan"])
    if st.button("🚀 Generate Study Material",key="student_btn",use_container_width=True):
        ok,ans=gemini_request(f"Create {mode} from this material. Be accurate and well formatted.\n\n{material}")
        (st.markdown(ans) if ok else st.error(ans))


def live_page() -> None:
    page_header("Live Information","Live search works without a Gemini key through Google News RSS, with optional Gemini web-search answers when connected.","🌐")
    query=st.text_input("Search current information",placeholder="Latest technology news, exams, jobs, India…",key="live_query")
    if st.button("🔎 Search Live Information",key="live_btn",use_container_width=True):
        articles=google_news(query)
        if articles:
            st.success(f"Found {len(articles)} current news items.")
            for a in articles:
                st.markdown(f'**{html.escape(a["title"])}**  \n{html.escape(a["date"])}  • [Open source article]({a["link"]})')
        else:
            st.warning("Live news feed is temporarily unavailable. Try again.")
        if gemini_key():
            ok,ans=gemini_request(f"Answer this current-information question using web search. State dates and sources clearly.\n\n{query}",use_search=True)
            if ok:
                st.markdown("### Gemini web-search answer")
                st.markdown(ans)
    st.markdown("### Direct public sources")
    links=[("📰 Google News","https://news.google.com/"),("🌦️ Open-Meteo Weather","https://open-meteo.com/"),("🛰️ ISRO","https://www.isro.gov.in/"),("📝 NTA","https://www.nta.ac.in/"),("🏛️ UPSC","https://upsc.gov.in/")]
    st.markdown("  ".join([f"[{t}]({u})" for t,u in links]))


def music_page() -> None:
    page_header("RacharlaGPT Music","Public listening area for songs published by the admin. Visitors do not upload songs here.","🎵")
    songs=sorted([p for p in MUSIC_DIR.iterdir() if p.is_file() and p.suffix.lower() in {".mp3",".wav",".m4a",".ogg",".aac"}],key=lambda p:p.name.lower())
    st.markdown("### 🎧 RacharlaGPT Music Library")
    if not songs:
        st.info("No songs have been published yet. Admin can add songs from the protected Admin Library section below.")
    else:
        for p in songs:
            st.markdown(f'<div class="library-row"><b>🎵 {html.escape(p.stem)}</b></div>',unsafe_allow_html=True)
            st.audio(p.read_bytes(),format=p.suffix.lstrip("."))
            st.download_button("⬇️ Download Song",p.read_bytes(),file_name=p.name,key=f"download_{p.name}",use_container_width=True)
    st.divider()
    st.markdown("### 🔐 Admin Library")
    st.caption("Only the creator/admin should use this section. Set MUSIC_ADMIN_PASSWORD in Streamlit Secrets.")
    pwd=st.text_input("Admin password",type="password",key="music_admin_pwd")
    admin_pw=secret_value("MUSIC_ADMIN_PASSWORD")
    unlocked=bool(admin_pw and pwd and pwd==admin_pw)
    if admin_pw and unlocked:
        uploads=st.file_uploader("Publish songs to the library",type=["mp3","wav","m4a","ogg","aac"],accept_multiple_files=True,key="admin_music_upload")
        if st.button("📤 Publish Songs",key="publish_songs",use_container_width=True):
            if not uploads: st.warning("Select at least one song.")
            else:
                for f in uploads:
                    safe=re.sub(r"[^A-Za-z0-9._ -]","_",f.name).strip() or "song.mp3"
                    (MUSIC_DIR/safe).write_bytes(f.getvalue())
                st.success("Songs published to the library. Refresh/reopen the page to see them.")
    elif not admin_pw:
        st.warning("Admin publishing is disabled until MUSIC_ADMIN_PASSWORD is added to Streamlit Secrets.")
    elif pwd:
        st.error("Incorrect admin password.")
    st.divider()
    st.markdown("### 🎧 Video → Audio")
    st.caption("Upload only videos you own or have permission to use. The app bundles FFmpeg through imageio-ffmpeg, so a system ffmpeg executable is not required.")
    video=st.file_uploader("Video file",type=["mp4","mov","mkv","webm","avi","m4v"],key="music_video")
    if st.button("🎧 Extract MP3",key="extract_btn",use_container_width=True):
        if not video: st.error("Please select a video file first.")
        else:
            ok,result=extract_audio_bytes(video.getvalue(),Path(video.name).suffix)
            if ok:
                st.success("MP3 extracted successfully.")
                st.audio(result,format="audio/mpeg")
                st.download_button("⬇️ Download MP3",result,file_name=f"{Path(video.name).stem}.mp3",mime="audio/mpeg",use_container_width=True)
            else: st.error(str(result))
    st.divider()
    st.markdown("### ▶️ YouTube URL • AI Video Analysis")
    yt=st.text_input("Public YouTube URL",placeholder="https://www.youtube.com/watch?v=…",key="yt_url")
    st.caption("This analyzes public YouTube content when Gemini supports the URL; it does not download third-party YouTube audio.")
    if st.button("▶️ Analyze YouTube Video",key="yt_btn",use_container_width=True):
        if not yt.strip(): st.error("Enter a YouTube URL first.")
        elif not gemini_key(): st.error("Gemini key not found. Add GEMINI_API_KEY to Streamlit Secrets.")
        else:
            try:
                from google import genai
                client=genai.Client(api_key=gemini_key())
                interaction=client.interactions.create(
                    model=gemini_model(),
                    input=[
                        {"type":"text","text":"Analyze this public YouTube video. Summarize it accurately, identify key points and do not invent details."},
                        {"type":"video","uri":yt.strip()},
                    ],
                )
                ans=getattr(interaction,"output_text","")
                if ans: st.markdown(ans)
                else: st.error("Gemini returned no YouTube analysis.")
            except Exception as exc:
                st.error(f"YouTube analysis failed: {str(exc).replace(gemini_key(),'[REDACTED]')}")


def video_page() -> None:
    page_header("RacharlaGPT Video Studio","Free local image → MP4 reel maker. No API key required.","🎬")
    st.info("Free core rendering is local. Optional cloud AI video generation is provider-dependent and may be paid or quota-limited.")
    title=st.text_input("Video title",value="NavaBharat AI",key="video_title")
    caption=st.text_area("Text / caption",height=120,placeholder="Your reel title or message…",key="video_caption")
    imgs=st.file_uploader("Add images",type=["png","jpg","jpeg","webp"],accept_multiple_files=True,key="video_imgs")
    duration=st.slider("Seconds per image",1.0,8.0,3.0,0.5,key="video_duration")
    if st.button("🎞️ Generate Free MP4 Reel",key="video_btn",use_container_width=True):
        data=[(f.name,f.getvalue()) for f in imgs] if imgs else []
        ok,result=make_reel_from_images(data,title,caption,duration)
        if ok:
            st.success(f"{title} created locally.")
            st.video(result)
            st.download_button("⬇️ Download MP4",result,file_name="racharlagpt_reel.mp4",mime="video/mp4",use_container_width=True)
        else: st.error(str(result))
    with st.expander("Optional AI generation"):
        st.write("A provider such as Veo can be connected later. Do not label paid/quota-limited provider generation as unlimited free.")


def creator_page() -> None:
    page_header("Creator Studio","Create social captions and content in your chosen language and style.","✨")
    platform=st.selectbox("Platform",["Instagram","WhatsApp","Facebook","X","LinkedIn","YouTube"])
    language=st.selectbox("Language",["English","Telugu","Hindi","Tamil","Kannada","Malayalam","Bengali","Marathi","Gujarati","Urdu"])
    style=st.selectbox("Style",["Professional","Friendly","Viral","Minimal","Inspirational","Educational"])
    topic=st.text_area("What are you creating?",height=150,key="creator_topic")
    if st.button("✨ Create Content",key="creator_btn",use_container_width=True):
        ok,ans=gemini_request(f"Create a {style} {platform} post in {language}. Include a strong opening, concise body, CTA and relevant hashtags.\n\n{topic}")
        (st.markdown(ans) if ok else st.error(ans))


def translator_page() -> None:
    page_header("Translator","High-contrast editor: copied text stays visible in a white box with dark text.","🌐")
    langs=["Auto-detect","English","Telugu","Hindi","Tamil","Kannada","Malayalam","Bengali","Marathi","Gujarati","Urdu"]
    left,right=st.columns(2)
    with left: source=st.selectbox("From",langs,key="source_lang")
    with right: target=st.selectbox("To",langs[1:],index=1,key="target_lang")
    text=st.text_area("Text to translate",height=260,placeholder="Paste copied text here — it will remain visible.",key="translate_input")
    if st.button("🌍 Translate Text",key="translate_btn",use_container_width=True):
        src="the detected source language" if source=="Auto-detect" else source
        ok,ans=gemini_request(f"Translate from {src} to {target}. Preserve meaning, formatting, names, numbers and line breaks. Return only the translation.\n\n{text}") if text.strip() else (False,"Please paste or type text first.")
        if ok:
            st.text_area("Translation",value=ans,height=260,key="translation_output")
            st.download_button("⬇️ Download Translation",ans.encode("utf-8"),file_name="translation.txt",mime="text/plain",use_container_width=True)
        else: st.error(ans)


def about_page() -> None:
    page_header("About NavaBharat AI","Creator, privacy, API diagnostics and deployment information.","🇮🇳")
    st.markdown(f'<div class="card"><h3>{BRAND}</h3><p><b>POWERED BY RACHARLAGPT</b><br/>Created & Developed by {CREATOR}<br/>Version {APP_VERSION}</p><p>No caste. No religion. No barriers.</p></div>',unsafe_allow_html=True)
    st.markdown("### 🔧 Gemini connection diagnostic")
    if gemini_key():
        st.success(f"Key detected. Model configured: {gemini_model()}")
        if st.button("🧪 Test Gemini Connection",key="gemini_test",use_container_width=True):
            ok,ans=gemini_request("Reply with exactly: NavaBharat AI Gemini connection OK")
            (st.success(ans) if ok else st.error(ans))
    else:
        st.error("No Gemini key detected. Expected Streamlit Secret: GEMINI_API_KEY = \"...\"")
    with st.expander("Correct Streamlit Secrets format"):
        st.code('GEMINI_API_KEY = "YOUR_KEY"\nGEMINI_MODEL = "gemini-3.8-flash"\nMUSIC_ADMIN_PASSWORD = "YOUR_ADMIN_PASSWORD"',language="toml")
    with st.expander("Important deployment behavior"):
        st.write("Public app visitors can listen to admin-published songs. Admin publishing is password protected. Streamlit Cloud filesystem storage is not a permanent media database; for permanent music hosting, keep published songs in the repository or external object storage.")
    with st.expander("Media rights"):
        st.write("Only upload/extract media you own or have permission to use. YouTube URL analysis is not a third-party audio downloader.")


HOME=st.Page(home_page,title="Home",icon="🏠",url_path="home")
SOLVE=st.Page(solve_page,title="Solve Anything",icon="🧠",url_path="solve")
SCIENCE=st.Page(science_page,title="AI Science Solver",icon="🔬",url_path="science")
STUDENTS=st.Page(students_page,title="Student Hub",icon="🎓",url_path="students")
LIVE=st.Page(live_page,title="Live Information",icon="🌐",url_path="live")
MUSIC=st.Page(music_page,title="RacharlaGPT Music",icon="🎵",url_path="music")
VIDEO=st.Page(video_page,title="Video Studio",icon="🎬",url_path="video")
CREATOR_PAGE=st.Page(creator_page,title="Creator Studio",icon="✨",url_path="creator")
TRANSLATOR=st.Page(translator_page,title="Translator",icon="🌍",url_path="translator")
ABOUT=st.Page(about_page,title="About",icon="ℹ️",url_path="about")
PAGES=[HOME,SOLVE,SCIENCE,STUDENTS,LIVE,MUSIC,VIDEO,CREATOR_PAGE,TRANSLATOR,ABOUT]
NAV_ITEMS=[(HOME,"Home","🏠"),(SOLVE,"Solve Anything","🧠"),(SCIENCE,"AI Science Solver","🔬"),(STUDENTS,"Student Hub","🎓"),(LIVE,"Live Information","🌐"),(MUSIC,"RacharlaGPT Music","🎵"),(VIDEO,"Video Studio","🎬"),(CREATOR_PAGE,"Creator Studio","✨"),(TRANSLATOR,"Translator","🌍"),(ABOUT,"About","ℹ️")]

inject_css()
pg=st.navigation(PAGES,position="hidden")
render_nav()
pg.run()
