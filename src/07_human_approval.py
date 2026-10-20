
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class ApprovalState(TypedDict):
    action: str
    approved: bool


def request_approval(state: ApprovalState) -> dict:
    # Pause the graph and expose the proposed action.
    decision = interrupt({
        "question": "Approve this action?",
        "proposed_action": state["action"],
    })

    return {"approved": decision == "yes"}


def execute_action(state: ApprovalState) -> dict:
    if state["approved"]:
        print("Approved action:", state["action"])
    else:
        print("Action rejected.")

    return {}


builder = StateGraph(ApprovalState)
builder.add_node("approval", request_approval)
builder.add_node("execute", execute_action)

builder.add_edge(START, "approval")


def route_after_approval(state: ApprovalState) -> str:
    return "execute" if state["approved"] else "finish"


builder.add_conditional_edges(
    "approval",
    route_after_approval,
    {
        "execute": "execute",
        "finish": END,
    },
)

builder.add_edge("execute", END)

graph = builder.compile(
    checkpointer=InMemorySaver()
)

config = {
    "configurable": {
        "thread_id": "approval-demo",
    }
}

# This invocation pauses at interrupt().
result = graph.invoke(
    {
        "action": "Send a draft email",
        "approved": False,
    },
    config=config,
)

print("Paused with:", result)

# In a real application, collect this decision from a human.
decision = input("Type yes to approve, or no to reject: ").strip().lower()

result = graph.invoke(
    Command(resume=decision),
    config=config,
)

print("Final state:", result)
