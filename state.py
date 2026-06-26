from typing import TypedDict

class GraphState(TypedDict, total=False):
    success: str
    url: str
    title: str
    video_path: str
    audio_path: str
    error: str