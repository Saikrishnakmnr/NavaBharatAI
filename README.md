# NavaBharat AI v5.0.0

**POWERED BY RACHARLAGPT**  
Created & Developed by **Racharla Saikrishna**

Premium Streamlit app with custom navigation, high-contrast inputs, Gemini integration, live RSS search, admin-published music, bundled FFmpeg media conversion, and free local image→MP4 reel creation.

## Streamlit Cloud Secrets

In **App → Settings → Secrets**, use:

```toml
GEMINI_API_KEY = "YOUR_KEY"
GEMINI_MODEL = "gemini-3.8-flash"
MUSIC_ADMIN_PASSWORD = "YOUR_ADMIN_PASSWORD"
```

Do not commit the real `secrets.toml`.

## Music

Visitors see the published RacharlaGPT Music library; they are not given an audio upload control. Admin publishing is protected by `MUSIC_ADMIN_PASSWORD`.

## FFmpeg

The app does **not** call a system `ffmpeg` command. It uses `imageio-ffmpeg`, which supplies an FFmpeg binary through the Python dependency. This fixes the previous `No such file or directory: 'ffmpeg'` failure.

## Live Information

Live search has a no-key Google News RSS path. If Gemini is configured, the app also offers a Gemini web-search answer. Direct public sources are always shown.

## YouTube

The app does not implement a general third-party YouTube-to-MP3 downloader. Public YouTube URLs are intended for AI analysis where supported. Upload original/permitted video files for audio extraction.
