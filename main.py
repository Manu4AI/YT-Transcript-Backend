from fastapi import FastAPI
import yt_dlp
import requests
import os

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Transcript backend running"}

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"

        # Create cookies file from environment variable
        cookies_content = os.getenv("YOUTUBE_COOKIES")

        if not cookies_content:
            return {"error": "Cookies not configured"}

        with open("cookies.txt", "w") as f:
            f.write(cookies_content)

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "format": "none",
            "cookiefile": "cookies.txt",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        subtitles = info.get("automatic_captions") or info.get("subtitles")

        if not subtitles:
            return {"error": "No subtitles available"}

        lang = "en" if "en" in subtitles else list(subtitles.keys())[0]

        subtitle_url = subtitles[lang][0]["url"]

        response = requests.get(subtitle_url)
        transcript_xml = response.text

        return {
            "success": True,
            "language": lang,
            "transcript_raw": transcript_xml
        }

    except Exception as e:
        return {"error": str(e)}
