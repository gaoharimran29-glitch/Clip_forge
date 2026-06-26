from langgraph.graph import StateGraph, START, END
from state import GraphState
from nodes.yt_download import yt_download

builder = StateGraph(GraphState)

builder.add_node("yt_download", yt_download)

builder.add_edge(START, "yt_download")
builder.add_edge("yt_download", END)

graph = builder.compile()

result = graph.invoke({"url": ""})

print(result)