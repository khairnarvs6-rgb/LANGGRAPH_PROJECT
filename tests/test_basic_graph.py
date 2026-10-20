
from src import basic_graph


def test_basic_graph_returns_answer():
    result = basic_graph.graph.invoke({
        "question": "What is LangGraph?"
    })

    assert result["question"] == "What is LangGraph?"
    assert result["answer"] == "You asked: What is LangGraph?"
