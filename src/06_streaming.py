
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, START, StateGraph

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")
load_dotenv(project_root / "tests" / ".env")

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to the project-root .env file "
        "or tests/.env; see .env.example."
    )

llm = ChatGroq(
    model=os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b",
    ),
    temperature=0,
)


def assistant(state: MessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_edge(START, "assistant")
graph = builder.compile()

config = {
    "configurable": {
        "thread_id": "stream-demo",
    }
}

for chunk in graph.stream(
    {
        "messages": [
            HumanMessage(
                content="Explain LangGraph in three points."
            )
        ]
    },
    config=config,
    stream_mode="updates",
):
    print(chunk)
