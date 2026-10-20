
if __package__:
    from .basic_graph import graph
else:
    from basic_graph import graph

# Execute the graph with an initial state.
result = graph.invoke({
    "question": "What is LangGraph?"
})

print(result)
