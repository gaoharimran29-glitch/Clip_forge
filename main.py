from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes.yt_download import yt_download
from nodes.transcript import transcribe_audio

builder = StateGraph(GraphState)

builder.add_node("yt_download", yt_download)
builder.add_node("transcribe_audio" , transcribe_audio)

builder.add_edge(START, "yt_download")
builder.add_edge("yt_download", "transcribe_audio")
builder.add_edge("transcribe_audio" , END)

graph = builder.compile()

result = graph.invoke({"url": "https://youtu.be/eRM2reLxN5k?si=T3TcWt5HxtQDnCTa"})

print(result)