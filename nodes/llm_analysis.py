import json
import os
from pathlib import Path
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from state import GraphState

class ClipAnalysis(BaseModel):
    start: float
    end: float
    text: str
    score: int = Field(ge=1, le=10, description="Score from 1 to 10 on viral potential")
    reason: str = Field(description="Reason should be one sentence explaining WHY this part is suitable for a short.")

class AnalysisResponse(BaseModel):
    clips: list[ClipAnalysis]

def llm_layer(transcript_path: str, unique_id: str) -> dict:
    """LLM layer to analyze and score each transcript chunk."""
    
    analysis_path = Path("outputs/analysis") / f"{unique_id}.json"
    analysis_path.parent.mkdir(parents=True, exist_ok=True)

    error_fallback = {
        "success": False, 
        "analysis": [], 
        "analysis_path": "", 
        "error": ""
    }

    if not os.path.exists(transcript_path):
        return {**error_fallback, "error": f"Transcript file not found: {transcript_path}"}

    with open(transcript_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        return {**error_fallback, "error": "Please setup the GROQ_API_KEY"}

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=4096, 
        streaming=False
    )

    structured_model = llm.with_structured_output(AnalysisResponse)
    
    prompt = f"""
    You are an expert YouTube Shorts editor.
    You are given transcript chunks from a YouTube video.
    Analyze EACH chunk and extract engaging hooks or highlights.

    Transcript:
    {json.dumps(data, indent=2, ensure_ascii=False)}
    """
    
    try:
        response = structured_model.invoke(prompt)
        analysis = sorted(
            [clip.model_dump() for clip in response.clips],
            key=lambda x: x["score"],
            reverse=True
            )[:3]
    except Exception as e:
        return {**error_fallback, "error": f"LLM or Parsing Error: {str(e)}"}
    
    with open(analysis_path, "w", encoding="utf-8") as file:
        json.dump(analysis, file, indent=4, ensure_ascii=False)

    return {
        "success": True,
        "analysis": analysis,
        "analysis_path": str(analysis_path),
        "error": None
    }

def llm_analyze(state: GraphState) -> GraphState:
    """LangGraph node responsible for scoring chunks."""
    result = llm_layer(state["transcript_path"], state["id"])
    
    return {
        **state,
        **result,
    }