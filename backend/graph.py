from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes.yt_download import youtube_download
from nodes.transcript import transcribe_audio
from nodes.llm_analysis import llm_analyze
from nodes.cut_clips import clip_generator
from nodes.cleanup_disk import cleanup

builder = StateGraph(GraphState)

builder.add_node("youtube_download", youtube_download)
builder.add_node("transcribe_audio" , transcribe_audio)
builder.add_node("llm_analyze" , llm_analyze)
builder.add_node("clip_generator" , clip_generator)
builder.add_node("cleanup" , cleanup)

builder.add_edge(START, "youtube_download")
builder.add_edge("youtube_download", "transcribe_audio")
builder.add_edge("transcribe_audio" , "llm_analyze")
builder.add_edge("llm_analyze" , "clip_generator")
builder.add_edge("clip_generator" , "cleanup")
builder.add_edge("cleanup" , END)

graph = builder.compile()