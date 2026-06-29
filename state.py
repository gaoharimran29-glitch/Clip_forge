from typing import TypedDict

class GraphState(TypedDict, total=False):
    success: bool
    id: str
    url: str
    title: str
    video_path: str
    audio_path: str
    transcript: list
    transcript_path: str
    analysis: list
    analysis_path: str
    language: str
    clips: list
    error: str