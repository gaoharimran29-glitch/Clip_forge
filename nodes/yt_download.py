from yt_dlp import YoutubeDL
from state import GraphState
import os
from pathlib import Path

def youtube_download(url: str):
    """Downloads the youtube video and audio and returns the metadata"""
    os.makedirs("videos", exist_ok=True)
    os.makedirs("audios", exist_ok=True)

    video_opts = {
        "format": "bestvideo",
        "outtmpl": "videos/%(title)s.%(ext)s",
    }

    audio_opts = {
    "format": "bestaudio",
    "outtmpl": "audios/%(title)s.%(ext)s",
    "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:

        with YoutubeDL(video_opts) as ydl:
            video_info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(video_info)

        with YoutubeDL(audio_opts) as ydl:
            audio_info = ydl.extract_info(url, download=True)
            audio_path = ydl.prepare_filename(audio_info)
            audio_path = str(Path(audio_path).with_suffix(".mp3"))

        return {
            "success": True,
            "title": video_info["title"],
            "video_path": video_path,
            "audio_path": audio_path,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }
        
def yt_download(state: GraphState) -> GraphState:
    """ LangGraph node responsible for downloading the YouTube video """

    result = youtube_download(state["url"])

    return {
        **state,
        **result,
    }