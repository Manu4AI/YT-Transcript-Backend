from fastapi import FastAPI
import yt_dlp

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
            "writeautomaticsub": True,
            "writesubtitles": True,
            "subtitlesformat": "vtt",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        subtitles = info.get("automatic_captions") or info.get("subtitles")

        if not subtitles:
            return {"error": "No subtitles available"}

        lang = list(subtitles.keys())[0]
        formats = subtitles[lang]

        # get subtitle URL
        subtitle_url = formats[0]["url"]

        import requests
        response = requests.get(subtitle_url)
        transcript = response.text

        return {
            "success": True,
            "language": lang,
            "transcript_raw": transcript
        }

    except Exception as e:
        return {"error": str(e)}
