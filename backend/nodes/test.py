from backend.nodes.cleanup_disk import cleanup

state = {
    "audio_path": "outputs/audios/test.mp3",
    "video_path": "outputs/videos/test.mp4",
    "transcript_path": "outputs/transcripts/test.json",
    "analysis_path": "outputs/analysis/test.json",
}

result = cleanup(state)
print(result)