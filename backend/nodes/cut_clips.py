import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from langsmith import traceable
from backend.state import GraphState

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

@traceable(name="clip_generator")
def clip_generator(state: GraphState) -> GraphState:
    """
    Reads the analysis file and generates the best clips in parallel.
    """
    print("Clips Cutting Started... ")
    output_dir = Path("outputs/best_clips") / state["id"]
    output_dir.mkdir(parents=True, exist_ok=True)

    with ThreadPoolExecutor(max_workers=3) as executor:

        futures = [
            executor.submit(
                cut_clip,
                index,
                clip,
                state["video_path"],
                state["audio_path"],
                output_dir,
            )
            for index, clip in enumerate(state['analysis'], start=1)
        ]

        clips = []
        for index, future in enumerate(futures, start=1):
            try:
                result = future.result()
                clips.append(result)
            except Exception as e:
                print(f"Clip {index} failed: {e}")

        if not clips:
            return {**state , "success": False, "error": "All clips failed"}
        
    return {
        **state ,
        "success": True,
        "clips": clips,
    }