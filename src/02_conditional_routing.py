
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class AssistantState(TypedDict):
    question: str
    category: str
    answer: str


def classify_question(state: AssistantState) -> dict:
    question = state["question"].lower()

    if "rag" in question or "retrieval" in question:
        category = "rag"
    elif "langgraph" in question or "agent" in question:
        category = "langgraph"
    else:
        category = "general"

    return {"category": category}


def choose_route(state: AssistantState) -> str:
    # The returned string selects a conditional edge.
    return state["category"]


def explain_langgraph(state: AssistantState) -> dict:
    return {"answer": "LangGraph manages stateful AI workflows."}


def explain_rag(state: AssistantState) -> dict:
    return {"answer": "RAG retrieves relevant information before generating an answer."}


def explain_general(state: AssistantState) -> dict:
    return {"answer": "This is the general assistant route."}


builder = StateGraph(AssistantState)

builder.add_node("classify", classify_question)
builder.add_node("langgraph", explain_langgraph)
builder.add_node("rag", explain_rag)
builder.add_node("general", explain_general)

builder.add_edge(START, "classify")

builder.add_conditional_edges(
    "classify",
    choose_route,
    {
        "langgraph": "langgraph",
        "rag": "rag",
        "general": "general",
    },
)

builder.add_edge("langgraph", END)
builder.add_edge("rag", END)
builder.add_edge("general", END)

graph = builder.compile()

for question in [
    "What is LangGraph?",
    "Explain RAG retrieval",
    "What is Python?",
]:
    result = graph.invoke({
        "question": question,
        "category": "",
        "answer": "",
    })
    print(question, "->", result["answer"])
