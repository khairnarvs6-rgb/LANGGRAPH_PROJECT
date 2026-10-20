
import operator
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class WorkflowState(TypedDict):
    steps: Annotated[list[str], operator.add]
    count: int


def step_one(state: WorkflowState) -> dict:
    return {
        "steps": ["Step 1 completed"],
        "count": state["count"] + 1,
    }


def step_two(state: WorkflowState) -> dict:
    return {
        "steps": ["Step 2 completed"],
        "count": state["count"] + 1,
    }


builder = StateGraph(WorkflowState)
builder.add_node("step_one", step_one)
builder.add_node("step_two", step_two)

builder.add_edge(START, "step_one")
builder.add_edge("step_one", "step_two")
builder.add_edge("step_two", END)

graph = builder.compile()

result = graph.invoke({"steps": [], "count": 0})
print(result)
