from pathlib import Path
from langsmith import traceable
from backend.state import GraphState

@traceable(name="cleanup")
def cleanup(state: GraphState) -> GraphState:
    """Delete temporary files."""
    print("Removing Temporary files...")

    try:
        for path in [state["audio_path"], state["video_path"], state["transcript_path"], state["analysis_path"]]:
            Path(path).unlink(missing_ok=True)

        return {
            **state,
            "success": True,
        }

    except Exception as e:
        return {
            **state,
            "success": False,
            "error": str(e),
        }