
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import MessagesState

project_root = Path(__file__).resolve().parents[1]
load_dotenv(project_root / ".env")
load_dotenv(project_root / "tests" / ".env")

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to the project-root .env file "
        "or tests/.env; see .env.example."
    )


# 1. Define a tool that the model may call.
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the exact result."""
    return a * b


@tool
def search_knowledge(query: str) -> str:
    """Search a small demo knowledge base about LangGraph and RAG."""
    knowledge = {
        "langgraph": (
            "LangGraph builds stateful workflows using nodes, "
            "edges, state, and graph execution."
        ),
        "rag": (
            "RAG retrieves relevant documents and provides them "
            "as context to a language model."
        ),
    }

    query_lower = query.lower()

    for topic, description in knowledge.items():
        if topic in query_lower:
            return description

    return "No matching entry found in this demo knowledge base."


tools = [multiply, search_knowledge]


# 2. Initialize the Groq chat model.
llm = ChatGroq(
    model=os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-120b",
    ),
    temperature=0,
)

# 3. Let the model know which tools it can request.
llm_with_tools = llm.bind_tools(tools)


# 4. Create the assistant node.
def assistant(state: MessagesState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# 5. Build the graph.
builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")

# If the assistant requested a tool, run it.
# Otherwise, finish the turn.
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)

# After tool execution, send results back to the model.
builder.add_edge("tools", "assistant")

graph = builder.compile()


# 6. Run a question.
question = input("Ask your AI assistant: ")

result = graph.invoke({
    "messages": [HumanMessage(content=question)]
})

print("\nAI response:")
print(result["messages"][-1].content)
