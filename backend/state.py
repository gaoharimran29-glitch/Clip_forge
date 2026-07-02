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
    clips: list
    clips_path: list
    clips_path_normalized: list
    error: str