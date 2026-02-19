from fastapi import FastAPI
import yt_dlp
import requests

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Transcript backend running"}

@app.get("/transcript/{video_id}")
def get_transcript(video_id: str):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "cookiefile": "cookies.txt",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        subtitles = info.get("automatic_captions") or info.get("subtitles")

        if not subtitles:
            return {"error": "No subtitles available"}

        # Prefer English if available
        if "en" in subtitles:
            lang = "en"
        else:
            lang = list(subtitles.keys())[0]

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
