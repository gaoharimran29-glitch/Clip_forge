from typing import TypedDict

class GraphState(TypedDict, total=False):
    success: str
    id: str
    url: str
    title: str
    video_path: str
    audio_path: str
    transcript_path: str
    analysis_path: str
    language: str
    clips: list
    error: str