import json
import os
from pathlib import Path
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from state import GraphState
from langsmith import traceable
from langchain_core.messages import HumanMessage, SystemMessage

class ClipScore(BaseModel):
    id: int = Field(description="The index of this chunk from the input transcript list")
    score: int = Field(ge=1, le=10, description="Score from 1 to 10 on viral potential")
    reason: str = Field(description="Reason should be one sentence explaining WHY this part is suitable for a short.")

class AnalysisResponse(BaseModel):
    clips: list[ClipScore]

@traceable(name="llm_analyze")
def llm_analyze(state: GraphState) -> dict:
    """LLM layer to analyze and score each transcript chunk."""
    print("LLM Analysis Started... ")
    analysis_path = Path("outputs/analysis") / f"{state['id']}.json"
    analysis_path.parent.mkdir(parents=True, exist_ok=True)

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        return {"success": False , "error": "Please setup the GROQ_API_KEY"}

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0,
        streaming=False
    )

    structured_model = llm.with_structured_output(AnalysisResponse)

    SYSTEM_PROMPT = """
        You are a viral YouTube Shorts editor specializing in both talk/podcast content and music videos.

        First, determine the content type:
        - TALK: podcasts, interviews, explainers, vlogs, commentary
        - MUSIC: songs, music videos, live performances, covers

        Then apply the correct criteria:

        ---

        IF TALK CONTENT:
        A great Short must have:
        - A strong HOOK in the first 3 seconds (surprising fact, bold claim, question that demands an answer)
        - A single clear idea — not multiple topics crammed together
        - Emotional pull: curiosity, shock, inspiration, controversy, or humor
        - A satisfying ending — punchline, revelation, or clear takeaway

        REJECT if:
        - Starts mid-sentence or mid-thought
        - Is just filler or transitions ("today we're going to talk about...")
        - Has no clear payoff or resolution

        ---

        IF MUSIC CONTENT:
        A great Short must have:
        - Starts at a musically strong point — chorus, drop, key change, or memorable hook
        - Captures an emotional peak — the most intense, beautiful, or energetic moment
        - Feels complete — doesn't cut off mid-lyric or mid-phrase awkwardly

        REJECT if:
        - Starts in the middle of a verse with no energy buildup
        - Is an intro, outro, or instrumental filler with no vocal or melodic peak
        - Cuts off before a natural musical pause or phrase ending

        ---

        Score each clip 1-10 where:
        - 10: Perfect standalone moment, immediately captivating, strong start and end
        - 7-9: Strong content but entry or exit point could be slightly better
        - 4-6: Decent moment but lacks a strong opening or natural resolution
        - 1-3: Weak energy, poor entry point, or no emotional payoff

        In your reason field, specify:
        - The content type (TALK or MUSIC)
        - For TALK: name the hook, emotional trigger, and payoff
        - For MUSIC: name the musical moment (chorus/drop/etc), the emotion it evokes, and why it stands alone well

        Respond with ONLY the id, score, and reason for your chosen clips. Do NOT repeat start, end, or text.
        """

    # Tag each transcript chunk with its index so the LLM can reference it by id
    indexed_transcript = [
        {"id": i, **chunk} for i, chunk in enumerate(state["transcript"])
    ]

    transcript_input = f"""
        Below are transcript chunks extracted from a YouTube video, each tagged with an "id".
        Choose ONLY the best 3 clips.
        Return ONLY the id, score, and reason for each chosen clip.
        Do NOT return start, end, or text — I already have that data.
        Transcript:
        {json.dumps(indexed_transcript, ensure_ascii=False, indent=2)}
        """

    messages = [SystemMessage(SYSTEM_PROMPT), HumanMessage(transcript_input)]

    try:
        response = structured_model.invoke(messages)

        analysis = []
        for clip_score in response.clips:
            original_chunk = state["transcript"][clip_score.id]
            analysis.append({
                "start": original_chunk["start"],
                "end": original_chunk["end"],
                "text": original_chunk["text"],
                "score": clip_score.score,
                "reason": clip_score.reason,
            })

        analysis = sorted(analysis, key=lambda x: x["score"], reverse=True)[:3]

    except Exception as e:
        return {"success": False, "error": f"LLM or Parsing Error: {str(e)}"}

    with open(analysis_path, "w", encoding="utf-8") as file:
        json.dump(analysis, file, indent=4, ensure_ascii=False)

    return {
        "success": True,
        "analysis": analysis,
        "analysis_path": str(analysis_path)
    }