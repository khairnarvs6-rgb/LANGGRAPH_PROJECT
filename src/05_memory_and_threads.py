
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START
from langgraph.graph import MessagesState
from langgraph.checkpoint.memory import InMemorySaver

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

# Store checkpoints in memory for this running process.
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)


def chat(question: str, thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    result = graph.invoke(
        {"messages": [HumanMessage(content=question)]},
        config=config,
    )

    print(result["messages"][-1].content)


# Both messages share the same thread.
chat("My favourite language is Python.", "user-1")
chat("Which programming language did I mention?", "user-1")

# A different thread has separate conversational state.
chat("Which programming language did I mention?", "user-2")
