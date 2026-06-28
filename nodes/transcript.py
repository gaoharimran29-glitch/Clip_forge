from faster_whisper import WhisperModel
import json
import os
from pathlib import Path
from state import GraphState

def transcribe(audio_path: str , unique_id: str , MAX_CHUNK_DURATION = 30):
    """Generate the transcription for audio of youtube video and save in the json file"""
    
    transcript_path = Path("outputs/transcripts") / f"{unique_id}.json"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)

    model_size = "medium"

    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_path, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    transcript = []

    current_chunk = {
        "start": None,
        "end": None,
        "text": ""
    }

    for segment in segments:
    
        if current_chunk["start"] is None:
            current_chunk["start"] = segment.start

        # Add text
        current_chunk["text"] += " " + segment.text.strip()

        # Update end time
        current_chunk["end"] = segment.end

        # If chunk reaches 30 seconds, save it
        if current_chunk["end"] - current_chunk["start"] >= MAX_CHUNK_DURATION:

            transcript.append({
                "start": current_chunk["start"],
                "end": current_chunk["end"],
                "text": current_chunk["text"].strip()
            })

            # Reset for the next chunk
            current_chunk = {
                "start": None,
                "end": None,
                "text": ""
            }

    # Save the final chunk if it contains any text
    if current_chunk["start"] is not None:
        transcript.append({
            "start": current_chunk["start"],
            "end": current_chunk["end"],
            "text": current_chunk["text"].strip()
        })
    
    with open(transcript_path, "w+", encoding="utf-8") as file:
        json.dump(transcript, file, indent=4, ensure_ascii=False)

    return {
        "success":True ,
        "transcript_path": str(transcript_path) , 
        "language": info.language
    }

def transcribe_audio(state: GraphState) -> GraphState:
    """ LangGraph node responsible for transcribing the downloaded audio from youtube video """

    result = transcribe(state["audio_path"] , state["id"])

    return {
        **state,
        **result,
    }