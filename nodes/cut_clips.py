import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from state import GraphState


def cut_clip(index, clip, video_path, audio_path, output_dir):
    """Cuts a single clip and returns its metadata."""

    start = clip["start"]
    end = clip["end"]
    duration = end - start

    output_path = output_dir / f"clip_{index}.mp4"

    command = [
        "ffmpeg",
        "-y",

        # Video Input
        "-ss", str(start),
        "-i", video_path,

        # Audio Input
        "-ss", str(start),
        "-i", audio_path,

        # Duration
        "-t", str(duration),

        # Copy video stream
        "-c:v", "copy",

        # Encode audio
        "-c:a", "aac",

        # Stop when shortest stream ends
        "-shortest",

        str(output_path),
    ]

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return {
        "id": index,
        "start": start,
        "end": end,
        "score": clip["score"],
        "reason": clip["reason"],
        "video_path": str(output_path),
    }


def get_clips(video_path: str, audio_path: str, analysis_path: str, unique_id: str):
    """
    Reads the analysis file and generates the best clips in parallel.
    """

    output_dir = Path("outputs/best_clips") / unique_id
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(analysis_path, "r", encoding="utf-8") as file:
        analysis = json.load(file)

    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = [
            executor.submit(
                cut_clip,
                index,
                clip,
                video_path,
                audio_path,
                output_dir,
            )
            for index, clip in enumerate(analysis, start=1)
        ]

        clips = [future.result() for future in futures]

    return {
        "success": True,
        "clips": clips,
    }


def clip_generator(state: GraphState) -> GraphState:
    """
    LangGraph node responsible for generating clips.
    """

    result = get_clips(
        video_path=state["video_path"],
        audio_path=state["audio_path"],
        analysis_path=state["analysis_path"],
        unique_id=state["id"],
    )

    return {
        **state,
        **result,
    }