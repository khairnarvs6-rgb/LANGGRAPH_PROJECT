from typing_extensions import TypedDict
from langgraph.graph import END, START, StateGraph


class AssistantState(TypedDict):
    question: str
    answer: str


def answer_question(state: AssistantState) -> dict:
    question = state["question"]

    return {
        "answer": f"You asked: {question}"
    }


builder = StateGraph(AssistantState)
builder.add_node("answer_question", answer_question)
builder.add_edge(START, "answer_question")
builder.add_edge("answer_question", END)
graph = builder.compile()
