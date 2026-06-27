from faster_whisper import WhisperModel
import json
import os
from pathlib import Path
from state import GraphState

def transcribe(audio_path: str):
    """Generate the transcription for audio of youtube video and save in the json file"""
    
    audio_file = Path(audio_path)
    transcript_path = Path("outputs/transcripts") / f"{audio_file.stem}.json"
    transcript_path.parent.mkdir(parents=True, exist_ok=True)

    model_size = "medium"

    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_path, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    transcript = []

    for segment in segments:
        transcript.append(
            {
                "start":segment.start ,
                "end":segment.end ,
                "text":segment.text
            }
        )

    with open(transcript_path, "w+", encoding="utf-8") as file:
        json.dump(transcript, file, indent=4, ensure_ascii=False)

    return {
        "success":True ,
        "transcript_path": str(transcript_path) , 
        "language": info.language
    }

def transcribe_audio(state: GraphState) -> GraphState:
    """ LangGraph node responsible for transcribing the downloaded audio from youtube video """

    result = transcribe(state["audio_path"])

    return {
        **state,
        **result,
    }