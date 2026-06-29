from faster_whisper import WhisperModel
import json
from pathlib import Path
from state import GraphState

model_size = "medium"

try:
    try:
        model = WhisperModel(model_size, device="cuda", compute_type="int8")
    except Exception:
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
except Exception as e:
    print(f"An error occurred while loading the Whisper model: {str(e)}")
    model = None

def transcribe_audio(state: GraphState , MAX_CHUNK_DURATION: int = 30) -> GraphState:
    """Generate the transcription for audio of youtube video and save in the json file"""
    
    transcript_path = Path("outputs/transcripts") / f"{state['id']}.json"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        segments, info = model.transcribe(state['audio_path'], beam_size=5)
        print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    except Exception as e:
        return {
        **state ,
        "success":False ,
        "error": str(e) , 
    }

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
        **state ,
        "success":True ,
        "transcript": transcript ,
        "transcript_path": str(transcript_path) , 
        "language": info.language
    }