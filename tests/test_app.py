from pathlib import Path
import ast
import subprocess
import tempfile
import os

ROOT = Path(__file__).parents[1]
SRC = ROOT / "app.py"


def test_python_syntax():
    ast.parse(SRC.read_text(encoding="utf-8"))


def test_required_pages_and_features():
    s = SRC.read_text(encoding="utf-8")
    for needle in ["Solve Anything","AI Science Solver","Student Hub","Live Information","RacharlaGPT Music","Video Studio","Creator Studio","Translator","st.navigation","st.Page"]:
        assert needle in s
    assert "imageio_ffmpeg" in s
    assert "MUSIC_ADMIN_PASSWORD" in s
    assert "caption" in s and "text_card.png" in s
    assert "GEMINI_API_KEY" in s


def test_no_system_ffmpeg_call():
    s = SRC.read_text(encoding="utf-8")
    assert 'cmd = ["ffmpeg"' not in s


def test_bundled_ffmpeg_can_render_media():
    import imageio_ffmpeg
    exe = imageio_ffmpeg.get_ffmpeg_exe()
    assert Path(exe).exists()
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "tone.mp4"
        p = subprocess.run([exe,"-y","-f","lavfi","-i","color=c=black:s=320x240:d=1","-f","lavfi","-i","sine=frequency=440:duration=1","-shortest","-c:v","libx264","-c:a","aac",str(out)],capture_output=True,text=True,timeout=60)
        assert p.returncode == 0, p.stderr[-1000:]
        assert out.exists() and out.stat().st_size > 0
        mp3 = Path(td) / "tone.mp3"
        p2 = subprocess.run([exe,"-y","-i",str(out),"-vn","-codec:a","libmp3lame","-q:a","2",str(mp3)],capture_output=True,text=True,timeout=60)
        assert p2.returncode == 0, p2.stderr[-1000:]
        assert mp3.exists() and mp3.stat().st_size > 0
