from pathlib import Path
from langsmith import traceable
from state import GraphState

@traceable(name="cleanup")
def cleanup(state: GraphState) -> dict:
    """Delete temporary files."""
    print("Removing Temporary files...")

    try:
        for path in [state["audio_path"], state["video_path"], state["transcript_path"]]:
            Path(path).unlink(missing_ok=True)
            print(f"Path deleted: {str(path)}")

        return {
            "success": True,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }