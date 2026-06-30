from yt_dlp import YoutubeDL
from backend.state import GraphState
import os
import uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from langsmith import traceable

def download_video(url: str , video_opts):
    """Helper function to download the video"""
    with YoutubeDL(video_opts) as ydl:
        video_info = ydl.extract_info(url, download=True)
        video_path = ydl.prepare_filename(video_info)

    return video_info , video_path

def download_audio(url: str , audio_opts):
    """Helper function to download the audio """

    with YoutubeDL(audio_opts) as ydl:
        audio_info = ydl.extract_info(url, download=True)
        audio_path = ydl.prepare_filename(audio_info)
        audio_path = str(Path(audio_path).with_suffix(".mp3"))

    return audio_path

@traceable(name="youtube_download")
def youtube_download(state: GraphState) -> GraphState:
    """Downloads the youtube video and audio and returns the metadata"""
    os.makedirs("outputs/videos", exist_ok=True)
    os.makedirs("outputs/audios", exist_ok=True)

    unique_id = str(uuid.uuid4())

    video_opts = {
        "format": "bestvideo",
        "outtmpl": f"outputs/videos/{unique_id}.%(ext)s",
    }

    audio_opts = {
    "format": "bestaudio",
    "outtmpl": f"outputs/audios/{unique_id}.%(ext)s",
    "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "128",
            }
        ],
    }

    with ThreadPoolExecutor(max_workers=2) as executor:
        try:
            video_future = executor.submit(download_video, state['url'], video_opts)
            audio_future = executor.submit(download_audio, state['url'], audio_opts)

            video_info, video_path = video_future.result()
            audio_path = audio_future.result()

            result = {
                **state ,
                "success": True,
                "id": unique_id ,
                "title": video_info["title"],
                "video_path": video_path,
                "audio_path": audio_path,
            }
        
        except Exception as e:
            result = {
                **state ,
                "success": False,
                "error": str(e),
            }

    return result