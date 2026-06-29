from pathlib import Path
from state import GraphState

def cleanup(state: GraphState) -> GraphState:
    """Delete temporary files."""
    try:
        for key in [state["audio_path"], state["video_path"], state["transcript_path"], state["analysis_path"]]:
            path = state.get(key)
            if path:
                Path(path).unlink(missing_ok=True)

        return {
            **state ,
            "success": True,
        }
    
    except Exception as e:
        return {
            **state ,
            "success": False,
            "error": str(e)
        }